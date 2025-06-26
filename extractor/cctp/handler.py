from typing import Any, Dict, List

from config.constants import Bridge
from extractor.base_handler import BaseHandler
from extractor.cctp.constants import BRIDGE_CONFIG
from extractor.cctp.utils.MessageBodyDecoder import MessageBodyDecoder
from repository.cctp.repository import (
    CCTPBlockchainTransactionRepository,
    CCTPDepositForBurnRepository,
    CCTPMessageReceivedRepository,
)
from repository.database import DBSession
from rpcs.evm_rpc_client import EvmRPCClient
from utils.utils import CustomException, log_error, unpad_address

from .constants import BLOCKCHAIN_IDS


class CctpHandler(BaseHandler):
    CLASS_NAME = "CctpHandler"

    def __init__(self, rpc_client: EvmRPCClient, blockchains: list) -> None:
        super().__init__(rpc_client, blockchains)
        self.bridge = Bridge.CCTP

    def get_bridge_contracts_and_topics(self, bridge: str, blockchain: List[str]) -> None:
        return super().get_bridge_contracts_and_topics(
            config=BRIDGE_CONFIG,
            bridge=bridge,
            blockchain=blockchain,
        )

    def bind_db_to_repos(self):
        self.blockchain_transaction_repo = CCTPBlockchainTransactionRepository(DBSession)
        self.cctp_deposit_for_burn_repo = CCTPDepositForBurnRepository(DBSession)
        self.cctp_message_received_repo = CCTPMessageReceivedRepository(DBSession)

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
                    == "0x2fa9ca894982930190727e75500a97d8dc500233a5065e0f3126c48fbe0343c0"
                ):  # DepositForBurn
                    event = self.handle_deposit_for_burn(blockchain, event)
                elif (
                    event["topic"]
                    == "0x58200b4c34ae05ee816d710053fff3fb75af4395915d3d2a771b24aa10e3cc5d"
                ):  # MessageReceived
                    event = self.handle_message_received(blockchain, event)

                if event:
                    included_events.append(event)

            except CustomException as e:
                request_desc = (
                    f"Error processing request: {blockchain}, {start_block}, "
                    f"{end_block}, {contract}, {topics}.\n{e}"
                )
                log_error(self.bridge, request_desc)

        return included_events

    def handle_deposit_for_burn(self, blockchain, event):
        func_name = "handle_deposit_for_burn"

        destination_chain = self.convert_doman_id_to_blockchain_name(event["destinationDomain"])

        if destination_chain is None:
            return None

        try:
            if self.cctp_deposit_for_burn_repo.event_exists(
                event["nonce"], blockchain, destination_chain
            ):
                return None

            self.cctp_deposit_for_burn_repo.create(
                {
                    "blockchain": blockchain,
                    "transaction_hash": event["transaction_hash"],
                    "nonce": event["nonce"],
                    "depositor": event["depositor"].lower(),
                    "burn_token": event["burnToken"].lower(),
                    "recipient": unpad_address(event["mintRecipient"]),
                    "dst_blockchain": destination_chain,
                    "amount": event["amount"],
                }
            )
            return event
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e

    def handle_message_received(self, blockchain, event):
        func_name = "handle_message_received"

        src_blockchain = self.convert_doman_id_to_blockchain_name(event["sourceDomain"])

        if src_blockchain is None:
            return None

        if (
            len(event["messageBody"]) != 264
        ):  # there are other messages with different length that we don't want to process
            return None

        message_body = MessageBodyDecoder.decode(event["messageBody"])

        try:
            if self.cctp_message_received_repo.event_exists(
                event["nonce"], src_blockchain, blockchain
            ):
                return None

            self.cctp_message_received_repo.create(
                {
                    "blockchain": blockchain,
                    "transaction_hash": event["transaction_hash"],
                    "nonce": event["nonce"],
                    "src_blockchain": src_blockchain,
                    "input_token": message_body["input_token"],
                    "depositor": message_body["depositor"],
                    "recipient": message_body["recipient"],
                    "amount": int(message_body["amount"], 16),
                }
            )

            return event
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e

    def convert_doman_id_to_blockchain_name(self, id: str) -> str:
        func_name = "convert_doman_id_to_blockchain_name"

        id = str(id)

        if id in BLOCKCHAIN_IDS:
            blockchain_name = BLOCKCHAIN_IDS[id]["name"]

            if self.counterPartyBlockchainsMap.get(blockchain_name):
                return blockchain_name
        else:
            CustomException(self.CLASS_NAME, func_name, f"Blockchain not found for Domain ID: {id}")
            # log_to_file(e, "data/out_of_scope_blockchains.log")
            return None
