from abc import ABC, abstractmethod
from typing import Any, Dict, List

from annotated_types import T

from config.constants import BLOCKCHAIN_IDS
from rpcs.evm_rpc_client import EvmRPCClient
from utils.utils import CustomException, convert_bin_to_hex


class BaseHandler(ABC):
    CLASS_NAME = "BaseHandler"

    def __init__(self, rpc_client: EvmRPCClient, blockchains: List[str]):
        self.rpc_client = rpc_client
        self.bind_db_to_repos()

        # Map of blockchains that are involved in the analysis, used to filter events.
        self.counterPartyBlockchainsMap = {b: True for b in blockchains}

    def get_solana_bridge_program_id(self) -> str:
        """
        Returns the program ID of the Solana bridge.
        This is a placeholder method and should be overridden in subclasses if needed.
        """
        raise NotImplementedError("This method should be implemented in subclasses.")

    @abstractmethod
    def handle_events(
        self,
        blockchain: str,
        start_block: int,
        end_block: int,
        contract: str,
        topics: List[str],
        event: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_bridge_contracts_and_topics(
        self, config: Dict, bridge: str, blockchain: List[str]
    ) -> List[T]:
        """
        Validates the mapping between the bridge and the blockchains.

        Args:
            bridge: The bridge to validate.
            blockchain: The blockchain to validate.
        """
        if blockchain not in config["blockchains"]:
            raise ValueError(f"Blockchain {blockchain} not supported for bridge {bridge}.")

        return config["blockchains"][blockchain]

    @abstractmethod
    def bind_db_to_repos(self) -> None:
        """
        This function is needed to rebind the repositories to new sessions when we have to rollback
        failed transactions (e.g., because of unique constraints in the tables) and create a new
        session. Binds the database session to the repository instances used in the handler.
        """
        pass

    @abstractmethod
    def handle_transactions(self, transactions: List[Dict[str, Any]]) -> None:
        pass

    def create_transaction_object(
        self, blockchain: str, tx_receipt: Dict[str, Any], timestamp: int
    ) -> None:
        func_name = "create_transaction_object"
        try:
            if blockchain == "solana":
                return {
                    "blockchain": blockchain,
                    "transaction_hash": tx_receipt["transaction"]["signatures"][0],
                    "block_number": tx_receipt["slot"],
                    "timestamp": timestamp,
                    "from_address": None,
                    "to_address": None,
                    "status": 1 if tx_receipt["meta"]["err"] is not None else 0,
                    "value": None,
                    "fee": tx_receipt["meta"]["fee"],
                }
            else:
                return {
                    "blockchain": blockchain,
                    "transaction_hash": tx_receipt["transactionHash"],
                    "block_number": int(tx_receipt["blockNumber"], 0),
                    "timestamp": int(timestamp, 16),
                    "from_address": tx_receipt["from"],
                    "to_address": tx_receipt["to"],
                    "status": int(tx_receipt["status"], 16),
                    "value": int(tx_receipt["value"], 16) if "value" in tx_receipt else None,
                    "fee": str(
                        int(tx_receipt["gasUsed"], 0) * int(tx_receipt["effectiveGasPrice"], 0)
                    ),
                }
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"Tx Hash: {tx_receipt['transactionHash']}: {e}"
                if "transactionHash" in tx_receipt
                else f"Tx Signature: {tx_receipt['signature']}: {e}",
            ) from e

    @abstractmethod
    def does_transaction_exist_by_hash(self, transaction_hash: str) -> Any:
        pass

    @staticmethod
    def flatten_object(obj):
        flattened = {}
        for key, value in obj.items():
            if key.startswith("(") and key.endswith(")"):  # Handle tuple-string keys
                keys = key.strip("()").split(",")
                new_tuple = ()
                for val in value:
                    new_tuple += (
                        (convert_bin_to_hex(val) if isinstance(val, (bytes, bytearray)) else val),
                    )
                flattened.update(dict(zip(keys, new_tuple)))
            else:
                flattened[key] = value
        return flattened

    def convert_id_to_blockchain_name(self, id: str, blockchain_ids=BLOCKCHAIN_IDS) -> str | None:
        func_name = "convert_id_to_blockchain_name"

        id = str(id)

        if id in blockchain_ids:
            blockchain_name = blockchain_ids[id]["name"]
            # If the blockchain name is not in the list of blockchains specified by the user,
            # return None
            if self.counterPartyBlockchainsMap.get(blockchain_name):
                return blockchain_ids[id]["name"]

        # If the blockchain ID is not found, log an error and return None
        CustomException(self.CLASS_NAME, func_name, f"Blockchain with ID {id} not included")
        # log_to_file(e, "data/out_of_scope_blockchains.log")
        return None
