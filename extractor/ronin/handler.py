from typing import Any, Dict, List

from config.constants import Bridge
from extractor.base_handler import BaseHandler
from extractor.ronin.constants import BRIDGE_CONFIG
from repository.database import DBSession
from repository.ronin.repository import (
    RoninBlockchainTransactionRepository,
    RoninDepositRequestedRepository,
    RoninTokenDepositedRepository,
    RoninTokenWithdrewRepository,
    RoninWithdrawalRequestedRepository,
)
from rpcs.evm_rpc_client import EvmRPCClient
from utils.utils import CustomException, log_error


class RoninHandler(BaseHandler):
    CLASS_NAME = "RoninHandler"

    def __init__(self, rpc_client: EvmRPCClient, blockchains: list) -> None:
        super().__init__(rpc_client, blockchains)
        self.bridge = Bridge.RONIN

    def get_bridge_contracts_and_topics(self, bridge: str, blockchain: List[str]) -> None:
        return super().get_bridge_contracts_and_topics(
            config=BRIDGE_CONFIG,
            bridge=bridge,
            blockchain=blockchain,
        )

    def bind_db_to_repos(self):
        self.blockchain_transaction_repo = RoninBlockchainTransactionRepository(DBSession)
        self.deposit_requested_repo = RoninDepositRequestedRepository(DBSession)
        self.token_deposited_repo = RoninTokenDepositedRepository(DBSession)
        self.withdrawal_requested_repo = RoninWithdrawalRequestedRepository(DBSession)
        self.token_withdrew_repo = RoninTokenWithdrewRepository(DBSession)

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

    def does_transaction_exist_by_hash(self, transaction_hash: str) -> Any:
        func_name = "does_transaction_exist_by_hash"
        """
        Retrieves a transaction by its hash from the database.

        Args:
            transaction_hash: The hash of the transaction to retrieve.

        Returns:
            The transaction with the given hash.
        """
        try:
            return self.blockchain_transaction_repo.get_transaction_by_hash(transaction_hash)
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"Error reading transaction from database: {e}",
            ) from e

    def handle_events(
        self,
        blockchain: str,
        start_block: int,
        end_block: int,
        contract: str,
        topics: List[str],
        events: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        included_events = []
        for event in events:
            try:
                if (
                    event["topic"]
                    == "0xd7b25068d9dc8d00765254cfb7f5070f98d263c8d68931d937c7362fa738048b"
                ):  # DepositRequested
                    event = self.handle_deposit_requested(blockchain, event)
                elif (
                    event["topic"]
                    == "0x8d20d8121a34dded9035ff5b43e901c142824f7a22126392992c353c37890524"
                ):  # Deposited
                    event = self.handle_tokens_deposited(blockchain, event)
                elif (
                    event["topic"]
                    == "0xf313c253a5be72c29d0deb2c8768a9543744ac03d6b3cafd50cc976f1c2632fc"
                ):  # WithdrawalRequested
                    event = self.handle_withdrawal_requested(blockchain, event)
                elif (
                    event["topic"]
                    == "0x21e88e956aa3e086f6388e899965cef814688f99ad8bb29b08d396571016372d"
                ):  # Withdrew
                    event = self.handle_token_withdrew(blockchain, event)

                if event:
                    included_events.append(event)

            except CustomException as e:
                request_desc = (
                    f"Error processing request: {blockchain}, {start_block}, "
                    f"{end_block}, {contract}, {topics}.\n{e}"
                )
                log_error(self.bridge, request_desc)

        return included_events

    def handle_deposit_requested(self, blockchain, event):
        func_name = "handle_deposit_requested"

        try:
            [receipt, mainchain_data, ronin_data, token_info] = self.extract_objects_from_event(
                event
            )

            if self.deposit_requested_repo.event_exists(receipt["id"]):
                return None

            if token_info["quantity"] == 0:
                return None

            self.deposit_requested_repo.create(
                {
                    "blockchain": "ethereum",
                    "transaction_hash": event["transaction_hash"],
                    "deposit_id": receipt["id"],
                    "kind": receipt["kind"],
                    "depositor": mainchain_data["addr"],
                    "input_token": mainchain_data["tokenAddr"],
                    "recipient": ronin_data["addr"],
                    "output_token": ronin_data["tokenAddr"],
                    "dst_blockchain": "ronin",
                    "token_standard": token_info["erc"],
                    "amount": token_info["quantity"],
                }
            )
            return event
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e

    def handle_tokens_deposited(self, blockchain, event):
        func_name = "handle_tokens_deposited"

        try:
            [receipt, mainchain_data, ronin_data, token_info] = self.extract_objects_from_event(
                event
            )

            if self.token_deposited_repo.event_exists(receipt["id"]):
                return None

            if token_info["quantity"] == 0:
                return None

            self.token_deposited_repo.create(
                {
                    "blockchain": "ronin",
                    "transaction_hash": event["transaction_hash"],
                    "deposit_id": receipt["id"],
                    "kind": receipt["kind"],
                    "src_blockchain": "ethereum",
                    "depositor": mainchain_data["addr"],
                    "input_token": mainchain_data["tokenAddr"],
                    "recipient": ronin_data["addr"],
                    "output_token": ronin_data["tokenAddr"],
                    "token_standard": token_info["erc"],
                    "amount": token_info["quantity"],
                }
            )

            return event
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e

    def handle_withdrawal_requested(self, blockchain, event):
        func_name = "handle_withdrawal_requested"

        try:
            [receipt, mainchain_data, ronin_data, token_info] = self.extract_objects_from_event(
                event
            )

            if self.withdrawal_requested_repo.event_exists(receipt["id"]):
                return None

            if token_info["quantity"] == 0:
                return None

            self.withdrawal_requested_repo.create(
                {
                    "blockchain": "ronin",
                    "transaction_hash": event["transaction_hash"],
                    "withdrawal_id": receipt["id"],
                    "kind": receipt["kind"],
                    "withdrawer": ronin_data["addr"],
                    "input_token": ronin_data["tokenAddr"],
                    "dst_blockchain": "ethereum",
                    "recipient": mainchain_data["addr"],
                    "output_token": mainchain_data["tokenAddr"],
                    "token_standard": token_info["erc"],
                    "amount": token_info["quantity"],
                }
            )

            return event
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e

    def handle_token_withdrew(self, blockchain, event):
        func_name = "handle_token_withdrew"

        try:
            [receipt, mainchain_data, ronin_data, token_info] = self.extract_objects_from_event(
                event
            )

            if self.token_withdrew_repo.event_exists(receipt["id"]):
                return None

            if token_info["quantity"] == 0:
                return None

            self.token_withdrew_repo.create(
                {
                    "blockchain": "ethereum",
                    "transaction_hash": event["transaction_hash"],
                    "withdrawal_id": receipt["id"],
                    "kind": receipt["kind"],
                    "src_blockchain": "ronin",
                    "withdrawer": ronin_data["addr"],
                    "input_token": ronin_data["tokenAddr"],
                    "recipient": mainchain_data["addr"],
                    "output_token": mainchain_data["tokenAddr"],
                    "token_standard": token_info["erc"],
                    "amount": token_info["quantity"],
                }
            )

            return event
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e

    def extract_objects_from_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extracts the objects from the event.

        Args:
            event: The event to extract the objects from.

        Returns:
            The extracted objects.
        """
        return [
            event["receipt"],
            event["receipt"]["mainchain"],
            event["receipt"]["ronin"],
            event["receipt"]["info"],
        ]
