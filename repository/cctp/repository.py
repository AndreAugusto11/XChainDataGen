from sqlalchemy import Index, func

from repository.base import BaseRepository

from .models import (
    CCTPBlockchainTransaction,
    CctpCrossChainTransactions,
    CCTPDepositForBurn,
    CCTPMessageReceived,
)


class CCTPDepositForBurnRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(CCTPDepositForBurn, session_factory)

    def event_exists(self, nonce: str, blockchain: str, dst_blockchain: str):
        with self.get_session() as session:
            return (
                session.query(CCTPDepositForBurn)
                .filter(
                    CCTPDepositForBurn.nonce == nonce,
                    CCTPDepositForBurn.blockchain == blockchain,
                    CCTPDepositForBurn.dst_blockchain == dst_blockchain,
                )
                .first()
            )


class CCTPMessageReceivedRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(CCTPMessageReceived, session_factory)

    def event_exists(self, nonce: int, src_blockchain: str, blockchain: str):
        with self.get_session() as session:
            return (
                session.query(CCTPMessageReceived)
                .filter(
                    CCTPMessageReceived.nonce == nonce,
                    CCTPMessageReceived.src_blockchain == src_blockchain,
                    CCTPMessageReceived.blockchain == blockchain,
                )
                .first()
            )


class CCTPBlockchainTransactionRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(CCTPBlockchainTransaction, session_factory)

    def get_transaction_by_hash(self, transaction_hash: str):
        with self.get_session() as session:
            return session.get(CCTPBlockchainTransaction, transaction_hash)

    def get_min_timestamp(self):
        with self.get_session() as session:
            return session.query(func.min(CCTPBlockchainTransaction.timestamp)).scalar()

    def get_max_timestamp(self):
        with self.get_session() as session:
            return session.query(func.max(CCTPBlockchainTransaction.timestamp)).scalar()


########## Processed Data ##########


class CctpCrossChainTransactionsRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(CctpCrossChainTransactions, session_factory)

    def get_number_of_records(self):
        with self.get_session() as session:
            return session.query(func.count(CctpCrossChainTransactions.id)).scalar()

    def empty_table(self):
        with self.get_session() as session:
            return session.query(CctpCrossChainTransactions).delete()

    def update_amount_usd(self, transaction_hash: str, amount_usd: float):
        with self.get_session() as session:
            session.query(CctpCrossChainTransactions).filter(
                CctpCrossChainTransactions.src_transaction_hash == transaction_hash
            ).update({"amount_usd": amount_usd})

    def get_by_src_tx_hash(self, src_tx_hash: str):
        with self.get_session() as session:
            return (
                session.query(CctpCrossChainTransactions)
                .filter(CctpCrossChainTransactions.src_transaction_hash == src_tx_hash)
                .first()
            )

    def get_unique_src_dst_contract_pairs(self):
        with self.get_session() as session:
            return (
                session.query(
                    CctpCrossChainTransactions.src_blockchain,
                    CctpCrossChainTransactions.src_contract_address,
                )
                .group_by(
                    CctpCrossChainTransactions.src_blockchain,
                    CctpCrossChainTransactions.src_contract_address,
                )
                .all()
            )

    def get_total_amount_usd_transacted(self):
        with self.get_session() as session:
            return session.query(func.sum(CctpCrossChainTransactions.amount_usd)).scalar()


Index("cctp_deposit_for_burn_nonce_idx", CCTPDepositForBurn.nonce)
Index(
    "cctp_deposit_for_burn_nonce_blockchain_idx",
    CCTPDepositForBurn.nonce,
    CCTPDepositForBurn.dst_blockchain,
    CCTPDepositForBurn.blockchain,
)
Index("cctp_deposit_for_burn_transaction_hash_idx", CCTPDepositForBurn.transaction_hash)

Index("cctp_message_received_nonce_idx", CCTPMessageReceived.nonce)
Index(
    "cctp_message_received_nonce_blockchain_idx",
    CCTPMessageReceived.nonce,
    CCTPMessageReceived.blockchain,
    CCTPMessageReceived.src_blockchain,
)
Index("cctp_message_received_transaction_hash_idx", CCTPMessageReceived.transaction_hash)
