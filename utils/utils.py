import importlib
import json
import logging
import os
import sys
from datetime import datetime
from enum import Enum

import base58
import requests
from hexbytes import HexBytes

from config.constants import BLOCKCHAIN_IDS, TOKEN_PRICING_SUPPORTED_BLOCKCHAINS, Bridge


def convert_blockchain_into_alchemy_id(blockchain: str) -> str:
    try:
        return TOKEN_PRICING_SUPPORTED_BLOCKCHAINS[blockchain]
    except KeyError as e:
        raise ValueError(f"{blockchain} is not a supported blockchain.") from e


def load_alchemy_api_key() -> str:
    key = os.getenv("ALCHEMY_API_KEY")
    if not key:
        raise ValueError("ALCHEMY_API_KEY environment variable not set.")
    return key


def load_solana_decoder_url() -> str:
    url = os.getenv("SOLANA_DECODER_URL")
    if not url:
        raise ValueError("SOLANA_DECODER_URL environment variable not set.")
    return url


def load_solana_api_key() -> str:
    key = os.getenv("SOLANA_API_KEY")
    if not key:
        raise ValueError("SOLANA_API_KEY environment variable not set.")
    return key


def get_block_by_timestamp(timestamp: int, blockchain: str) -> int:
    chain_id = get_blockchain_evm_id(blockchain)

    url = f"https://api.findblock.xyz/v1/chain/{chain_id}/block/before/{timestamp}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data["number"]
    else:
        raise Exception(f"Error fetching {blockchain} block with timestamp {timestamp}.")


def get_blockchain_evm_id(blockchain: str) -> str:
    for chain_id in BLOCKCHAIN_IDS:
        if BLOCKCHAIN_IDS[chain_id]["name"] == blockchain:
            return chain_id


def get_blockchain_native_token_symbol(blockchain: str) -> str:
    for chain_id in BLOCKCHAIN_IDS:
        if BLOCKCHAIN_IDS[chain_id]["name"] == blockchain:
            return BLOCKCHAIN_IDS[chain_id]["native_token"]


def get_enum_instance(enum_class: Enum, value: str):
    try:
        return enum_class(value.lower())
    except ValueError as e:
        raise ValueError(f"{value} is not a valid member of the {enum_class.__name__} Enum.") from e


def trim0x(hex_string: str) -> str:
    return hex_string[2:] if hex_string.startswith("0x") else hex_string


def convert_bin_to_hex(bin_string: str) -> str:
    return HexBytes(bin_string).hex()


def unpad_address(padded_address) -> str:
    """
    Extracts the original Ethereum address from a 32-byte padded value.
    Assumes that the address occupies the rightmost 20 bytes.

    Args:
        padded_address (bytes): A 32-byte padded address.

    Returns:
        str: The original Ethereum address as a hex string.
    """

    if isinstance(padded_address, bytes):
        # Convert bytes to hex string without the "0x" prefix
        hex_str = padded_address.hex()
    elif isinstance(padded_address, str):
        # Remove "0x" prefix if present
        hex_str = padded_address[2:] if padded_address.startswith("0x") else padded_address
    else:
        raise TypeError("padded_address must be either bytes or a hex string")

    # Extract the last 40 hex characters (20 bytes) which represent the address
    original_address = hex_str[-40:]
    return "0x" + original_address


def convert_32_byte_array_to_evm_address(buffer: list) -> str:
    if buffer is None:
        return None

    return unpad_address(bytes(buffer).hex())


def convert_32_byte_array_to_solana_address(buffer: list) -> str:
    return base58.b58encode(bytes(buffer)).decode("utf-8")


def log_error(bridge: Bridge, message: str):
    """
    Logs an error message to the console and writes it to a log file.

    :param message: The error message to be logged.
    """
    log_file = "./error_log.log"

    log_to_file(message, log_file)
    log_to_cli(build_log_message_generator(bridge, f"Error written to {log_file}"), CliColor.ERROR)


def log_to_file(message: str, log_file: str):
    """
    Writes an error message to the specified log file with a timestamp.

    :param message: The error message to be logged.
    :param log_file: Path to the log file (default: './error_log.log').
    """
    try:
        # Ensure the logger is configured once
        logger = logging.getLogger(log_file)
        if not logger.handlers:
            handler = logging.FileHandler(log_file)
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s\n")
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.ERROR)

        # Log the error message
        logger.error(message)

    except Exception as e:
        # Fallback in case the logger fails
        with open(log_file, "a") as fallback_log:
            fallback_log.write(f"{datetime.now()} - ERROR - Failed to log error: {e}\n")
            fallback_log.write(f"{datetime.now()} - ERROR - Original message: {message}\n")


class CliColor(Enum):
    INFO = "\033[93m"
    SUCCESS = "\033[92m"
    ERROR = "\033[91m"


def log_to_cli(message: str = "", color: CliColor = CliColor.INFO):
    sys.stdout.write(f"{color.value}{message}\033[0m\n")


def build_log_message(
    start_block: int,
    end_block: int,
    contract: str,
    bridge: Bridge,
    blockchain: str,
    message: str = "",
):
    message = (
        f"Block range {start_block}-{end_block} in {blockchain} in contract {contract} -- {message}"
    )
    message = f"{datetime.now()} - INFO - {bridge.value} - {message}"

    return message


def build_log_message_2(
    start_block: int, end_block: int, bridge: Bridge, blockchain: str, message: str = ""
):
    message = f"Block range {start_block}-{end_block} in {blockchain} -- {message}"
    message = f"{datetime.now()} - INFO - {bridge.value} - {message}"

    return message


def build_log_message_solana(start_sig: str, end_sig: str, bridge: Bridge, message: str = ""):
    short_start = f"{start_sig[:3]}...{start_sig[-3:]}"
    short_end = f"{end_sig[:3]}...{end_sig[-3:]}"
    message = f"Signature range {short_start}-{short_end} in solana -- {message}"
    message = f"{datetime.now()} - INFO - {bridge.value} - {message}"

    return message


def build_log_message_generator(bridge: Bridge, message: str = ""):
    message = f"{datetime.now()} - INFO - {bridge.value} - {message}"

    return message


def load_module(module_name: str):
    return importlib.import_module(module_name)


def load_bridge_config(bridge_name: str) -> dict:
    module = load_module(f"extractor.{bridge_name}.constants")
    return module.BRIDGE_CONFIG


def load_abi(root_dir: str, bridge: Bridge, blockchain, contract_addr: str):
    abi_path = os.path.join(
        root_dir, bridge.value, "ABIs", blockchain, f"{contract_addr.lower()}.json"
    )

    with open(abi_path, "r") as abi_file:
        abi = json.load(abi_file)
        return abi


class CustomException(Exception):
    def __init__(self, classname: str, func_name: str, message: str):
        super().__init__(f"(Class: {classname}) {func_name}: {message}")
