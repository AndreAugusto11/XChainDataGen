from sqlalchemy import Index, func

from repository.base import BaseRepository

from .models import (
    AcrossBlockchainTransaction,
    AcrossCrossChainTransaction,
    AcrossFilledRelay,
    AcrossFundsDeposited,
    AcrossRelayerRefund,
)


class AcrossRelayerRefundRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(AcrossRelayerRefund, session_factory)

    def event_exists(
        self,
        transaction_hash: str,
        amount_to_return: str,
        refund_amount: str,
        l2_token_address: str,
        refund_address: str,
    ):
        with self.get_session() as session:
            return (
                session.query(AcrossRelayerRefund)
                .filter(
                    AcrossRelayerRefund.transaction_hash == transaction_hash,
                    AcrossRelayerRefund.amount_to_return == amount_to_return,
                    AcrossRelayerRefund.refund_amount == refund_amount,
                    AcrossRelayerRefund.l2_token_address == l2_token_address,
                    AcrossRelayerRefund.refund_address == refund_address,
                )
                .first()
            )


class AcrossFilledRelayRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(AcrossFilledRelay, session_factory)

    def event_exists(self, deposit_id: str):
        with self.get_session() as session:
            return (
                session.query(AcrossFilledRelay)
                .filter(AcrossFilledRelay.deposit_id == deposit_id)
                .first()
            )


class AcrossFundsDepositedRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(AcrossFundsDeposited, session_factory)

    def event_exists(self, deposit_id: str):
        with self.get_session() as session:
            return (
                session.query(AcrossFundsDeposited)
                .filter(AcrossFundsDeposited.deposit_id == deposit_id)
                .first()
            )


class AcrossBlockchainTransactionRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(AcrossBlockchainTransaction, session_factory)

    def get_transaction_by_hash(self, transaction_hash: str):
        with self.get_session() as session:
            return session.get(AcrossBlockchainTransaction, transaction_hash)

    def get_min_timestamp(self):
        with self.get_session() as session:
            return session.query(func.min(AcrossBlockchainTransaction.timestamp)).scalar()

    def get_max_timestamp(self):
        with self.get_session() as session:
            return session.query(func.max(AcrossBlockchainTransaction.timestamp)).scalar()


########## Processed Data ##########


class AcrossCrossChainTransactionRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(AcrossCrossChainTransaction, session_factory)

    def get_number_of_records(self):
        with self.get_session() as session:
            return session.query(func.count(AcrossCrossChainTransaction.intent_id)).scalar()

    def empty_table(self):
        with self.get_session() as session:
            return session.query(AcrossCrossChainTransaction).delete()

    def get_by_src_tx_hash(self, src_tx_hash: str):
        with self.get_session() as session:
            return (
                session.query(AcrossCrossChainTransaction)
                .filter(AcrossCrossChainTransaction.src_transaction_hash == src_tx_hash)
                .first()
            )

    # select src_blockchain, src_contract_address, dst_blockchain, dst_contract_address from
    # stargate_bus_cross_chain_transactions group by src_contract_address, dst_contract_address;
    def get_unique_src_dst_contract_pairs(self):
        with self.get_session() as session:
            return (
                session.query(
                    AcrossCrossChainTransaction.src_blockchain,
                    AcrossCrossChainTransaction.src_contract_address,
                    AcrossCrossChainTransaction.dst_blockchain,
                    AcrossCrossChainTransaction.dst_contract_address,
                )
                .group_by(
                    AcrossCrossChainTransaction.src_blockchain,
                    AcrossCrossChainTransaction.src_contract_address,
                    AcrossCrossChainTransaction.dst_blockchain,
                    AcrossCrossChainTransaction.dst_contract_address,
                )
                .all()
            )

    def get_total_amount_usd_transacted(self):
        with self.get_session() as session:
            return session.query(func.sum(AcrossCrossChainTransaction.input_amount_usd)).scalar()


Index("ix_blockchain_transactions_tx_hash", AcrossBlockchainTransaction.transaction_hash)
Index("ix_filled_v3_relay_tx_hash", AcrossFilledRelay.transaction_hash)
Index("ix_filled_v3_relay_deposit_id", AcrossFilledRelay.deposit_id)
Index("ix_funds_deposited_tx_hash", AcrossFundsDeposited.transaction_hash)
Index("ix_funds_deposited_deposit_id", AcrossFundsDeposited.deposit_id)
