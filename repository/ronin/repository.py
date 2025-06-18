from sqlalchemy import Index, func

from repository.base import BaseRepository

from .models import (
    RoninBlockchainTransaction,
    RoninCrossChainTransaction,
    RoninDepositRequested,
    RoninTokenDeposited,
    RoninTokenWithdrew,
    RoninWithdrawalRequested,
)


class RoninDepositRequestedRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(RoninDepositRequested, session_factory)

    def event_exists(self, deposit_id: str):
        with self.get_session() as session:
            return (
                session.query(RoninDepositRequested)
                .filter(RoninDepositRequested.deposit_id == deposit_id)
                .first()
            )


class RoninTokenDepositedRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(RoninTokenDeposited, session_factory)

    def event_exists(self, deposit_id: int):
        with self.get_session() as session:
            return (
                session.query(RoninTokenDeposited)
                .filter(RoninTokenDeposited.deposit_id == deposit_id)
                .first()
            )


class RoninWithdrawalRequestedRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(RoninWithdrawalRequested, session_factory)

    def event_exists(self, withdrawal_id: str):
        with self.get_session() as session:
            return (
                session.query(RoninWithdrawalRequested)
                .filter(RoninWithdrawalRequested.withdrawal_id == withdrawal_id)
                .first()
            )


class RoninTokenWithdrewRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(RoninTokenWithdrew, session_factory)

    def event_exists(self, withdrawal_id: int):
        with self.get_session() as session:
            return (
                session.query(RoninTokenWithdrew)
                .filter(RoninTokenWithdrew.withdrawal_id == withdrawal_id)
                .first()
            )


class RoninBlockchainTransactionRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(RoninBlockchainTransaction, session_factory)

    def get_transaction_by_hash(self, transaction_hash: str):
        with self.get_session() as session:
            return session.get(RoninBlockchainTransaction, transaction_hash)

    def get_min_timestamp(self):
        with self.get_session() as session:
            return session.query(func.min(RoninBlockchainTransaction.timestamp)).scalar()

    def get_max_timestamp(self):
        with self.get_session() as session:
            return session.query(func.max(RoninBlockchainTransaction.timestamp)).scalar()


########## Processed Data ##########


class RoninCrossChainTransactionRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(RoninCrossChainTransaction, session_factory)

    def get_number_of_records(self):
        with self.get_session() as session:
            return session.query(func.count(RoninCrossChainTransaction.id)).scalar()

    def empty_table(self):
        with self.get_session() as session:
            return session.query(RoninCrossChainTransaction).delete()

    def update_amount_usd(self, transaction_hash: str, amount_usd: float):
        with self.get_session() as session:
            session.query(RoninCrossChainTransaction).filter(
                RoninCrossChainTransaction.src_transaction_hash == transaction_hash
            ).update({"amount_usd": amount_usd})

    def get_by_src_tx_hash(self, src_tx_hash: str):
        with self.get_session() as session:
            return (
                session.query(RoninCrossChainTransaction)
                .filter(RoninCrossChainTransaction.src_transaction_hash == src_tx_hash)
                .first()
            )

    def get_unique_src_dst_contract_pairs(self):
        with self.get_session() as session:
            return (
                session.query(
                    RoninCrossChainTransaction.src_blockchain,
                    RoninCrossChainTransaction.src_contract_address,
                    RoninCrossChainTransaction.dst_blockchain,
                    RoninCrossChainTransaction.dst_contract_address,
                )
                .group_by(
                    RoninCrossChainTransaction.src_blockchain,
                    RoninCrossChainTransaction.src_contract_address,
                    RoninCrossChainTransaction.dst_blockchain,
                    RoninCrossChainTransaction.dst_contract_address,
                )
                .all()
            )

    def get_total_amount_usd_transacted(self):
        with self.get_session() as session:
            return session.query(func.sum(RoninCrossChainTransaction.amount_usd)).scalar()


Index("ix_deposit_requested_deposit_id", RoninDepositRequested.deposit_id)
Index("ix_token_deposited_deposit_id", RoninTokenDeposited.deposit_id)
Index("ix_withdrawal_requested_withdrawal_id", RoninWithdrawalRequested.withdrawal_id)
Index("ix_token_withdrawn_withdrawal_id", RoninTokenWithdrew.withdrawal_id)
