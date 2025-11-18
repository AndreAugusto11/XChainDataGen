from typing import Any, Dict, List

from config.constants import Bridge
from extractor.across.constants import BRIDGE_CONFIG
from extractor.base_handler import BaseHandler
from repository.across.repository import (
    AcrossBlockchainTransactionRepository,
    AcrossFilledRelayRepository,
    AcrossFundsDepositedRepository,
    AcrossRelayerRefundRepository,
)
from repository.database import DBSession
from rpcs.evm_rpc_client import EvmRPCClient
from utils.utils import CustomException, convert_bin_to_hex, log_error, unpad_address


class AcrossHandler(BaseHandler):
    CLASS_NAME = "AcrossHandler"

    def __init__(self, rpc_client: EvmRPCClient, blockchains: list) -> None:
        super().__init__(rpc_client, blockchains)
        self.bridge = Bridge.ACROSS

    def get_bridge_contracts_and_topics(self, bridge: str, blockchain: List[str]) -> None:
        return super().get_bridge_contracts_and_topics(
            config=BRIDGE_CONFIG,
            bridge=bridge,
            blockchain=blockchain,
        )

    def bind_db_to_repos(self):
        self.blockchain_transaction_repo = AcrossBlockchainTransactionRepository(DBSession)
        self.across_filled_relay_repo = AcrossFilledRelayRepository(DBSession)
        self.across_funds_deposited_repo = AcrossFundsDepositedRepository(DBSession)
        self.across_relayer_refund_repo = AcrossRelayerRefundRepository(DBSession)

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
                    == "0x32ed1a409ef04c7b0227189c3a103dc5ac10e775a15b785dcc510201f7c25ad3"
                ):  # FundsDeposited
                    event = self.handle_funds_deposited(blockchain, event)
                elif (
                    event["topic"]
                    == "0x44b559f101f8fbcc8a0ea43fa91a05a729a5ea6e14a7c75aa750374690137208"
                ):  # FilledRelay
                    event = self.handle_filled_relay(blockchain, event)
                elif (
                    event["topic"]
                    == "0xf4ad92585b1bc117fbdd644990adf0827bc4c95baeae8a23322af807b6d0020e"
                ):  # ExecutedRelayerRefundRoot
                    event = self.handle_relayer_refund(blockchain, event)

                if event:
                    included_events.append(event)

            except CustomException as e:
                request_desc = (
                    f"Error processing request: {blockchain}, {start_block}, "
                    f"{end_block}, {contract}, {topics}.\n{e}"
                )
                log_error(self.bridge, request_desc)

        return included_events

    def handle_funds_deposited(self, blockchain, event):
        func_name = "handle_funds_deposited"

        destination_chain = self.convert_id_to_blockchain_name(event["destinationChainId"])

        if destination_chain is None:
            return None

        try:
            if self.across_funds_deposited_repo.event_exists(str(event["depositId"])):
                return None

            self.across_funds_deposited_repo.create(
                {
                    "blockchain": blockchain,
                    "transaction_hash": event["transaction_hash"],
                    "destination_chain": destination_chain,
                    "deposit_id": event["depositId"],
                    "depositor": unpad_address(event["depositor"]),
                    "input_token": unpad_address(event["inputToken"]),
                    "output_token": unpad_address(event["outputToken"]),
                    "input_amount": str(event["inputAmount"]),
                    "output_amount": str(event["outputAmount"]),
                    "quote_timestamp": event["quoteTimestamp"],
                    "fill_deadline": event["fillDeadline"],
                    "exclusivity_deadline": event["exclusivityDeadline"],
                    "recipient": unpad_address(event["recipient"]),
                    "exclusive_relayer": unpad_address(event["exclusiveRelayer"]),
                    "message": event["message"],
                }
            )
            return event
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e

    def handle_filled_relay(self, blockchain, event):
        func_name = "handle_filled_relay"

        origin_chain = self.convert_id_to_blockchain_name(event["originChainId"])
        repayment_chain = self.convert_id_to_blockchain_name(event["repaymentChainId"])

        if repayment_chain is None or origin_chain is None:
            return None

        try:
            if self.across_filled_relay_repo.event_exists(str(event["depositId"])):
                return None

            self.across_filled_relay_repo.create(
                {
                    "blockchain": blockchain,
                    "transaction_hash": event["transaction_hash"],
                    "src_chain": origin_chain,
                    "deposit_id": str(event["depositId"]),
                    "relayer": unpad_address(event["relayer"]),
                    "input_token": unpad_address(event["inputToken"]),
                    "output_token": unpad_address(event["outputToken"]),
                    "input_amount": str(event["inputAmount"]),
                    "output_amount": str(event["outputAmount"]),
                    "repayment_chain": repayment_chain,
                    "fill_deadline": event["fillDeadline"],
                    "exclusivity_deadline": event["exclusivityDeadline"],
                    "exclusive_relayer": unpad_address(event["exclusiveRelayer"]),
                    "depositor": unpad_address(event["depositor"]),
                    "recipient": unpad_address(event["recipient"]),
                    "message_hash": event["messageHash"],
                    "updated_recipient": unpad_address(
                        event["relayExecutionInfo"]["updatedRecipient"]
                    ),
                    "updated_message_hash": convert_bin_to_hex(
                        event["relayExecutionInfo"]["updatedMessageHash"]
                    ),
                    "updated_output_amount": str(
                        event["relayExecutionInfo"]["updatedOutputAmount"]
                    ),
                    "fill_type": event["relayExecutionInfo"]["fillType"],
                }
            )

            return event
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e

    def handle_relayer_refund(self, blockchain, event):
        func_name = "relayer_refund"

        for i in range(len(event["refundAmounts"])):
            try:
                if self.across_relayer_refund_repo.event_exists(
                    event["transaction_hash"],
                    str(event["amountToReturn"]),
                    str(event["refundAmounts"][i]),
                    event["l2TokenAddress"],
                    event["refundAddresses"][i],
                ):
                    continue

                self.across_relayer_refund_repo.create(
                    {
                        "blockchain": blockchain,
                        "transaction_hash": event["transaction_hash"],
                        "root_bundle_id": event["rootBundleId"],
                        "amount_to_return": str(event["amountToReturn"]),
                        "refund_amount": str(event["refundAmounts"][i]),
                        "l2_token_address": event["l2TokenAddress"],
                        "refund_address": event["refundAddresses"][i],
                        "caller": event["caller"],
                    }
                )
            except Exception as e:
                raise CustomException(
                    self.CLASS_NAME,
                    func_name,
                    f"{blockchain} - Tx Hash: {event['transaction_hash']}. Error writing to DB:{e}",
                ) from e

        return event
