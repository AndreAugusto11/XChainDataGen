import time
from abc import ABC, abstractmethod
from itertools import cycle

import requests
import yaml

from config.constants import (
    BRIDGE_NEEDS_TRANSACTION_BY_HASH_RPC_METHOD,
    MAX_NUM_THREADS_EXTRACTOR,
    RPCS_CONFIG_FILE,
)
from utils.utils import CustomException, load_solana_api_key, log_error


class RPCClient(ABC):
    CLASS_NAME = "RPCClient"

    def __init__(self, bridge, config_file: str = RPCS_CONFIG_FILE):
        self.bridge = bridge
        self.blockchains = self.load_config(config_file)
        self.rpc_mapping = self.initialize_rpc_mapping()
        self.rpc_sizes = {
            blockchain["name"]: len(blockchain["rpcs"]) for blockchain in self.blockchains
        }
        self.requires_transaction_by_hash_rpc_call = BRIDGE_NEEDS_TRANSACTION_BY_HASH_RPC_METHOD[
            bridge
        ]  # noqa: E501

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

                    if blockchain_name == "solana":
                        headers = {
                            "Content-Type": "application/json",
                            "Accept": "application/json",
                            "Authorization": f"Bearer {load_solana_api_key()}",
                        }
                    else:
                        headers = {
                            "Content-Type": "application/json",
                            "Accept": "application/json",
                        }
                    try:
                        response = requests.post(rpc_url, json=payload, headers=headers, timeout=10)
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
                log_error(
                    self.bridge,
                    (
                        f"Failed to make RPC request to {blockchain_name}, method {method}, "
                        f"params {params}. Tried RPCs: {tried_rpcs}. Retrying with backoff ",
                        f"{backoff} seconds.",
                    ),
                )
                backoff = (backoff * 2) if backoff < 30 else 30

        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                (
                    f"Failed to make RPC request to {blockchain_name}, method {method}, "
                    f"params {params}. Error: {e}"
                ),
            ) from e

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

    @abstractmethod
    def process_transaction(self, blockchain: str, tx_hash: str, block_number: str) -> dict:
        pass
