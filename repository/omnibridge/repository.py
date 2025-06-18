from sqlalchemy import func

from repository.base import BaseRepository

from .models import (
    OmnibridgeAffirmationCompleted,
    OmnibridgeBlockchainTransaction,
    OmnibridgeCrossChainTransactions,
    OmnibridgeOperatorTransactions,
    OmnibridgeRelayedMessage,
    OmnibridgeSignedForAffirmation,
    OmnibridgeSignedForUserRequest,
    OmnibridgeTokensBridged,
    OmnibridgeTokensBridgingInitiated,
    OmnibridgeUserRequestForAffirmation,
    OmnibridgeUserRequestForSignature,
)


class OmnibridgeBlockchainTransactionRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(OmnibridgeBlockchainTransaction, session_factory)

    def get_transaction_by_hash(self, transaction_hash: str):
        with self.get_session() as session:
            return session.get(OmnibridgeBlockchainTransaction, transaction_hash)

    def get_min_timestamp(self):
        with self.get_session() as session:
            return session.query(func.min(OmnibridgeBlockchainTransaction.timestamp)).scalar()

    def get_max_timestamp(self):
        with self.get_session() as session:
            return session.query(func.max(OmnibridgeBlockchainTransaction.timestamp)).scalar()


class OmnibridgeTokensBridgedRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(OmnibridgeTokensBridged, session_factory)


class OmnibridgeTokensBridgingInitiatedRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(OmnibridgeTokensBridgingInitiated, session_factory)


class OmnibridgeRelayedMessageRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(OmnibridgeRelayedMessage, session_factory)


class OmnibridgeSignedForUserRequestRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(OmnibridgeSignedForUserRequest, session_factory)


class OmnibridgeSignedForAffirmationRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(OmnibridgeSignedForAffirmation, session_factory)


class OmnibridgeUserRequestForSignatureRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(OmnibridgeUserRequestForSignature, session_factory)


class OmnibridgeAffirmationCompletedRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(OmnibridgeAffirmationCompleted, session_factory)


class OmnibridgeUserRequestForAffirmationRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(OmnibridgeUserRequestForAffirmation, session_factory)


########## Processed Data ##########


class OmnibridgeCrossChainTransactionsRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(OmnibridgeCrossChainTransactions, session_factory)

    def get_number_of_records(self):
        with self.get_session() as session:
            return session.query(func.count(OmnibridgeCrossChainTransactions.id)).scalar()

    def empty_table(self):
        with self.get_session() as session:
            return session.query(OmnibridgeCrossChainTransactions).delete()

    def update_amount_usd(self, transaction_hash: str, amount_usd: float):
        with self.get_session() as session:
            session.query(OmnibridgeCrossChainTransactions).filter(
                OmnibridgeCrossChainTransactions.src_transaction_hash == transaction_hash
            ).update({"amount_usd": amount_usd})

    def get_by_src_tx_hash(self, src_tx_hash: str):
        with self.get_session() as session:
            return (
                session.query(OmnibridgeCrossChainTransactions)
                .filter(OmnibridgeCrossChainTransactions.src_transaction_hash == src_tx_hash)
                .first()
            )

    def get_unique_src_dst_contract_pairs(self):
        with self.get_session() as session:
            return (
                session.query(
                    OmnibridgeCrossChainTransactions.src_blockchain,
                    OmnibridgeCrossChainTransactions.src_contract_address,
                    OmnibridgeCrossChainTransactions.dst_blockchain,
                    OmnibridgeCrossChainTransactions.dst_contract_address,
                )
                .group_by(
                    OmnibridgeCrossChainTransactions.src_blockchain,
                    OmnibridgeCrossChainTransactions.src_contract_address,
                    OmnibridgeCrossChainTransactions.dst_blockchain,
                    OmnibridgeCrossChainTransactions.dst_contract_address,
                )
                .all()
            )

    def get_total_amount_usd_transacted(self):
        with self.get_session() as session:
            return session.query(func.sum(OmnibridgeCrossChainTransactions.amount_usd)).scalar()


class OmnibridgeOperatorTransactionsRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(OmnibridgeOperatorTransactions, session_factory)

    def get_number_of_records(self):
        with self.get_session() as session:
            return session.query(func.count(OmnibridgeOperatorTransactions.id)).scalar()

    def empty_table(self):
        with self.get_session() as session:
            return session.query(OmnibridgeOperatorTransactions).delete()
