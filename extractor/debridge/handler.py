from typing import Any, Dict, List

from eth_utils import keccak

from config.constants import BLOCKCHAIN_IDS, Bridge
from extractor.base_handler import BaseHandler
from extractor.debridge.constants import BRIDGE_CONFIG
from repository.database import DBSession
from repository.debridge.repository import *
from utils.rpc_utils import RPCClient
from utils.utils import CustomException, log_error, unpad_address


class DebridgeHandler(BaseHandler):
    CLASS_NAME = "DebridgeHandler"

    def __init__(self, rpc_client: RPCClient) -> None:
        super().__init__(rpc_client)
        self.bridge = Bridge.DEBRIDGE

    def get_bridge_contracts_and_topics(
        self, bridge: str, blockchain: List[str]
    ) -> None:
        """
        Validates the mapping between the bridge and the blockchains.

        Args:
            bridge: The bridge to validate.
            blockchain: The blockchain to validate.
        """

        if blockchain not in BRIDGE_CONFIG["blockchains"]:
            raise ValueError(
                f"Blockchain {blockchain} not supported for bridge {bridge}."
            )

        return BRIDGE_CONFIG["blockchains"][blockchain]

    def bind_db_to_repos(self):
        """
        This function is needed to rebind the repositories to new sessions when we have to rollback failed transactions
        (e.g., because of unique constraints in the tables) and create a new session.
        Binds the database session to the repository instances used in the handler.
        """

        self.blockchain_transaction_repo = DeBridgeBlockchainTransactionRepository(
            DBSession
        )
        self.created_order_repo = DeBridgeCreatedOrderRepository(DBSession)
        self.fulfilled_order_repo = DeBridgeFulfilledOrderRepository(DBSession)
        self.sent_order_unlock_repo = DeBridgeSentOrderUnlockRepository(DBSession)
        self.claimed_unlock_repo = DeBridgeClaimedUnlockRepository(DBSession)

    def handle_transactions(self, transactions: List[Dict[str, Any]]) -> None:
        func_name = "handle_transactions"
        try:
            self.blockchain_transaction_repo.create_all(transactions)
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"Error writing transactions to database: {e}",
            )

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
            return self.blockchain_transaction_repo.get_transaction_by_hash(
                transaction_hash
            )
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"Error reading transaction from database: {e}",
            )

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
                if event["topic"] == "0xfc8703fd57380f9dd234a89dce51333782d49c5902f307b02f03e014d18fe471":  # CreatedOrder
                    event = self.handle_created_order(blockchain, event)
                elif event["topic"] == "0xd281ee92bab1446041582480d2c0a9dc91f855386bb27ea295faac1e992f7fe4":  # FulfilledOrder
                    event = self.handle_fulfilled_order(blockchain, event)
                elif event["topic"] == "0x37a01d7dc38e924008cf4f2fa3d2ec1f45e7ae3c8292eb3e7d9314b7ad10e2fc":  # SentOrderUnlock
                    event = self.handle_sent_order_unlock(blockchain, event)
                elif event["topic"] == "0x33fff3d864e92b6e1ef9e830196fc019c946104ea621b833aaebd3c3e84b2f6f":  # ClaimedUnlock
                    event = self.handle_claimed_unlock(blockchain, event)

                if event:
                    included_events.append(event)

            except CustomException as e:
                request_desc = f"Error processing request: {blockchain}, {start_block}, {end_block}, {contract}, {topics}.\n{e}"
                log_error(self.bridge, request_desc)

        return included_events


    def handle_created_order(self, blockchain, event):
        func_name = "handle_created_order"

        obj = event['(makerOrderNonce,makerSrc,giveChainId,giveTokenAddress,giveAmount,takeChainId,takeTokenAddress,takeAmount,receiverDst,givePatchAuthoritySrc,orderAuthorityAddressDst,allowedTakerDst,allowedCancelBeneficiarySrc,externalCall)']

        src_blockchain = self.convert_id_to_blockchain_name(obj[2])
        dst_blockchain = self.convert_id_to_blockchain_name(obj[5])

        if src_blockchain is None or dst_blockchain is None:
            return None

        try:
            if self.created_order_repo.event_exists(event["orderId"]):
                return None

            self.created_order_repo.create({
                "blockchain": blockchain,
                "transaction_hash": event["transaction_hash"],
                "maker_order_nonce": obj[0],
                "maker_src": unpad_address(obj[1]),
                "src_blockchain": src_blockchain,
                "give_token_address": unpad_address(obj[3]),
                "give_amount": obj[4],
                "dst_blockchain": dst_blockchain,
                "take_token_address": unpad_address(obj[6]),
                "take_amount": obj[7],
                "receiver_dst": unpad_address(obj[8]),
                "give_patch_authority_src": unpad_address(obj[9]),
                "order_authority_address_dst": unpad_address(obj[10]),
                "allowed_taker_dst": unpad_address(obj[11]),
                "allowed_cancel_beneficiary_src": obj[12],
                "external_call": obj[13],
                "order_id": event["orderId"],
                "affiliate_fee": event.get("affiliateFee"),
                "native_fix_fee": event["nativeFixFee"],
                "percent_fee": event["percentFee"],
                "referral_code": event["referralCode"],
                "_metadata": event.get("metadata"),
            })
            return event
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            )

    def handle_fulfilled_order(self, blockchain, event):
        func_name = "handle_fulfilled_order"

        obj = event['(makerOrderNonce,makerSrc,giveChainId,giveTokenAddress,giveAmount,takeChainId,takeTokenAddress,takeAmount,receiverDst,givePatchAuthoritySrc,orderAuthorityAddressDst,allowedTakerDst,allowedCancelBeneficiarySrc,externalCall)']
        
        src_blockchain = self.convert_id_to_blockchain_name(obj[2])
        dst_blockchain = self.convert_id_to_blockchain_name(obj[5])

        if src_blockchain is None or dst_blockchain is None:
            return None

        try:
            if self.fulfilled_order_repo.event_exists(event["orderId"]):
                return None

            self.fulfilled_order_repo.create({
                "blockchain": blockchain,
                "transaction_hash": event["transaction_hash"],
                "maker_order_nonce": obj[0],
                "maker_src": unpad_address(obj[1]),
                "src_blockchain": src_blockchain,
                "give_token_address": unpad_address(obj[3]),
                "give_amount": obj[4],
                "dst_blockchain": dst_blockchain,
                "take_token_address": unpad_address(obj[6]),
                "take_amount": obj[7],
                "receiver_dst": unpad_address(obj[8]),
                "give_patch_authority_src": unpad_address(obj[9]),
                "order_authority_address_dst": unpad_address(obj[10]),
                "allowed_taker_dst": unpad_address(obj[11]),
                "allowed_cancel_beneficiary_src": unpad_address(obj[12]),
                "external_call": unpad_address(obj[13]),
                "order_id": event["orderId"],
                "sender": unpad_address(event["sender"]),
                "unlock_authority": unpad_address(event["unlockAuthority"]),
            })
            return event
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            )


    def handle_sent_order_unlock(self, blockchain, event):
        func_name = "handle_sent_order_unlock"

        try:
            if self.sent_order_unlock_repo.event_exists(event["orderId"]):
                return None

            self.sent_order_unlock_repo.create({
                "blockchain": blockchain,
                "transaction_hash": event["transaction_hash"],
                "order_id": event["orderId"],
                "beneficiary": unpad_address(event["beneficiary"]),
                "submission_id": event["submissionId"],
            })
            return event
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            )
        

    def handle_claimed_unlock(self, blockchain, event):
        func_name = "handle_claimed_unlock"

        try:
            if self.claimed_unlock_repo.event_exists(event["orderId"]):
                return None

            self.claimed_unlock_repo.create({
                "blockchain": blockchain,
                "transaction_hash": event["transaction_hash"],
                "order_id": event["orderId"],
                "beneficiary": unpad_address(event["beneficiary"]),
                "give_amount": event["giveAmount"],
                "give_token_address": unpad_address(event["giveTokenAddress"]),
            })
            return event
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            )

    def convert_id_to_blockchain_name(self, id: str) -> str:
        func_name = "convert_id_to_blockchain_name"

        id = str(id)

        # Discard smaller blockchains as we focus on the ones with more transferred value
        # see list here https://docs.debridge.finance/the-debridge-messaging-protocol/fees-and-supported-chains
        if id.startswith("1000000"):
            return None

        if id in BLOCKCHAIN_IDS:
            return BLOCKCHAIN_IDS[id]["name"]
        else:
            e = CustomException(
                self.CLASS_NAME, func_name, f"Blockchain not found for ID: {id}"
            )
            # log_to_file(e, "data/out_of_scope_blockchains.log")
            return None
