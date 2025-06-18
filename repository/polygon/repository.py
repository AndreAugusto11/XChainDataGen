from sqlalchemy import Index, func

from repository.base import BaseRepository

from .models import (
    PolygonBlockchainTransaction,
    PolygonBridgeWithdraw,
    PolygonCrossChainTransactions,
    PolygonExitedToken,
    PolygonLockedToken,
    PolygonNewDepositBlock,
    PolygonPlasmaCrossChainTransactions,
    PolygonPOLWithdraw,
    PolygonStateCommitted,
    PolygonStateSynced,
    PolygonTokenDeposited,
)


class PolygonStateSyncedRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(PolygonStateSynced, session_factory)

    def event_exists(self, state_id: str):
        with self.get_session() as session:
            return (
                session.query(PolygonStateSynced)
                .filter(PolygonStateSynced.state_id == state_id)
                .first()
            )


class PolygonStateCommittedRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(PolygonStateCommitted, session_factory)

    def event_exists(self, state_id: str):
        with self.get_session() as session:
            return (
                session.query(PolygonStateCommitted)
                .filter(PolygonStateCommitted.state_id == state_id)
                .first()
            )


class PolygonLockedTokenRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(PolygonLockedToken, session_factory)

    def event_exists(self, transaction_hash, depositor, deposit_receiver, root_token, amount):
        with self.get_session() as session:
            return (
                session.query(PolygonLockedToken)
                .filter(
                    PolygonLockedToken.transaction_hash == transaction_hash,
                    PolygonLockedToken.depositor == depositor,
                    PolygonLockedToken.deposit_receiver == deposit_receiver,
                    PolygonLockedToken.root_token == root_token,
                    PolygonLockedToken.amount == amount,
                )
                .first()
            )


class PolygonExitedTokenRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(PolygonExitedToken, session_factory)

    def event_exists(self, transaction_hash, exitor, deposit_receiver, root_token, amount):
        with self.get_session() as session:
            return (
                session.query(PolygonExitedToken)
                .filter(
                    PolygonExitedToken.transaction_hash == transaction_hash,
                    PolygonExitedToken.exitor == exitor,
                    PolygonExitedToken.deposit_receiver == deposit_receiver,
                    PolygonExitedToken.root_token == root_token,
                    PolygonExitedToken.amount == amount,
                )
                .first()
            )


class PolygonNewDepositBlockRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(PolygonNewDepositBlock, session_factory)

    def event_exists(self, deposit_block_id: str):
        with self.get_session() as session:
            return (
                session.query(PolygonNewDepositBlock)
                .filter(PolygonNewDepositBlock.deposit_block_id == deposit_block_id)
                .first()
            )


class PolygonPOLWithdrawRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(PolygonPOLWithdraw, session_factory)

    def event_exists(self, transaction_hash, from_address, token, amount):
        with self.get_session() as session:
            return (
                session.query(PolygonPOLWithdraw)
                .filter(
                    PolygonPOLWithdraw.transaction_hash == transaction_hash,
                    PolygonPOLWithdraw.from_address == from_address,
                    PolygonPOLWithdraw.token == token,
                    PolygonPOLWithdraw.amount == amount,
                )
                .first()
            )


class PolygonBridgeWithdrawRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(PolygonBridgeWithdraw, session_factory)

    def event_exists(self, exit_id: str):
        with self.get_session() as session:
            return (
                session.query(PolygonBridgeWithdraw)
                .filter(PolygonBridgeWithdraw.exit_id == exit_id)
                .first()
            )


class PolygonTokenDepositedRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(PolygonTokenDeposited, session_factory)

    def event_exists(self, deposit_count: str):
        with self.get_session() as session:
            return (
                session.query(PolygonTokenDeposited)
                .filter(PolygonTokenDeposited.deposit_count == deposit_count)
                .first()
            )


class PolygonBlockchainTransactionRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(PolygonBlockchainTransaction, session_factory)

    def get_transaction_by_hash(self, transaction_hash: str):
        with self.get_session() as session:
            return session.get(PolygonBlockchainTransaction, transaction_hash)

    def get_min_timestamp(self):
        with self.get_session() as session:
            return session.query(func.min(PolygonBlockchainTransaction.timestamp)).scalar()

    def get_max_timestamp(self):
        with self.get_session() as session:
            return session.query(func.max(PolygonBlockchainTransaction.timestamp)).scalar()


# ########## Processed Data ##########


class PolygonCrossChainTransactionsRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(PolygonCrossChainTransactions, session_factory)

    def get_number_of_records(self):
        with self.get_session() as session:
            return session.query(func.count(PolygonCrossChainTransactions.id)).scalar()

    def empty_table(self):
        with self.get_session() as session:
            return session.query(PolygonCrossChainTransactions).delete()

    def update_amount_usd(self, transaction_hash: str, amount_usd: float):
        with self.get_session() as session:
            session.query(PolygonCrossChainTransactions).filter(
                PolygonCrossChainTransactions.src_transaction_hash == transaction_hash
            ).update({"amount_usd": amount_usd})

    def get_by_src_tx_hash(self, src_tx_hash: str):
        with self.get_session() as session:
            return (
                session.query(PolygonCrossChainTransactions)
                .filter(PolygonCrossChainTransactions.src_transaction_hash == src_tx_hash)
                .first()
            )

    def get_unique_src_dst_contract_pairs(self):
        with self.get_session() as session:
            return (
                session.query(
                    PolygonCrossChainTransactions.src_blockchain,
                    PolygonCrossChainTransactions.src_contract_address,
                )
                .group_by(
                    PolygonCrossChainTransactions.src_blockchain,
                    PolygonCrossChainTransactions.src_contract_address,
                )
                .all()
            )

    def get_total_amount_usd_transacted(self):
        with self.get_session() as session:
            return session.query(func.sum(PolygonCrossChainTransactions.amount_usd)).scalar()


class PolygonPlasmaCrossChainTransactionsRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(PolygonPlasmaCrossChainTransactions, session_factory)

    def get_number_of_records(self):
        with self.get_session() as session:
            return session.query(func.count(PolygonPlasmaCrossChainTransactions.id)).scalar()

    def empty_table(self):
        with self.get_session() as session:
            return session.query(PolygonPlasmaCrossChainTransactions).delete()

    def update_amount_usd(self, transaction_hash: str, amount_usd: float):
        with self.get_session() as session:
            session.query(PolygonPlasmaCrossChainTransactions).filter(
                PolygonPlasmaCrossChainTransactions.src_transaction_hash == transaction_hash
            ).update({"amount_usd": amount_usd})

    def get_by_src_tx_hash(self, src_tx_hash: str):
        with self.get_session() as session:
            return (
                session.query(PolygonPlasmaCrossChainTransactions)
                .filter(PolygonPlasmaCrossChainTransactions.src_transaction_hash == src_tx_hash)
                .first()
            )

    def get_unique_src_dst_contract_pairs(self):
        with self.get_session() as session:
            return (
                session.query(
                    PolygonPlasmaCrossChainTransactions.src_blockchain,
                    PolygonPlasmaCrossChainTransactions.src_contract_address,
                )
                .group_by(
                    PolygonPlasmaCrossChainTransactions.src_blockchain,
                    PolygonPlasmaCrossChainTransactions.src_contract_address,
                )
                .all()
            )

    def get_total_amount_usd_transacted(self):
        with self.get_session() as session:
            return session.query(func.sum(PolygonPlasmaCrossChainTransactions.amount_usd)).scalar()


Index("ix_polygon_state_synced_state_id", PolygonStateSynced.state_id)
Index("ix_polygon_state_committed_state_id", PolygonStateCommitted.state_id)
Index(
    "ix_polygon_locked_token_unique_key",
    PolygonLockedToken.transaction_hash,
    PolygonLockedToken.depositor,
    PolygonLockedToken.deposit_receiver,
    PolygonLockedToken.root_token,
)
Index(
    "ix_polygon_exited_token_unique_key",
    PolygonExitedToken.transaction_hash,
    PolygonExitedToken.exitor,
    PolygonExitedToken.root_token,
    PolygonExitedToken.amount,
)
Index("ix_polygon_new_deposit_block_deposit_block_id", PolygonNewDepositBlock.deposit_block_id)
Index(
    "ix_polygon_pol_withdraw_unique_key",
    PolygonPOLWithdraw.transaction_hash,
    PolygonPOLWithdraw.transaction_hash,
    PolygonPOLWithdraw.from_address,
    PolygonPOLWithdraw.token,
    PolygonPOLWithdraw.amount,
)
Index("ix_polygon_bridge_withdraw_exit_id", PolygonBridgeWithdraw.exit_id)
Index("ix_polygon_token_deposited_deposit_count", PolygonTokenDeposited.deposit_count)
