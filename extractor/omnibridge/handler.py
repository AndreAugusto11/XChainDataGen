from typing import Any, Dict, List

from eth_utils import keccak

from config.constants import Bridge
from extractor.base_handler import BaseHandler
from extractor.omnibridge.constants import BRIDGE_CONFIG
from repository.database import DBSession
from repository.omnibridge.repository import (
    OmnibridgeAffirmationCompletedRepository,
    OmnibridgeBlockchainTransactionRepository,
    OmnibridgeRelayedMessageRepository,
    OmnibridgeSignedForAffirmationRepository,
    OmnibridgeSignedForUserRequestRepository,
    OmnibridgeTokensBridgedRepository,
    OmnibridgeTokensBridgingInitiatedRepository,
    OmnibridgeUserRequestForAffirmationRepository,
    OmnibridgeUserRequestForSignatureRepository,
)
from rpcs.evm_rpc_client import EvmRPCClient
from utils.utils import CustomException, log_error


class OmnibridgeHandler(BaseHandler):
    CLASS_NAME = "OmnibridgeHandler"

    def __init__(self, rpc_client: EvmRPCClient, blockchains: list) -> None:
        super().__init__(rpc_client, blockchains)
        self.bridge = Bridge.OMNIBRIDGE

    def get_bridge_contracts_and_topics(self, bridge: str, blockchain: List[str]) -> None:
        return super().get_bridge_contracts_and_topics(
            config=BRIDGE_CONFIG,
            bridge=bridge,
            blockchain=blockchain,
        )

    def bind_db_to_repos(self):
        self.blockchain_transaction_repo = OmnibridgeBlockchainTransactionRepository(DBSession)
        self.tokens_bridged_repo = OmnibridgeTokensBridgedRepository(DBSession)
        self.tokens_bridging_initiated_repo = OmnibridgeTokensBridgingInitiatedRepository(DBSession)
        self.relayed_message_repo = OmnibridgeRelayedMessageRepository(DBSession)
        self.signed_for_user_request_repo = OmnibridgeSignedForUserRequestRepository(DBSession)
        self.signed_for_affirmation_repo = OmnibridgeSignedForAffirmationRepository(DBSession)
        self.user_request_for_signature_repo = OmnibridgeUserRequestForSignatureRepository(
            DBSession
        )
        self.affirmation_completed_repo = OmnibridgeAffirmationCompletedRepository(DBSession)
        self.user_request_for_affirmation_repo = OmnibridgeUserRequestForAffirmationRepository(
            DBSession
        )

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
                    == "0x59a9a8027b9c87b961e254899821c9a276b5efc35d1f7409ea4f291470f1629a"
                ):  # TokensBridgingInitiated
                    event = self.handle_tokens_bridging_initiated(blockchain, event)
                elif (
                    event["topic"]
                    == "0x9afd47907e25028cdaca89d193518c302bbb128617d5a992c5abd45815526593"
                ):  # TokensBridged
                    event = self.handle_tokens_bridged(blockchain, event)
                elif (
                    event["topic"]
                    == "0x1d491a427d1f8cc0d447496f300fac39f7306122481d8e663451eb268274146b"
                ):  # UserRequestForAffirmation (address recipient, uint256 value)
                    event = self.handle_user_request_for_affirmation(blockchain, event)
                elif (
                    event["topic"]
                    == "0x482515ce3d9494a37ce83f18b72b363449458435fafdd7a53ddea7460fe01b58"
                ):  # UserRequestForAffirmation (index_topic_1 bytes32 messageId, bytes encodedData)
                    event = self.handle_user_request_for_affirmation(blockchain, event)
                elif (
                    event["topic"]
                    == "0x4ab7d581336d92edbea22636a613e8e76c99ac7f91137c1523db38dbfb3bf329"
                ):  # RelayedMessage
                    event = self.handle_relayed_message(blockchain, event)
                elif (
                    event["topic"]
                    == "0x127650bcfb0ba017401abe4931453a405140a8fd36fece67bae2db174d3fdd63"
                ):  # UserRequestForSignature (address recipient, uint256 value)
                    event = self.handle_user_request_for_signature(blockchain, event)
                elif (
                    event["topic"]
                    == "0x520d2afde79cbd5db58755ac9480f81bc658e5c517fcae7365a3d832590b0183"
                ):  # UserRequestForSignature (index_topic_1 bytes32 messageId, bytes encodedData)
                    event = self.handle_user_request_for_signature(blockchain, event)
                elif (
                    event["topic"]
                    == "0xbf06885f40778f5ccfb64497d3f92ce568ddaedb7e2fb4487f72690418cf8e4c"
                ):  # SignedForUserRequest
                    event = self.handle_signed_for_user_request(blockchain, event)
                elif (
                    event["topic"]
                    == "0x5df9cc3eb93d8a9a481857a3b70a8ca966e6b80b25cf0ee2cce180ec5afa80a1"
                ):  # SignedForAffirmation (index_topic_1 address signer, bytes32 messageHash)
                    event = self.handle_signed_for_affirmation(blockchain, event)
                elif (
                    event["topic"]
                    == "0x5df9cc3eb93d8a9a481857a3b70a8ca966e6b80b25cf0ee2cce180ec5afa80a1"
                ):  # SignedForAffirmation (index_topic_1 address signer, bytes32 transactionHash)
                    event = self.handle_signed_for_affirmation(blockchain, event)
                elif (
                    event["topic"]
                    == "0x6fc115a803b8703117d9a3956c5a15401cb42401f91630f015eb6b043fa76253"
                ):  # AffirmationCompleted
                    event = self.handle_affirmation_completed(blockchain, event)

                if event:
                    included_events.append(event)

            except CustomException as e:
                request_desc = (
                    f"Error processing request: {blockchain}, {start_block}, "
                    f"{end_block}, {contract}, {topics}.\n{e}"
                )
                log_error(self.bridge, request_desc)

        return included_events

    def handle_tokens_bridging_initiated(self, blockchain, event):
        func_name = "handle_tokens_bridging_initiated"

        try:
            self.tokens_bridging_initiated_repo.create(
                {
                    "blockchain": blockchain,
                    "transaction_hash": event["transaction_hash"],
                    "token": event["token"],
                    "sender": event["sender"],
                    "value": str(event["value"]),
                    "message_id": event["messageId"],
                }
            )
            return event
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e

    def handle_tokens_bridged(self, blockchain, event):
        func_name = "handle_tokens_bridged"

        try:
            self.tokens_bridged_repo.create(
                {
                    "blockchain": blockchain,
                    "transaction_hash": event["transaction_hash"],
                    "token": event["token"],
                    "recipient": event["recipient"],
                    "value": str(event["value"]),
                    "message_id": event["messageId"],
                }
            )
            return event
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e

    def handle_user_request_for_affirmation(self, blockchain, event):
        func_name = "handle_user_request_for_affirmation"

        try:
            self.user_request_for_affirmation_repo.create(
                {
                    "blockchain": blockchain,
                    "transaction_hash": event["transaction_hash"],
                    "message_id": event["messageId"] if "messageId" in event else None,
                    "encoded_data": event["encodedData"] if "encodedData" in event else None,
                    "value": str(event["value"]) if "value" in event else None,
                    "recipient": event["recipient"] if "recipient" in event else None,
                }
            )
            return event
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e

    def handle_user_request_for_signature(self, blockchain, event):
        func_name = "handle_user_request_for_signature"

        try:
            self.user_request_for_signature_repo.create(
                {
                    "blockchain": blockchain,
                    "transaction_hash": event["transaction_hash"],
                    "message_id": event["messageId"] if "messageId" in event else None,
                    "encoded_data": event["encodedData"] if "encodedData" in event else None,
                    "encoded_data_hash": keccak(hexstr=event["encodedData"]).hex()
                    if "encodedData" in event
                    else None,
                    "recipient": event["recipient"] if "recipient" in event else None,
                    "value": str(event["value"]) if "value" in event else None,
                }
            )
            return event
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e

    def handle_signed_for_user_request(self, blockchain, event):
        func_name = "handle_signed_for_user_request"

        try:
            self.signed_for_user_request_repo.create(
                {
                    "blockchain": blockchain,
                    "transaction_hash": event["transaction_hash"],
                    "signer": event["signer"],
                    "message_hash": event["messageHash"],
                }
            )
            return event
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e

    def handle_signed_for_affirmation(self, blockchain, event):
        func_name = "handle_signed_for_affirmation"

        try:
            self.signed_for_affirmation_repo.create(
                {
                    "blockchain": blockchain,
                    "transaction_hash": event["transaction_hash"],
                    "signer": event["signer"] if "signer" in event else None,
                    "message_hash": event["messageHash"] if "messageHash" in event else None,
                    "src_transaction_hash": event["transactionHash"]
                    if "transactionHash" in event
                    else None,
                }
            )
            return event
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e

    def handle_affirmation_completed(self, blockchain, event):
        func_name = "handle_affirmation_completed"

        try:
            self.affirmation_completed_repo.create(
                {
                    "blockchain": blockchain,
                    "transaction_hash": event["transaction_hash"],
                    "recipient": event["recipient"],
                    "value": str(event["value"]),
                    "src_transaction_hash": "0x" + event["transactionHash"],
                }
            )
            return event
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e

    def handle_relayed_message(self, blockchain, event):
        func_name = "handle_relayed_message"

        try:
            self.relayed_message_repo.create(
                {
                    "blockchain": blockchain,
                    "transaction_hash": event["transaction_hash"],
                    "recipient": event["recipient"],
                    "value": str(event["value"]),
                    "src_transaction_hash": "0x" + event["transactionHash"],
                }
            )
            return event
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e
