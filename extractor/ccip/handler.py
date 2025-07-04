from typing import Any, Dict, List

from config.constants import Bridge
from extractor.base_handler import BaseHandler
from extractor.ccip.constants import BRIDGE_CONFIG
from repository.ccip.repository import (
    CCIPBlockchainTransactionRepository,
    CCIPExecutionStateChangedRepository,
    CCIPSendRequestedRepository,
)
from repository.database import DBSession
from rpcs.evm_rpc_client import EvmRPCClient
from utils.utils import CustomException, log_error, unpad_address


class CcipHandler(BaseHandler):
    CLASS_NAME = "CcipHandler"

    def __init__(self, rpc_client: EvmRPCClient, blockchains: list) -> None:
        super().__init__(rpc_client, blockchains)
        self.bridge = Bridge.CCIP

    def get_bridge_contracts_and_topics(self, bridge: str, blockchain: List[str]) -> None:
        return super().get_bridge_contracts_and_topics(
            config=BRIDGE_CONFIG,
            bridge=bridge,
            blockchain=blockchain,
        )

    def bind_db_to_repos(self):
        self.blockchain_transaction_repo = CCIPBlockchainTransactionRepository(DBSession)
        self.ccip_send_requested_repo = CCIPSendRequestedRepository(DBSession)
        self.ccip_execution_state_changed_repo = CCIPExecutionStateChangedRepository(DBSession)

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
                    == "0xd0c3c799bf9e2639de44391e7f524d229b2b55f5b1ea94b2bf7da42f7243dddd"
                ):  # CCIPSendRequested
                    event = self.handle_send_requested(blockchain, event)
                elif (
                    event["topic"]
                    == "0xd4f851956a5d67c3997d1c9205045fef79bae2947fdee7e9e2641abc7391ef65"
                ):  # MessageReceived
                    event = self.handle_execution_state_changed(blockchain, event)

                if event:
                    included_events.append(event)

            except CustomException as e:
                request_desc = (
                    f"Error processing request: {blockchain}, {start_block}, "
                    f"{end_block}, {contract}, {topics}.\n{e}"
                )
                log_error(self.bridge, request_desc)

        return included_events

    def handle_send_requested(self, blockchain, event):
        func_name = "handle_send_requested"

        message = event["message"]

        try:
            if self.ccip_send_requested_repo.event_exists(message["messageId"]):
                return None

            if message["data"] != "":
                return None

            input_token = None
            amount = None
            output_token = None
            if message["tokenAmounts"] != []:
                if len(message["tokenAmounts"]) > 1:
                    log_error(self.bridge, f"More than one token amount in message: {message}")
                    return None

                input_token = message["tokenAmounts"][0]["token"]
                amount = message["tokenAmounts"][0]["amount"]

                output_token = unpad_address(message["sourceTokenData"][0][512:576])

            self.ccip_send_requested_repo.create(
                {
                    "blockchain": blockchain,
                    "transaction_hash": event["transaction_hash"],
                    "nonce": message["nonce"],
                    "sender": unpad_address(message["sender"]).lower(),
                    "receiver": unpad_address(message["receiver"]).lower(),
                    "sequence_number": message["sequenceNumber"],
                    "gas_limit": message["gasLimit"],
                    "strict": message["strict"],
                    "fee_token": unpad_address(message["feeToken"]).lower(),
                    "fee_token_amount": message["feeTokenAmount"],
                    "input_token": input_token,
                    "amount": amount,
                    "output_token": output_token,
                    "message_id": message["messageId"],
                }
            )
            return event
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e

    def handle_execution_state_changed(self, blockchain, event):
        func_name = "handle_execution_state_changed"

        try:
            if self.ccip_execution_state_changed_repo.event_exists(event["messageId"]):
                return None

            self.ccip_execution_state_changed_repo.create(
                {
                    "blockchain": blockchain,
                    "transaction_hash": event["transaction_hash"],
                    "sequence_number": event["sequenceNumber"],
                    "message_id": event["messageId"],
                    "state": event["state"],
                    "return_data": event["returnData"],
                }
            )

            return event
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e
