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

    def get_solana_bridge_program_ids(self) -> str:
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

    def handle_transactions(self, transactions: List[Dict[str, Any]]) -> None:
        func_name = "handle_transactions"
        try:
            self.blockchain_transaction_repo.create_all(transactions)
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"Error writing transactions to database: {e}",
            ) from e

    def handle_transaction(self, transaction: Dict[str, Any]) -> None:
        func_name = "handle_transaction"
        try:
            self.blockchain_transaction_repo.create(transaction)
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"Error writing transaction to database: {e}",
            ) from e

    def create_transaction_object(
        self, blockchain: str, tx: Dict[str, Any], timestamp: int
    ) -> None:
        func_name = "create_transaction_object"
        try:
            if blockchain == "solana":
                return {
                    "blockchain": blockchain,
                    "transaction_hash": tx["transaction"]["signatures"][0],
                    "block_number": tx["slot"],
                    "timestamp": timestamp,
                    "from_address": None,
                    "to_address": None,
                    "status": 1 if tx["meta"]["err"] is not None else 0,
                    "input_data": None,
                    "value": None,
                    "fee": tx["meta"]["fee"],
                }
            else:
                input_data = tx["input"] if "input" in tx else None
                if isinstance(input_data, bytes):
                    input_data = input_data.hex()
                elif hasattr(input_data, "hex"):  # HexBytes
                    input_data = input_data.hex()

                # Truncate to 35000 chars if needed
                if input_data and len(input_data) > 35000:
                    input_data = input_data[:35000]

                return {
                    "blockchain": blockchain,
                    "transaction_hash": tx["transactionHash"],
                    "block_number": int(tx["blockNumber"], 0),
                    "timestamp": int(timestamp, 16),
                    "from_address": tx["from"],
                    "to_address": tx["to"],
                    "status": int(tx["status"], 16),
                    "value": int(tx["value"], 16) if "value" in tx else None,
                    "input_data": input_data,
                    "fee": str(int(tx["gasUsed"], 0) * int(tx["effectiveGasPrice"], 0)),
                }
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"Tx Hash: {tx['transactionHash']}: {e}"
                if "transactionHash" in tx
                else f"Tx Signature: {tx['signature']}: {e}",
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
                flattened.update(dict(zip(keys, new_tuple, strict=False)))
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

    def post_processing(self) -> None:
        """
        Placeholder for post-processing tasks.
        This method can be overridden in subclasses to implement specific post-processing logic.
        """
        return None
