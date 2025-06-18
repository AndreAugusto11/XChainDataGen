from sqlalchemy import Index, func

from repository.base import BaseRepository

from .models import (
    CCIPBlockchainTransaction,
    CCIPCrossChainTransactions,
    CCIPExecutionStateChanged,
    CCIPSendRequested,
)


class CCIPSendRequestedRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(CCIPSendRequested, session_factory)

    def event_exists(self, message_id: str):
        with self.get_session() as session:
            return (
                session.query(CCIPSendRequested)
                .filter(CCIPSendRequested.message_id == message_id)
                .first()
            )


class CCIPExecutionStateChangedRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(CCIPExecutionStateChanged, session_factory)

    def event_exists(self, message_id: str):
        with self.get_session() as session:
            return (
                session.query(CCIPExecutionStateChanged)
                .filter(CCIPExecutionStateChanged.message_id == message_id)
                .first()
            )


class CCIPBlockchainTransactionRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(CCIPBlockchainTransaction, session_factory)

    def get_transaction_by_hash(self, transaction_hash: str):
        with self.get_session() as session:
            return session.get(CCIPBlockchainTransaction, transaction_hash)

    def get_min_timestamp(self):
        with self.get_session() as session:
            return session.query(func.min(CCIPBlockchainTransaction.timestamp)).scalar()

    def get_max_timestamp(self):
        with self.get_session() as session:
            return session.query(func.max(CCIPBlockchainTransaction.timestamp)).scalar()


########## Processed Data ##########


class CCIPCrossChainTransactionsRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(CCIPCrossChainTransactions, session_factory)

    def get_number_of_records(self):
        with self.get_session() as session:
            return session.query(func.count(CCIPCrossChainTransactions.id)).scalar()

    def empty_table(self):
        with self.get_session() as session:
            return session.query(CCIPCrossChainTransactions).delete()

    def update_amount_usd(self, transaction_hash: str, amount_usd: float):
        with self.get_session() as session:
            session.query(CCIPCrossChainTransactions).filter(
                CCIPCrossChainTransactions.src_transaction_hash == transaction_hash
            ).update({"amount_usd": amount_usd})

    def get_by_src_tx_hash(self, src_tx_hash: str):
        with self.get_session() as session:
            return (
                session.query(CCIPCrossChainTransactions)
                .filter(CCIPCrossChainTransactions.src_transaction_hash == src_tx_hash)
                .first()
            )

    def get_unique_src_dst_contract_pairs(self):
        with self.get_session() as session:
            return (
                session.query(
                    CCIPCrossChainTransactions.src_blockchain,
                    CCIPCrossChainTransactions.src_contract_address,
                )
                .group_by(
                    CCIPCrossChainTransactions.src_blockchain,
                    CCIPCrossChainTransactions.src_contract_address,
                )
                .all()
            )

    def get_total_amount_usd_transacted(self):
        with self.get_session() as session:
            return session.query(func.sum(CCIPCrossChainTransactions.amount_usd)).scalar()


Index("ccip_send_requested_message_id_idx", CCIPSendRequested.message_id)
Index("ccip_send_requested_transaction_hash_idx", CCIPSendRequested.transaction_hash)

Index("ccip_message_received_message_id_idx", CCIPExecutionStateChanged.message_id)
Index("ccip_message_received_transaction_hash_idx", CCIPExecutionStateChanged.transaction_hash)
