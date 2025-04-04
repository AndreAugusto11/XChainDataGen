from abc import ABC, abstractmethod
from typing import Any, Dict, List

from annotated_types import T
from sqlalchemy.orm import scoped_session, sessionmaker

from repository.database import engine
from utils.rpc_utils import RPCClient
from utils.utils import CustomException, convert_bin_to_hex


class BaseHandler(ABC):

    def __init__(self, rpc_client: RPCClient):
        self.rpc_client = rpc_client
        self.bind_db_to_repos()

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
    def get_bridge_contracts_and_topics(self, blockchain: str) -> List[T]:
        pass

    @abstractmethod
    def bind_db_to_repos(self) -> None:
        pass

    @abstractmethod
    def handle_transactions(self, transactions: List[Dict[str, Any]]) -> None:
        pass

    def create_transaction_object(self, blockchain: str, tx_receipt: Dict[str, Any], block: Dict[str, Any]) -> None:
        func_name = "create_transaction_object"
        try:
            return {
                        "blockchain": blockchain,
                        "transaction_hash": tx_receipt["transactionHash"],
                        "block_number": int(tx_receipt["blockNumber"], 0),
                        "timestamp": int(block["timestamp"], 16),
                        "from_address": tx_receipt["from"],
                        "to_address": tx_receipt["to"],
                        "status": int(tx_receipt["status"], 16),
                        "fee": str(
                            int(tx_receipt["gasUsed"], 0)
                            * int(tx_receipt["effectiveGasPrice"], 0)
                        ),
                    }
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"Tx Hash: {tx_receipt['transactionHash']}: {e}",
            )

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
                        (
                            convert_bin_to_hex(val)
                            if isinstance(val, (bytes, bytearray))
                            else val
                        ),
                    )
                flattened.update(dict(zip(keys, new_tuple)))
            else:
                flattened[key] = value
        return flattened
