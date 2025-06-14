from sqlalchemy import Index, func

from repository.base import BaseRepository

from .models import (
    PortalBlockchainTransaction,
    PortalCrossChainTransaction,
    PortalLogMessagePublished,
    PortalTransferRedeemed,
)


class PortalLogMessagePublishedRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(PortalLogMessagePublished, session_factory)

    def event_exists(self, sequence_number: str):
        with self.get_session() as session:
            return (
                session.query(PortalLogMessagePublished)
                .filter(PortalLogMessagePublished.sequence_number == sequence_number)
                .first()
            )


class PortalTransferRedeemedRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(PortalTransferRedeemed, session_factory)

    def event_exists(self, sequence_number: str):
        with self.get_session() as session:
            return (
                session.query(PortalTransferRedeemed)
                .filter(PortalTransferRedeemed.sequence_number == sequence_number)
                .first()
            )


class PortalBlockchainTransactionRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(PortalBlockchainTransaction, session_factory)

    def get_transaction_by_hash(self, transaction_hash: str):
        with self.get_session() as session:
            return session.query(PortalBlockchainTransaction).get(transaction_hash)

    def get_min_timestamp(self):
        with self.get_session() as session:
            return session.query(func.min(PortalBlockchainTransaction.timestamp)).scalar()

    def get_max_timestamp(self):
        with self.get_session() as session:
            return session.query(func.max(PortalBlockchainTransaction.timestamp)).scalar()


########## Processed Data ##########


class PortalCrossChainTransactionRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(PortalCrossChainTransaction, session_factory)

    def populate_table(self, query):
        return self.execute(query)

    def get_number_of_records(self):
        with self.get_session() as session:
            return session.query(func.count(PortalCrossChainTransaction.id)).scalar()

    def empty_table(self):
        with self.get_session() as session:
            return session.query(PortalCrossChainTransaction).delete()

    def update_amount_usd(self, transaction_hash: str, amount_usd: float):
        with self.get_session() as session:
            session.query(PortalCrossChainTransaction).filter(
                PortalCrossChainTransaction.src_transaction_hash == transaction_hash
            ).update({"amount_usd": amount_usd})

    def get_by_src_tx_hash(self, src_tx_hash: str):
        with self.get_session() as session:
            return (
                session.query(PortalCrossChainTransaction)
                .filter(PortalCrossChainTransaction.src_transaction_hash == src_tx_hash)
                .first()
            )

    def get_unique_src_dst_contract_pairs(self):
        with self.get_session() as session:
            return (
                session.query(
                    PortalCrossChainTransaction.src_blockchain,
                    PortalCrossChainTransaction.src_contract_address,
                    PortalCrossChainTransaction.dst_blockchain,
                    PortalCrossChainTransaction.dst_contract_address,
                )
                .group_by(
                    PortalCrossChainTransaction.src_blockchain,
                    PortalCrossChainTransaction.src_contract_address,
                    PortalCrossChainTransaction.dst_blockchain,
                    PortalCrossChainTransaction.dst_contract_address,
                )
                .all()
            )

    def get_total_amount_usd_transacted(self):
        with self.get_session() as session:
            return session.query(func.sum(PortalCrossChainTransaction.amount_usd)).scalar()


Index("ix_log_message_published_sequence_number", PortalLogMessagePublished.sequence_number)
Index("ix_transfer_redeemed_sequence_number", PortalTransferRedeemed.sequence_number)
