from typing import Any, Dict, List

from config.constants import Bridge
from extractor.base_handler import BaseHandler
from extractor.portal.constants import BLOCKCHAIN_IDS, BRIDGE_CONFIG
from extractor.portal.utils.PayloadDecoder import PayloadDecoder
from repository.database import DBSession
from repository.portal.repository import (
    PortalBlockchainTransactionRepository,
    PortalLogMessagePublishedRepository,
    PortalTransferRedeemedRepository,
)
from utils.rpc_utils import RPCClient
from utils.utils import CustomException, log_error, unpad_address


class PortalHandler(BaseHandler):
    CLASS_NAME = "PortalHandler"

    def __init__(self, rpc_client: RPCClient) -> None:
        super().__init__(rpc_client)
        self.bridge = Bridge.PORTAL

    def get_bridge_contracts_and_topics(self, bridge: str, blockchain: List[str]) -> None:
        self.get_bridge_contracts_and_topics(
            config=BRIDGE_CONFIG,
            bridge=bridge,
            blockchain=blockchain,
        )

    def bind_db_to_repos(self):
        self.blockchain_transaction_repo = PortalBlockchainTransactionRepository(DBSession)
        self.log_message_published_repo = PortalLogMessagePublishedRepository(DBSession)
        self.transfer_redeemed_repo = PortalTransferRedeemedRepository(DBSession)

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
                    == "0x6eb224fb001ed210e379b335e35efe88672a8ce935d981a6896b27ffdf52a3b2"
                ):  # LogMessagePublished
                    event = self.handle_log_message_published(blockchain, event)
                elif (
                    event["topic"]
                    == "0xcaf280c8cfeba144da67230d9b009c8f868a75bac9a528fa0474be1ba317c169"
                ):  # TransferRedeemed
                    event = self.handle_transfer_redeemed(blockchain, event)

                if event:
                    included_events.append(event)

            except CustomException as e:
                request_desc = (
                    f"Error processing request: {blockchain}, {start_block}, "
                    f"{end_block}, {contract}, {topics}.\n{e}"
                )
                log_error(self.bridge, request_desc)

        return included_events

    def handle_log_message_published(self, blockchain, event):
        func_name = "handle_log_message_published"

        token_decimals = 18

        print(len(event["payload"]))

        if len(event["payload"]) != 266:
            # this means that we are dealing with a transfer of another protocol on top of wormhole
            return None

        try:
            payload_decoded = PayloadDecoder.decode(event["payload"], token_decimals)

            dst_chain = self.convert_id_to_blockchain_name(payload_decoded["toChain"])

            if dst_chain is None:
                return None

            self.log_message_published_repo.create(
                {
                    "amount": payload_decoded["originalAmount"],
                    "token_address": unpad_address(payload_decoded["tokenAddress"]),
                    "token_chain": payload_decoded["tokenChain"],
                    "recipient": payload_decoded["to"],
                    "recipient_chain": dst_chain,
                    "fee": payload_decoded["fee"],
                    "nonce": event["nonce"],
                    "sequence_number": event["sequence"],
                }
            )
            return event
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e

    def handle_transfer_redeemed(self, blockchain, event):
        func_name = "handle_transfer_redeemed"

        try:
            src_chain = self.convert_id_to_blockchain_name(event["emitter_chain_id"])

            if src_chain is None:
                return None

            self.transfer_redeemed_repo.create(
                {
                    "emitter_chain": src_chain,
                    "emitter_address": unpad_address(event["emitter_address"]),
                    "sequence_number": event["sequence"],
                    "data": event["data"],
                }
            )
            return event
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e

    def convert_id_to_blockchain_name(self, id: str) -> str:
        func_name = "convert_id_to_blockchain_name"

        id = str(id)

        # Discard smaller blockchains as we focus on the ones with more transferred value
        # and only EVM-based blockchains. See list here https://wormhole.com/docs/build/reference/chain-ids/

        if id in BLOCKCHAIN_IDS:
            blockchain_name = BLOCKCHAIN_IDS[id]["name"]
            # If the blockchain name is not in the list of blockchains specified by the user,
            # return None
            if self.counterPartyBlockchainsMap.get(blockchain_name):
                return BLOCKCHAIN_IDS[id]["name"]
        else:
            CustomException(self.CLASS_NAME, func_name, f"Blockchain not found for ID: {id}")
            # log_to_file(e, "data/out_of_scope_blockchains.log")
            return None
