from typing import Any, Dict, List

from config.constants import Bridge
from extractor.base_handler import BaseHandler
from extractor.mayan.constants import BLOCKCHAIN_IDS, BRIDGE_CONFIG, WETH_CONTRACT_ADDRESSES
from repository.database import DBSession
from repository.mayan.repository import (
    MayanBlockchainTransactionRepository,
    MayanForwardedRepository,
    MayanOrderCreatedRepository,
    MayanOrderFulfilledRepository,
    MayanOrderUnlockedRepository,
    MayanSwapAndForwardedRepository,
)
from utils.rpc_utils import RPCClient
from utils.utils import CustomException, log_error


class MayanHandler(BaseHandler):
    CLASS_NAME = "MayanHandler"

    def __init__(self, rpc_client: RPCClient, blockchains: list) -> None:
        super().__init__(rpc_client, blockchains)
        self.bridge = Bridge.MAYAN

    def get_bridge_contracts_and_topics(self, bridge: str, blockchain: List[str]) -> None:
        return super().get_bridge_contracts_and_topics(
            config=BRIDGE_CONFIG,
            bridge=bridge,
            blockchain=blockchain,
        )

    def bind_db_to_repos(self):
        self.blockchain_transaction_repo = MayanBlockchainTransactionRepository(DBSession)
        self.order_created_repo = MayanOrderCreatedRepository(DBSession)
        self.order_fulfilled_repo = MayanOrderFulfilledRepository(DBSession)
        self.order_unlocked_repo = MayanOrderUnlockedRepository(DBSession)
        self.swap_and_forwarded_repo = MayanSwapAndForwardedRepository(DBSession)
        self.forwarded_repo = MayanForwardedRepository(DBSession)

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
                    == "0x7cbff921ae1f3ea71284120d2aabde13587df067f2bb5c831ea6e35d7a9242ac"
                ):  # SwapAndForwardedEth
                    event = self.handle_swap_and_forwarded_eth(blockchain, event)
                elif (
                    event["topic"]
                    == "0x23278f58875126c795a4072b98b5851fe9b21cea19895b02a6224fefbb1e3298"
                ):  # SwapAndForwardedERC20
                    event = self.handle_swap_and_forwarded_erc20(blockchain, event)
                elif (
                    event["topic"]
                    == "0xb8543d214cab9591941648db8d40126a163bfd0db4a865678320b921e1398043"
                ):  # ForwardedEth
                    event = self.handle_forwarded_eth(blockchain, event)
                elif (
                    event["topic"]
                    == "0xbf150db6b4a14b084f7346b4bc300f552ce867afe55be27bce2d6b37e3307cda"
                ):  # ForwardedERC20
                    event = self.handle_forwarded_erc20(blockchain, event)
                elif (
                    event["topic"]
                    == "0x918554b6bd6e2895ce6553de5de0e1a69db5289aa0e4fe193a0dcd1f14347477"
                ):  # OrderCreated
                    event = self.handle_order_created(blockchain, event)
                elif (
                    event["topic"]
                    == "0x6ec9b1b5a9f54d929394f18dac4ba1b1cc79823f2266c2d09cab8a3b4700b40b"
                ):  # OrderFulfilled
                    event = self.handle_order_fulfilled(blockchain, event)
                elif (
                    event["topic"]
                    == "0x4bdcff348c4d11383c487afb95f732f243d93fbfc478aa736a4981cf6a640911"
                ):  # OrderUnlocked
                    event = self.handle_order_unlocked(blockchain, event)

                if event:
                    included_events.append(event)

            except CustomException as e:
                request_desc = (
                    f"Error processing request: {blockchain}, {start_block}, "
                    f"{end_block}, {contract}, {topics}.\n{e}"
                )
                log_error(self.bridge, request_desc)

        return included_events

    def handle_swap_and_forwarded_eth(self, blockchain, event):
        func_name = "handle_swap_and_forwarded_eth"

        event["tokenIn"] = self.populate_weth_token(blockchain)

        try:
            return self.handle_swap_and_forwarded(blockchain, event)
        except CustomException as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e

    def handle_swap_and_forwarded_erc20(self, blockchain, event):
        func_name = "handle_swap_and_forwarded_erc20"

        try:
            return self.handle_swap_and_forwarded(blockchain, event)
        except CustomException as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e

    def handle_swap_and_forwarded(self, blockchain, event):
        func_name = "handle_swap_and_forwarded"

        try:
            if self.swap_and_forwarded_repo.event_exists(event["transaction_hash"]):
                return None

            # Only interested in events from the Mayan Swift protocol (other alternatives
            # are WH Swap Bridge and Mayan MCTP, currently not supported)
            if event["mayanProtocol"] != "0xC38e4e6A15593f908255214653d3D947CA1c2338":
                return None

            decoded_payload = None

            # function signature for createOrderWithEth
            if event["mayanData"][:8] == "b866e173":
                from extractor.mayan.utils.MayanOrderParamsDecoder import MayanOrderParamsDecoder

                decoded_payload = MayanOrderParamsDecoder.decode(event["mayanData"][8:])

            # function signature for createOrderWithToken
            elif event["mayanData"][:8] == "8e8d142b":
                from extractor.mayan.utils.MayanOrderParamsDecoder import MayanOrderParamsDecoder

                decoded_payload = MayanOrderParamsDecoder.decode(event["mayanData"][136:])

            dst_chain = self.convert_id_to_blockchain_name(
                id=decoded_payload["destChainId"],
                blockchain_ids=BLOCKCHAIN_IDS,
            )

            if not dst_chain:
                return None

            self.swap_and_forwarded_repo.create(
                {
                    "blockchain": blockchain,
                    "transaction_hash": event["transaction_hash"],
                    "token_in": event["tokenIn"],
                    "amount_in": event["amountIn"],
                    "swap_protocol": event["swapProtocol"],
                    "middle_token": event["middleToken"],
                    "middle_amount": event["middleAmount"],
                    "mayan_protocol": event["mayanProtocol"],
                    "trader": decoded_payload["trader"],
                    "token_out": decoded_payload["tokenOut"],
                    "min_amount_out": decoded_payload["minAmountOut"],
                    "gas_drop": decoded_payload["gasDrop"],
                    "cancel_fee": decoded_payload["cancelFee"],
                    "refund_fee": decoded_payload["refundFee"],
                    "deadline": decoded_payload["deadline"],
                    "dst_addr": decoded_payload["destAddr"],
                    "dst_chain": dst_chain,
                    "referrer_addr": decoded_payload["referrerAddr"],
                    "referrer_bps": decoded_payload["referrerBps"],
                    "auction_mode": decoded_payload["auctionMode"],
                    "random": decoded_payload["random"],
                }
            )
            return event
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e

    def handle_forwarded_eth(self, blockchain, event):
        func_name = "handle_forwarded_eth"

        event["token"] = self.populate_weth_token(blockchain)

        try:
            return self.handle_forwarded(blockchain, event)
        except CustomException as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e

    def handle_forwarded_erc20(self, blockchain, event):
        func_name = "handle_forwarded_erc20"

        try:
            return self.handle_forwarded(blockchain, event)
        except CustomException as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e

    def handle_forwarded(self, blockchain, event):
        func_name = "handle_forwarded"

        try:
            if self.swap_and_forwarded_repo.event_exists(event["transaction_hash"]):
                return None

            # Only interested in events from the Mayan Swift protocol (other alternatives
            # are WH Swap Bridge and Mayan MCTP, currently not supported)
            if event["mayanProtocol"] != "0xC38e4e6A15593f908255214653d3D947CA1c2338":
                return None

            decoded_payload = None

            # function signature for createOrderWithEth
            if event["protocolData"][:8] == "b866e173":
                from extractor.mayan.utils.MayanOrderParamsDecoder import MayanOrderParamsDecoder

                decoded_payload = MayanOrderParamsDecoder.decode(event["protocolData"][8:])

            # function signature for createOrderWithToken
            elif event["protocolData"][:8] == "8e8d142b":
                from extractor.mayan.utils.MayanOrderParamsDecoder import MayanOrderParamsDecoder

                decoded_payload = MayanOrderParamsDecoder.decode(event["protocolData"][136:])

            dst_chain = self.convert_id_to_blockchain_name(
                id=decoded_payload["destChainId"],
                blockchain_ids=BLOCKCHAIN_IDS,
            )

            if not dst_chain:
                return None

            self.forwarded_repo.create(
                {
                    "blockchain": blockchain,
                    "transaction_hash": event["transaction_hash"],
                    "token": event["token"],
                    "amount": event["amount"] if "amount" in event else None,
                    "mayan_protocol": event["mayanProtocol"],
                    "trader": decoded_payload["trader"],
                    "token_out": decoded_payload["tokenOut"],
                    "min_amount_out": decoded_payload["minAmountOut"],
                    "gas_drop": decoded_payload["gasDrop"],
                    "cancel_fee": decoded_payload["cancelFee"],
                    "refund_fee": decoded_payload["refundFee"],
                    "deadline": decoded_payload["deadline"],
                    "dst_addr": decoded_payload["destAddr"],
                    "dst_chain": dst_chain,
                    "referrer_addr": decoded_payload["referrerAddr"],
                    "referrer_bps": decoded_payload["referrerBps"],
                    "auction_mode": decoded_payload["auctionMode"],
                    "random": decoded_payload["random"],
                }
            )
            return event
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e

    def handle_order_created(self, blockchain, event):
        func_name = "handle_order_created"

        try:
            if self.order_created_repo.event_exists(event["key"]):
                return None

            self.order_created_repo.create(
                {
                    "blockchain": blockchain,
                    "transaction_hash": event["transaction_hash"],
                    "key": event["key"],
                }
            )
            return event
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e

    def handle_order_fulfilled(self, blockchain, event):
        func_name = "handle_order_fulfilled"

        try:
            if self.order_fulfilled_repo.event_exists(event["key"]):
                return None

            self.order_fulfilled_repo.create(
                {
                    "blockchain": blockchain,
                    "transaction_hash": event["transaction_hash"],
                    "key": event["key"],
                    "sequence": event["sequence"],
                    "net_amount": event["netAmount"],
                }
            )
            return event
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e

    def handle_order_unlocked(self, blockchain, event):
        func_name = "handle_order_unlocked"

        try:
            if self.order_unlocked_repo.event_exists(event["key"]):
                return None

            self.order_unlocked_repo.create(
                {
                    "blockchain": blockchain,
                    "transaction_hash": event["transaction_hash"],
                    "key": event["key"],
                }
            )
            return event
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e

    def populate_weth_token(self, blockchain: str) -> str:
        """
        Populates the WETH token address based on the blockchain.

        Args:
            blockchain: The blockchain to populate the WETH token for.

        Returns:
            The WETH token address.
        """
        return WETH_CONTRACT_ADDRESSES[blockchain]["contract_address"]
