import time
from itertools import cycle

import requests
import yaml

from config.constants import MAX_NUM_THREADS_EXTRACTOR, RPCS_CONFIG_FILE
from utils.utils import CustomException, convert_blockchain_into_alchemy_id, load_alchemy_api_key


class RPCClient:
    CLASS_NAME = "RPCClient"

    def __init__(self, bridge, config_file: str = RPCS_CONFIG_FILE):
        self.bridge = bridge
        self.blockchains = self.load_config(config_file)
        self.rpc_mapping = self.initialize_rpc_mapping()
        self.rpc_sizes = {
            blockchain["name"]: len(blockchain["rpcs"]) for blockchain in self.blockchains
        }

    def max_threads_per_blockchain(self, blockchain_name: str) -> int:
        func_name = "max_threads_per_blockchain"
        for blockchain in self.blockchains:
            if blockchain["name"] == blockchain_name:
                return min(MAX_NUM_THREADS_EXTRACTOR, len(blockchain["rpcs"]))
        raise CustomException(
            self.CLASS_NAME,
            func_name,
            f"blockchain {blockchain_name} not found in configuration.",
        )

    @staticmethod
    def load_config(config_file: str) -> list:
        """Load blockchain configurations from a JSON file."""
        with open(config_file, "r") as file:
            return yaml.safe_load(file)["blockchains"]

    def initialize_rpc_mapping(self):
        """Initialize a round-robin cycle for each blockchain's RPC endpoints."""
        rpc_mapping = {}
        for blockchain in self.blockchains:
            blockchain_name = blockchain["name"]
            rpc_mapping[blockchain_name] = cycle(blockchain["rpcs"])
        return rpc_mapping

    def get_next_rpc(self, blockchain_name: str) -> str:
        """Get the next RPC URL in the round-robin cycle for a blockchain."""
        func_name = "get_next_rpc"
        if blockchain_name not in self.rpc_mapping:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"blockchain {blockchain_name} not found in configuration.",
            )

        next_rpc = next(self.rpc_mapping[blockchain_name])
        return next_rpc

    def get_random_rpc(self, blockchain) -> str:
        """Get a random RPC URL for Ethereum."""
        return self.get_next_rpc(blockchain)

    def get_logs_emitted_by_contract(
        self,
        blockchain: str,
        contract: str,
        topics: list,
        start_block: str,
        end_block: str,
    ) -> list:
        method = "eth_getLogs"
        params = [
            {
                "fromBlock": hex(start_block),
                "toBlock": hex(end_block),
                "topics": [topics],
                "address": contract,
            }
        ]

        rpc = self.get_next_rpc(blockchain)
        response = self.make_request(rpc, blockchain, method, params)

        return response["result"] if response else []

    def make_request(self, rpc_url: str, blockchain_name: str, method: str, params: list) -> dict:
        """Make an RPC request using the next available endpoint in the round-robin."""
        func_name = "make_request"
        num_rpcs = self.rpc_sizes[blockchain_name]

        try:
            backoff = 1
            while True:
                tried_rpcs = {}
                while len(tried_rpcs) < num_rpcs:
                    payload = {
                        "id": 1,
                        "jsonrpc": "2.0",
                        "method": method,
                        "params": params,
                    }
                    try:
                        response = requests.post(rpc_url, json=payload, timeout=10)
                        response.raise_for_status()

                        if response.json() is None or response.json()["result"] is None:
                            raise Exception()

                        return response.json()
                    except Exception as e:
                        tried_rpcs[rpc_url] = e
                        rpc_url = self.get_next_rpc(blockchain_name)
                        # ignore the exception and try the next RPC endpoint
                        pass

                # if we have tried all RPC endpoints and none of them worked, back off
                # exponentially and try again all endpoints. Only return once we have
                # a correct response
                time.sleep(backoff)
                backoff *= 2

        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                (
                    f"Failed to make RPC request to {blockchain_name}, method {method}, "
                    f"params {params}. Error: {e}"
                ),
            ) from e

    def process_transaction(self, blockchain: str, tx_hash: str, block_number: str) -> dict:
        import concurrent.futures

        method_receipt = "eth_getTransactionReceipt"
        params_receipt = [tx_hash]

        method_block = "eth_getBlockByNumber"
        params_block = [block_number, True]

        rpc = self.get_next_rpc(blockchain)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_receipt = executor.submit(
                self.make_request, rpc, blockchain, method_receipt, params_receipt
            )
            future_block = executor.submit(
                self.make_request, rpc, blockchain, method_block, params_block
            )

            response_receipt = future_receipt.result()
            response_block = future_block.result()

        return response_receipt["result"] if response_receipt else {}, response_block[
            "result"
        ] if response_block else {}

    def get_transaction_receipt(self, blockchain: str, tx_hash: str) -> dict:
        method = "eth_getTransactionReceipt"
        params = [tx_hash]

        rpc = self.get_next_rpc(blockchain)
        response = self.make_request(rpc, blockchain, method, params)

        return response["result"] if response else {}

    def get_transaction_by_hash(self, blockchain: str, tx_hash: str) -> dict:
        method = "eth_getTransactionByHash"
        params = [tx_hash]

        rpc = self.get_next_rpc(blockchain)
        response = self.make_request(rpc, blockchain, method, params)

        return response["result"] if response else {}

    def get_transaction_trace(self, blockchain: str, tx_hash: str) -> dict:
        method = "trace_transaction"
        params = [tx_hash]

        rpc = self.get_next_rpc(blockchain)
        response = self.make_request(rpc, blockchain, method, params)

        return response["result"] if response else {}

    def debug_transaction(self, blockchain: str, tx_hash: str, extra_params: str) -> dict:
        method = "debug_traceTransaction"
        params = [tx_hash, extra_params] if extra_params else [tx_hash]

        rpc = self.get_next_rpc(blockchain)
        response = self.make_request(rpc, blockchain, method, params)

        return response["result"] if response else {}

    def get_block(self, blockchain: str, block_number: str) -> dict:
        method = "eth_getBlockByNumber"
        params = [block_number, True]

        rpc = self.get_next_rpc(blockchain)
        response = self.make_request(rpc, blockchain, method, params)

        return response["result"] if response else {}

    @staticmethod
    def plain_request(rpc, method, params):
        func_name = "plain_request"
        response = requests.post(
            rpc,
            headers={"Content-Type": "application/json", "Accept": "application/json"},
            json={"id": 1, "jsonrpc": "2.0", "method": method, "params": params},
        )

        if response.status_code != 200:
            raise CustomException(
                "",
                func_name,
                f"RPC request failed with status code {response.status_code}",
            )

        return response.json()

    @staticmethod
    def get_token_metadata(blockchain: str, contract: str) -> dict:
        func_name = "get_token_metadata"

        blockchain_id = convert_blockchain_into_alchemy_id(blockchain)

        url = f"https://{blockchain_id}-mainnet.g.alchemy.com/v2/{load_alchemy_api_key()}/"

        payload = {
            "id": 1,
            "jsonrpc": "2.0",
            "method": "alchemy_getTokenMetadata",
            "params": [contract],
        }
        headers = {"accept": "application/json", "content-type": "application/json"}

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code != 200:
            raise CustomException(
                "",
                func_name,
                f"Alchemy request failed with status code {response.status_code}",
            )

        return response.json()["result"] if response else {}

    @staticmethod
    def get_token_prices_by_symbol_or_address(
        start_ts: int,
        end_ts: int,
        symbol: str = None,
        blockchain: str = None,
        token_address: str = None,
    ) -> dict:
        func_name = "get_token_prices_by_symbol_or_address"

        payload = {}

        if not symbol:
            if blockchain is None or token_address is None:
                raise CustomException(
                    "",
                    func_name,
                    "Either symbol or blockchain and token_address must be provided.",
                )

            blockchain_id = convert_blockchain_into_alchemy_id(blockchain)

            if blockchain_id is None:
                return {}

            payload = {
                "network": f"{blockchain_id}-mainnet",
                "address": token_address,
                "startTime": start_ts,
                "endTime": end_ts,
                "interval": "1d",
            }
        else:
            if blockchain is not None or token_address is not None:
                raise CustomException(
                    "",
                    func_name,
                    "Either symbol or blockchain and token_address must be provided.",
                )

            payload = {
                "symbol": symbol,
                "startTime": start_ts,
                "endTime": end_ts,
                "interval": "1d",
            }

        url = f"https://api.g.alchemy.com/prices/v1/{load_alchemy_api_key()}/tokens/historical"

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
        }

        response = requests.post(url, json=payload, headers=headers)

        for i in range(5):
            try:
                response = requests.post(url, json=payload, headers=headers)
                response.raise_for_status()
                return response.json() if response else {}
            except requests.exceptions.RequestException:
                # if response.text contains "token not found" return {}
                if "Token not found" in response.text:
                    return {}

                if i < 4:
                    time.sleep(2**i)  # Exponential backoff
                else:
                    return None

        return response.json() if response else {}
