from sqlalchemy import func

from repository.base import BaseRepository

from .models import (
    MayanBlockchainTransaction,
    MayanCrossChainTransaction,
    MayanForwarded,
    MayanOrderCreated,
    MayanOrderFulfilled,
    MayanOrderUnlocked,
    MayanSwapAndForwarded,
)


class MayanSwapAndForwardedRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(MayanSwapAndForwarded, session_factory)

    def event_exists(self, transaction_hash: str):
        with self.get_session() as session:
            return (
                session.query(MayanSwapAndForwarded)
                .filter(MayanSwapAndForwarded.transaction_hash == transaction_hash)
                .first()
            )


class MayanForwardedRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(MayanForwarded, session_factory)

    def event_exists(self, transaction_hash: str):
        with self.get_session() as session:
            return (
                session.query(MayanForwarded)
                .filter(MayanForwarded.transaction_hash == transaction_hash)
                .first()
            )


class MayanOrderCreatedRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(MayanOrderCreated, session_factory)

    def event_exists(self, key: str):
        with self.get_session() as session:
            return session.query(MayanOrderCreated).filter(MayanOrderCreated.key == key).first()


class MayanOrderFulfilledRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(MayanOrderFulfilled, session_factory)

    def event_exists(self, key: str):
        with self.get_session() as session:
            return session.query(MayanOrderFulfilled).filter(MayanOrderFulfilled.key == key).first()


class MayanOrderUnlockedRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(MayanOrderUnlocked, session_factory)

    def event_exists(self, key: str):
        with self.get_session() as session:
            return session.query(MayanOrderUnlocked).filter(MayanOrderUnlocked.key == key).first()


class MayanBlockchainTransactionRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(MayanBlockchainTransaction, session_factory)

    def get_transaction_by_hash(self, transaction_hash: str):
        with self.get_session() as session:
            return session.get(MayanBlockchainTransaction, transaction_hash)

    def get_min_timestamp(self):
        with self.get_session() as session:
            return session.query(func.min(MayanBlockchainTransaction.timestamp)).scalar()

    def get_max_timestamp(self):
        with self.get_session() as session:
            return session.query(func.max(MayanBlockchainTransaction.timestamp)).scalar()


########## Processed Data ##########


class MayanCrossChainTransactionRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(MayanCrossChainTransaction, session_factory)

    def get_number_of_records(self):
        with self.get_session() as session:
            return session.query(func.count(MayanCrossChainTransaction.id)).scalar()

    def empty_table(self):
        with self.get_session() as session:
            return session.query(MayanCrossChainTransaction).delete()

    def update_amount_usd(self, transaction_hash: str, amount_usd: float):
        with self.get_session() as session:
            session.query(MayanCrossChainTransaction).filter(
                MayanCrossChainTransaction.src_transaction_hash == transaction_hash
            ).update({"amount_usd": amount_usd})

    def get_by_src_tx_hash(self, src_tx_hash: str):
        with self.get_session() as session:
            return (
                session.query(MayanCrossChainTransaction)
                .filter(MayanCrossChainTransaction.src_transaction_hash == src_tx_hash)
                .first()
            )

    def get_unique_src_dst_contract_pairs(self):
        with self.get_session() as session:
            return (
                session.query(
                    MayanCrossChainTransaction.src_blockchain,
                    MayanCrossChainTransaction.src_contract_address,
                    MayanCrossChainTransaction.dst_blockchain,
                    MayanCrossChainTransaction.dst_contract_address,
                )
                .group_by(
                    MayanCrossChainTransaction.src_blockchain,
                    MayanCrossChainTransaction.src_contract_address,
                    MayanCrossChainTransaction.dst_blockchain,
                    MayanCrossChainTransaction.dst_contract_address,
                )
                .all()
            )

    def get_total_amount_usd_transacted(self):
        with self.get_session() as session:
            return session.query(func.sum(MayanCrossChainTransaction.amount_usd)).scalar()
