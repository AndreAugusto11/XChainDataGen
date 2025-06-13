import os
from typing import Any, Dict, Union

from eth_typing import HexStr
from eth_utils import event_abi_to_log_topic
from hexbytes import HexBytes
from web3 import Web3
from web3._utils.abi import map_abi_data
from web3._utils.normalizers import BASE_RETURN_NORMALIZERS
from web3.contract import Contract

from config.constants import Bridge
from extractor.base_decoder import BaseDecoder
from utils.utils import (
    CustomException,
    convert_bin_to_hex,
    load_abi,
    load_bridge_config,
    load_module,
)


class BridgeDecoder:
    CLASS_NAME = "BridgeDecoder"

    def __init__(self, bridge: Bridge, rpc_url: str):
        self.w3 = Web3(provider=Web3.HTTPProvider(rpc_url))
        self.bridge = bridge
        self.contracts = {}
        self.contracts_abi = {}
        self.event_abis = {}
        self.sign_abis = {}
        self.ordered_input_types_and_names = {}

        self.load_contracts_and_abis(bridge)

    def load_contracts_and_abis(self, bridge: Bridge):
        blockchains_config = load_bridge_config(bridge.value)

        for blockchain in blockchains_config["blockchains"]:
            for object in blockchains_config["blockchains"][blockchain]:
                for contract_addr in object["contracts"]:
                    abi_filename = object["abi"]
                    abi = load_abi(os.path.dirname(__file__), bridge, blockchain, abi_filename)
                    self.contracts_abi[(contract_addr, blockchain)] = abi

                    self.register_contract(
                        contract_addr,
                        blockchain,
                        self.contracts_abi[(contract_addr, blockchain)],
                    )

    def load_bridge_decoder(self, bridge) -> BaseDecoder:
        """Dynamically loads the decoder for the specified bridge."""
        func_name = "load_bridge_decoder"
        bridge_name = bridge.value

        try:
            module = load_module(f"extractor.{bridge_name}.decoder")
            decoder_class_name = f"{bridge_name.capitalize()}Decoder"
            decoder_class = getattr(module, decoder_class_name)

            return decoder_class()
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME, func_name, f"Bridge {bridge_name} not supported"
            ) from e

    def register_contract(self, contract_addr: str, blockchain: str, contract_abi: str):
        func_name = "register_contract"
        try:
            contract = self.w3.eth.contract(
                address=Web3.to_checksum_address(contract_addr), abi=contract_abi
            )
            self.contracts[(contract_addr, blockchain)] = contract
            self.contracts_abi[(contract_addr, blockchain)] = contract_abi

            self.event_abis[contract] = [abi for abi in contract.abi if abi["type"] == "event"]
            self.sign_abis[contract] = {
                event_abi_to_log_topic(abi): abi for abi in self.event_abis[contract]
            }
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"Error registering contract {contract_addr}: {e}",
            ) from e

    def decode_log(self, contract: Contract, result: Dict[str, Any]):
        """
        whenever possible we try to use the default (and general) decoder. Whenever events
        are too complex and fail the decoding process, we relay to the individual decoders
        for each bridge.
        """
        try:
            data = [t[2:] for t in result["topics"]]
            data += [result["data"][2:]]
            data = "0x" + "".join(data)

            return self.decode_event_input(contract, data)
        except Exception:
            self.custom_decoder = self.load_bridge_decoder(self.bridge)
            decoded_log = self.custom_decoder.decode_event(contract, result)
            decoded_log = self.convert_bytes_to_hex(decoded_log)
            return decoded_log

    def convert_bytes_to_hex(self, data: Any) -> Any:
        if isinstance(data, dict):
            return {key: self.convert_bytes_to_hex(value) for key, value in data.items()}
        elif isinstance(data, list) or isinstance(data, tuple):
            return [self.convert_bytes_to_hex(item) for item in data]
        elif isinstance(data, bytes):
            return convert_bin_to_hex(data)
        else:
            return data

    def decode_event_input(
        self, contract: Contract, event_data: Union[HexStr, str]
    ) -> Dict[str, Any]:
        func_name = "decode_event_input"

        try:
            data = HexBytes(event_data)
            selector, params = data[:32], data[32:]

            func_abi = self._get_event_abi_by_selector(contract, selector)
            [names, types] = self.get_abi_input_types_custom(func_abi, selector)
            decoded = contract.w3.codec.decode(types, params)

            # convert all fields from binary to hex
            decoded = self.convert_bytes_to_hex(decoded)

            normalized = map_abi_data(BASE_RETURN_NORMALIZERS, types, decoded)

            return dict(zip(names, normalized))
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"Error decoding event input in contract: {contract}; and data: {event_data}; {e}",
            ) from e

    def _get_event_abi_by_selector(self, contract: Contract, selector: HexBytes) -> Dict[str, Any]:
        func_name = "_get_event_abi_by_selector"
        try:
            return self.sign_abis[contract][selector]
        except KeyError as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"Event with selector {selector.hex()} is not presented in contract ABI.",
            ) from e

    def decode(self, contract_addr: str, blockchain: str, log_data: dict) -> dict:
        if (contract_addr, blockchain) not in self.contracts.keys():
            raise CustomException(
                self.CLASS_NAME,
                f"Contract {contract_addr} not found in contracts list.",
            )

        event = self.decode_log(self.contracts[(contract_addr, blockchain)], log_data)

        return event

    def get_abi_input_types_custom(self, abi_element, selector):
        """
        Extracts and orders the input names and types from an ABI element, ensuring that indexed
        and non-indexed inputs are separated and ordered correctly -- i.e., consistent with the
        data received in decode_log.

        This function is created instead of using the default `get_abi_input_names` and
        `get_abi_input_types` in `eth_utils` because they simply extract the names and types in
        the order that appears in the ABI, which then clashes with the separation of the topics
        with the general data. Therefore, we need to ensure those are in the same order to have
        a successful decoding of all fields.

        Args:
            abi_element (dict): The ABI element containing input definitions.

        Returns:
            tuple: A tuple containing two lists:
            - ordered_input_names (list): The ordered (by being indexed or not) list of input
              names.
            - ordered_input_types (list): The ordered (by being indexed or not) list of input
              types.
        """

        if self.ordered_input_types_and_names.get(selector):
            return self.ordered_input_types_and_names[selector]

        inputs = abi_element["inputs"]

        ordered_inputs = [input for input in inputs if input["indexed"]] + [
            input for input in inputs if not input["indexed"]
        ]

        ordered_input_types = []
        for input in ordered_inputs:
            if "internalType" in input and input["internalType"].startswith("struct"):
                if input["type"] == "tuple":
                    in_tuple = "("
                    for component in input["components"]:
                        in_tuple += f"{component['internalType']},"
                    in_tuple = in_tuple[:-1]
                    in_tuple += ")"
                    ordered_input_types.append(in_tuple)

                else:
                    for component in input["components"]:
                        ordered_input_types.append(component["internalType"])
            else:
                ordered_input_types.append(
                    input["internalType"] if "internalType" in input else input["type"]
                )

        ordered_input_names = []
        for input in ordered_inputs:
            if "internalType" in input and input["internalType"].startswith("struct"):
                if input["type"] == "tuple":
                    in_tuple = "("
                    for component in input["components"]:
                        in_tuple += f"{component['name']},"
                    in_tuple = in_tuple[:-1]
                    in_tuple += ")"
                    ordered_input_names.append(in_tuple)

                else:
                    for component in input["components"]:
                        ordered_input_names.append(component["name"])
            else:
                ordered_input_names.append(input["name"])

        """
        For an unkonwn reason, without this last step, some events were throwing an error:
        
        Example:
        PacketReceived events emitted by 0x4d73adb72bc3dd368966edd0f0b2148401a178e2 in Ethereum
        eth_abi.exceptions.InvalidPointer: Invalid pointer in tuple at location 64 in payload
        names = ['srcChainId', 'dstAddress', 'srcAddress', 'nonce', 'payloadHash']
        types = ['uint16', 'address', 'bytes', 'uint64', 'bytes32']

        the problem is with the "bytes" type, which is not being decoded correctly
        the lines below are a workaround to fix this issue, in which we convert the "bytes"
        type to "bytes32" whenever there is an address in the name of the input
        """
        for i in range(len(ordered_input_types)):
            if ordered_input_types[i] == "bytes" and (
                "address" in ordered_input_names[i].lower()
                or ordered_input_names[i].lower() == "to"
                or ordered_input_names[i].lower() == "from"
            ):
                ordered_input_types[i] = "bytes32"

        self.ordered_input_types_and_names[selector] = [
            ordered_input_names,
            ordered_input_types,
        ]

        return [ordered_input_names, ordered_input_types]
