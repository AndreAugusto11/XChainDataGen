from sqlalchemy import Index, func

from repository.base import BaseRepository

from .models import (
    DeBridgeBlockchainTransaction,
    DeBridgeClaimedUnlock,
    DeBridgeCreatedOrder,
    DeBridgeCrossChainTransactions,
    DeBridgeFulfilledOrder,
)


class DeBridgeBlockchainTransactionRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(DeBridgeBlockchainTransaction, session_factory)

    def get_transaction_by_hash(self, transaction_hash: str):
        with self.get_session() as session:
            return session.get(DeBridgeBlockchainTransaction, transaction_hash)

    def get_min_timestamp(self):
        with self.get_session() as session:
            return session.query(func.min(DeBridgeBlockchainTransaction.timestamp)).scalar()

    def get_max_timestamp(self):
        with self.get_session() as session:
            return session.query(func.max(DeBridgeBlockchainTransaction.timestamp)).scalar()


class DeBridgeCreatedOrderRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(DeBridgeCreatedOrder, session_factory)

    def event_exists(self, maker_order_nonce: str):
        with self.get_session() as session:
            return (
                session.query(DeBridgeCreatedOrder)
                .filter(DeBridgeCreatedOrder.maker_order_nonce == maker_order_nonce)
                .first()
            )

    def update_middle_info_order_fulfilled(
        self, order_id: str, middle_src_token: str, middle_src_amount: float
    ):
        with self.get_session() as session:
            session.query(DeBridgeCreatedOrder).filter(
                DeBridgeCreatedOrder.order_id == order_id
            ).update({"original_token": middle_src_token, "original_amount": middle_src_amount})


class DeBridgeFulfilledOrderRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(DeBridgeFulfilledOrder, session_factory)

    def event_exists(self, order_id: str):
        with self.get_session() as session:
            return (
                session.query(DeBridgeFulfilledOrder)
                .filter(DeBridgeFulfilledOrder.order_id == order_id)
                .first()
            )

    def update_middle_info_order_fulfilled(
        self, order_id: str, middle_dst_token: str, middle_dst_amount: float
    ):
        with self.get_session() as session:
            session.query(DeBridgeFulfilledOrder).filter(
                DeBridgeFulfilledOrder.order_id == order_id
            ).update({"middle_dst_token": middle_dst_token, "middle_dst_amount": middle_dst_amount})


class DeBridgeClaimedUnlockRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(DeBridgeClaimedUnlock, session_factory)

    def event_exists(self, order_id: str):
        with self.get_session() as session:
            return (
                session.query(DeBridgeClaimedUnlock)
                .filter(DeBridgeClaimedUnlock.order_id == order_id)
                .first()
            )


########## Processed Data ##########


class DeBridgeCrossChainTransactionsRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(DeBridgeCrossChainTransactions, session_factory)

    def get_number_of_records(self):
        with self.get_session() as session:
            return session.query(func.count(DeBridgeCrossChainTransactions.intent_id)).scalar()

    def empty_table(self):
        with self.get_session() as session:
            return session.query(DeBridgeCrossChainTransactions).delete()

    def update_amount_usd(self, transaction_hash: str, amount_usd: float):
        with self.get_session() as session:
            session.query(DeBridgeCrossChainTransactions).filter(
                DeBridgeCrossChainTransactions.src_transaction_hash == transaction_hash
            ).update({"amount_usd": amount_usd})

    def get_by_src_tx_hash(self, src_tx_hash: str):
        with self.get_session() as session:
            return (
                session.query(DeBridgeCrossChainTransactions)
                .filter(DeBridgeCrossChainTransactions.src_transaction_hash == src_tx_hash)
                .first()
            )

    def get_unique_src_dst_contract_pairs(self):
        with self.get_session() as session:
            return (
                session.query(
                    DeBridgeCrossChainTransactions.src_blockchain,
                    DeBridgeCrossChainTransactions.src_contract_address,
                    DeBridgeCrossChainTransactions.dst_blockchain,
                    DeBridgeCrossChainTransactions.dst_contract_address,
                )
                .group_by(
                    DeBridgeCrossChainTransactions.src_blockchain,
                    DeBridgeCrossChainTransactions.src_contract_address,
                    DeBridgeCrossChainTransactions.dst_blockchain,
                    DeBridgeCrossChainTransactions.dst_contract_address,
                )
                .all()
            )

    def get_total_amount_usd_transacted(self):
        with self.get_session() as session:
            return session.query(
                func.sum(DeBridgeCrossChainTransactions.output_amount_usd)
            ).scalar()


Index("idx_debridge_created_order_maker_order_nonce", DeBridgeCreatedOrder.maker_order_nonce)
