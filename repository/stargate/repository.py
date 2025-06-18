from sqlalchemy import Index, func

from repository.base import BaseRepository, CrossChainRepository

from .models import (
    StargateBlockchainTransaction,
    StargateBusCrossChainTransaction,
    StargateBusDriven,
    StargateBusRode,
    StargateComposeDelivered,
    StargateComposeSent,
    StargateCrossChainSwap,
    StargateCrossChainTokenTransfers,
    StargateDVNFeePaid,
    StargateExecutorFeePaid,
    StargateOFTCrossChainTransaction,
    StargateOFTReceived,
    StargateOFTReceiveFromChain,
    StargateOFTSendToChain,
    StargateOFTSent,
    StargatePacket,
    StargatePacketDelivered,
    StargatePacketReceived,
    StargatePacketSent,
    StargatePacketVerified,
    StargatePayloadVerified,
    StargateRelayerFee,
    StargateSwap,
    StargateSwapRemote,
    StargateUlnConfigSet,
    StargateVerifierFee,
)


class StargateOFTSentRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(StargateOFTSent, session_factory)

    def get_by_transaction_hash(self, transaction_hash: str):
        with self.get_session() as session:
            return (
                session.query(StargateOFTSent)
                .filter(StargateOFTSent.transaction_hash == transaction_hash)
                .first()
            )

    def event_exists(self, transaction_hash: str, guid: str, amount_received_ld: int):
        with self.get_session() as session:
            return (
                session.query(StargateOFTSent)
                .filter(
                    StargateOFTSent.transaction_hash == transaction_hash,
                    StargateOFTSent.guid == guid,
                    StargateOFTSent.amount_received_ld == amount_received_ld,
                )
                .first()
            )


class StargateOFTReceivedRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(StargateOFTReceived, session_factory)

    def get_all_by_guid(self, guid: str):
        with self.get_session() as session:
            return session.query(StargateOFTReceived).filter(StargateOFTReceived.guid == guid).all()

    def get_by_guid(self, guid: str):
        with self.get_session() as session:
            return (
                session.query(StargateOFTReceived).filter(StargateOFTReceived.guid == guid).first()
            )

    def get_by_transaction_hash(self, transaction_hash: str):
        with self.get_session() as session:
            return (
                session.query(StargateOFTReceived)
                .filter(StargateOFTReceived.transaction_hash == transaction_hash)
                .first()
            )


class StargateOFTSendToChainRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(StargateOFTSendToChain, session_factory)

    def event_exists(self, transaction_hash: str, dst_blockchain: str):
        with self.get_session() as session:
            return (
                session.query(StargateOFTSendToChain)
                .filter(
                    StargateOFTSendToChain.transaction_hash == transaction_hash,
                    StargateOFTSendToChain.dst_blockchain == dst_blockchain,
                )
                .first()
            )


class StargateOFTReceiveFromChainRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(StargateOFTReceiveFromChain, session_factory)

    def get_by_transaction_hash(self, transaction_hash: str):
        with self.get_session() as session:
            return (
                session.query(StargateOFTReceiveFromChain)
                .filter(StargateOFTReceiveFromChain.transaction_hash == transaction_hash)
                .first()
            )

    def event_exists(self, transaction_hash: str, src_blockchain: str):
        with self.get_session() as session:
            return (
                session.query(StargateOFTReceiveFromChain)
                .filter(
                    StargateOFTReceiveFromChain.transaction_hash == transaction_hash,
                    StargateOFTReceiveFromChain.src_blockchain == src_blockchain,
                )
                .first()
            )


class StargateUlnConfigSetRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(StargateUlnConfigSet, session_factory)

    def event_exists(self, transaction_hash: str, dst_blockchain: str, oapp: str):
        with self.get_session() as session:
            return (
                session.query(StargateUlnConfigSet)
                .filter(
                    StargateUlnConfigSet.transaction_hash == transaction_hash,
                    StargateUlnConfigSet.dst_blockchain == dst_blockchain,
                    StargateUlnConfigSet.oapp == oapp,
                )
                .first()
            )


class StargateExecutorFeePaidRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(StargateExecutorFeePaid, session_factory)

    def get_by_transaction_hash(self, transaction_hash: str):
        with self.get_session() as session:
            return (
                session.query(StargateExecutorFeePaid)
                .filter(StargateExecutorFeePaid.transaction_hash == transaction_hash)
                .first()
            )


class StargateDVNFeePaidRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(StargateDVNFeePaid, session_factory)

    def get_total_fee_by_transaction_hash(self, transaction_hash: str):
        with self.get_session() as session:
            return (
                session.query(func.sum(StargateDVNFeePaid.fee))
                .filter(StargateDVNFeePaid.transaction_hash == transaction_hash)
                .scalar()
            )


class StargateBusRodeRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(StargateBusRode, session_factory)

    def get_by_ticket_id(self, ticket_id: str):
        with self.get_session() as session:
            return (
                session.query(StargateBusRode)
                .filter(StargateBusRode.ticket_id == ticket_id)
                .first()
            )

    def event_exists(self, transaction_hash: str, ticket_id: str):
        with self.get_session() as session:
            return (
                session.query(StargateBusRode)
                .filter(
                    StargateBusRode.transaction_hash == transaction_hash,
                    StargateBusRode.ticket_id == ticket_id,
                )
                .first()
            )


class StargateBusDrivenRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(StargateBusDriven, session_factory)

    def get_by_transaction_hash(self, transaction_hash: str):
        with self.get_session() as session:
            return (
                session.query(StargateBusDriven)
                .filter(StargateBusDriven.transaction_hash == transaction_hash)
                .first()
            )

    def event_exists(self, guid: str):
        with self.get_session() as session:
            return session.query(StargateBusDriven).filter(StargateBusDriven.guid == guid).first()


class StargatePacketSentRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(StargatePacketSent, session_factory)

    def event_exists(self, guid: str):
        with self.get_session() as session:
            return session.query(StargatePacketSent).filter(StargatePacketSent.guid == guid).first()


class StargatePacketReceivedRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(StargatePacketReceived, session_factory)

    def get_by_nonce(self, nonce: int):
        with self.get_session() as session:
            return (
                session.query(StargatePacketReceived)
                .filter(StargatePacketReceived.nonce == nonce)
                .first()
            )

    def event_exists(self, transaction_hash: str):
        with self.get_session() as session:
            return (
                session.query(StargatePacketReceived)
                .filter(StargatePacketReceived.transaction_hash == transaction_hash)
                .first()
            )


class StargatePacketRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(StargatePacket, session_factory)

    def get_by_transaction_hash(self, transaction_hash: str):
        with self.get_session() as session:
            return (
                session.query(StargatePacket)
                .filter(StargatePacket.transaction_hash == transaction_hash)
                .first()
            )

    def event_exists(self, transaction_hash: str, dst_blockchain: str, nonce: int):
        with self.get_session() as session:
            return (
                session.query(StargatePacket)
                .filter(
                    StargatePacket.transaction_hash == transaction_hash,
                    StargatePacket.dst_blockchain == dst_blockchain,
                    StargatePacket.nonce == nonce,
                )
                .first()
            )


class StargatePacketDeliveredRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(StargatePacketDelivered, session_factory)

    def get_by_nonce(self, nonce: int):
        with self.get_session() as session:
            return (
                session.query(StargatePacketDelivered)
                .filter(StargatePacketDelivered.nonce == nonce)
                .first()
            )

    def event_exists(self, transaction_hash: str):
        with self.get_session() as session:
            return (
                session.query(StargatePacketDelivered)
                .filter(StargatePacketDelivered.transaction_hash == transaction_hash)
                .first()
            )


class StargatePacketVerifiedRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(StargatePacketVerified, session_factory)

    def event_exists(self, transaction_hash: str):
        with self.get_session() as session:
            return (
                session.query(StargatePacketVerified)
                .filter(StargatePacketVerified.transaction_hash == transaction_hash)
                .first()
            )


class StargatePayloadVerifiedRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(StargatePayloadVerified, session_factory)

    def event_exists(self, transaction_hash: str):
        with self.get_session() as session:
            return (
                session.query(StargatePayloadVerified)
                .filter(StargatePayloadVerified.transaction_hash == transaction_hash)
                .first()
            )


class StargateSwapRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(StargateSwap, session_factory)


class StargateSwapRemoteRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(StargateSwapRemote, session_factory)

    def get_by_transaction_hash(self, transaction_hash: str):
        with self.get_session() as session:
            return (
                session.query(StargateSwapRemote)
                .filter(StargateSwapRemote.transaction_hash == transaction_hash)
                .first()
            )

    def event_exists(self, transaction_hash: str):
        with self.get_session() as session:
            return (
                session.query(StargateSwapRemote)
                .filter(StargateSwapRemote.transaction_hash == transaction_hash)
                .first()
            )


class StargateComposeSentRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(StargateComposeSent, session_factory)

    def event_exists(self, guid: str):
        with self.get_session() as session:
            return (
                session.query(StargateComposeSent).filter(StargateComposeSent.guid == guid).first()
            )


class StargateComposeDeliveredRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(StargateComposeDelivered, session_factory)

    def event_exists(self, guid: str):
        with self.get_session() as session:
            return (
                session.query(StargateComposeDelivered)
                .filter(StargateComposeDelivered.guid == guid)
                .first()
            )


class StargateVerifierFeeRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(StargateVerifierFee, session_factory)

    def get_by_transaction_hash(self, transaction_hash: str):
        with self.get_session() as session:
            return (
                session.query(StargateVerifierFee)
                .filter(StargateVerifierFee.transaction_hash == transaction_hash)
                .first()
            )


class StargateRelayerFeeRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(StargateRelayerFee, session_factory)

    def get_by_transaction_hash(self, transaction_hash: str):
        with self.get_session() as session:
            return (
                session.query(StargateRelayerFee)
                .filter(StargateRelayerFee.transaction_hash == transaction_hash)
                .first()
            )


class StargateBlockchainTransactionRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(StargateBlockchainTransaction, session_factory)

    def get_transaction_by_hash(self, transaction_hash: str):
        with self.get_session() as session:
            return session.get(StargateBlockchainTransaction, transaction_hash)

    def get_min_timestamp(self):
        with self.get_session() as session:
            return session.query(func.min(StargateBlockchainTransaction.timestamp)).scalar()

    def get_max_timestamp(self):
        with self.get_session() as session:
            return session.query(func.max(StargateBlockchainTransaction.timestamp)).scalar()


########## Processed Data ##########


class StargateBusCrossChainTransactionRepository(CrossChainRepository):
    def __init__(self, session_factory):
        super().__init__(StargateBusCrossChainTransaction, session_factory)

    def get_number_of_records(self):
        with self.get_session() as session:
            return session.query(func.count(StargateBusCrossChainTransaction.id)).scalar()

    def empty_table(self):
        with self.get_session() as session:
            return session.query(StargateBusCrossChainTransaction).delete()

    # select src_blockchain, src_contract_address, dst_blockchain, dst_contract_address
    # from stargate_bus_cross_chain_transactions group by src_contract_address, dst_contract_address
    def get_unique_src_dst_contract_pairs(self):
        with self.get_session() as session:
            return (
                session.query(
                    StargateBusCrossChainTransaction.src_blockchain,
                    StargateBusCrossChainTransaction.src_contract_address,
                    StargateBusCrossChainTransaction.dst_blockchain,
                    StargateBusCrossChainTransaction.dst_contract_address,
                )
                .group_by(
                    StargateBusCrossChainTransaction.src_blockchain,
                    StargateBusCrossChainTransaction.src_contract_address,
                    StargateBusCrossChainTransaction.dst_blockchain,
                    StargateBusCrossChainTransaction.dst_contract_address,
                )
                .all()
            )

    def get_total_amount_usd_transacted(self):
        with self.get_session() as session:
            return session.query(
                func.sum(StargateBusCrossChainTransaction.amount_received_ld_usd)
            ).scalar()


class StargateCrossChainSwapRepository(CrossChainRepository):
    def __init__(self, session_factory):
        super().__init__(StargateCrossChainSwap, session_factory)

    def get_number_of_records(self):
        with self.get_session() as session:
            return session.query(func.count(StargateCrossChainSwap.id)).scalar()

    def empty_table(self):
        with self.get_session() as session:
            return session.query(StargateCrossChainSwap).delete()

    # select src_blockchain, src_contract_address, dst_blockchain, dst_contract_address
    # from stargate_bus_cross_chain_transactions group by src_contract_address, dst_contract_address
    def get_unique_src_dst_contract_pairs(self):
        with self.get_session() as session:
            return (
                session.query(
                    StargateCrossChainSwap.src_blockchain,
                    StargateCrossChainSwap.src_contract_address,
                    StargateCrossChainSwap.dst_blockchain,
                    StargateCrossChainSwap.dst_contract_address,
                )
                .group_by(
                    StargateCrossChainSwap.src_blockchain,
                    StargateCrossChainSwap.src_contract_address,
                    StargateCrossChainSwap.dst_blockchain,
                    StargateCrossChainSwap.dst_contract_address,
                )
                .all()
            )

    def get_total_amount_usd_transacted(self):
        with self.get_session() as session:
            return session.query(func.sum(StargateCrossChainSwap.amount_usd)).scalar()


class StargateOFTCrossChainTransactionRepository(CrossChainRepository):
    def __init__(self, session_factory):
        super().__init__(StargateOFTCrossChainTransaction, session_factory)

    def get_number_of_records(self):
        with self.get_session() as session:
            return session.query(func.count(StargateOFTCrossChainTransaction.id)).scalar()

    def empty_table(self):
        with self.get_session() as session:
            return session.query(StargateOFTCrossChainTransaction).delete()

    def get_unique_src_dst_contract_pairs(self):
        with self.get_session() as session:
            return (
                session.query(
                    StargateOFTCrossChainTransaction.src_blockchain,
                    StargateOFTCrossChainTransaction.src_contract_address,
                    StargateOFTCrossChainTransaction.dst_blockchain,
                    StargateOFTCrossChainTransaction.dst_contract_address,
                )
                .group_by(
                    StargateOFTCrossChainTransaction.src_blockchain,
                    StargateOFTCrossChainTransaction.src_contract_address,
                    StargateOFTCrossChainTransaction.dst_blockchain,
                    StargateOFTCrossChainTransaction.dst_contract_address,
                )
                .all()
            )

    def get_total_amount_usd_transacted(self):
        with self.get_session() as session:
            return session.query(func.sum(StargateOFTCrossChainTransaction.amount_usd)).scalar()


class StargateCrossChainTokenTransferRepository(CrossChainRepository):
    def __init__(self, session_factory):
        super().__init__(StargateCrossChainTokenTransfers, session_factory)

    def get_number_of_records(self):
        with self.get_session() as session:
            return session.query(func.count(StargateCrossChainTokenTransfers.id)).scalar()

    def empty_table(self):
        with self.get_session() as session:
            return session.query(StargateCrossChainTokenTransfers).delete()

    def get_unique_src_dst_contract_pairs(self):
        with self.get_session() as session:
            return (
                session.query(
                    StargateCrossChainTokenTransfers.src_blockchain,
                    StargateCrossChainTokenTransfers.src_contract_address,
                    StargateCrossChainTokenTransfers.dst_blockchain,
                    StargateCrossChainTokenTransfers.dst_contract_address,
                )
                .group_by(
                    StargateCrossChainTokenTransfers.src_blockchain,
                    StargateCrossChainTokenTransfers.src_contract_address,
                    StargateCrossChainTokenTransfers.dst_blockchain,
                    StargateCrossChainTokenTransfers.dst_contract_address,
                )
                .all()
            )

    def get_total_amount_usd_transacted(self):
        with self.get_session() as session:
            return session.query(func.sum(StargateCrossChainTokenTransfers.amount_usd)).scalar()


########## Indexes ##########

Index(
    "ix_bus_driven_blockchain_tx", StargateBusDriven.blockchain, StargateBusDriven.transaction_hash
)
Index(
    "ix_bus_driven_ticket_range",
    StargateBusDriven.start_ticket_id,
    StargateBusDriven.num_passengers,
)
Index("ix_bus_rode_blockchain_tx", StargateBusRode.blockchain, StargateBusRode.transaction_hash)
Index("ix_bus_rode_ticket_id", StargateBusRode.ticket_id)
Index("ix_oft_sent_tx_blockchain", StargateOFTSent.transaction_hash, StargateOFTSent.blockchain)
Index("ix_oft_sent_from_address", StargateOFTSent.from_address)
Index("ix_blockchain_transactions_tx", StargateBlockchainTransaction.transaction_hash)
Index(
    "ix_oft_received_to_address_blockchain",
    StargateOFTReceived.to_address,
    StargateOFTReceived.blockchain,
)
Index("ix_executor_fee_paid_transaction_hash", StargateExecutorFeePaid.transaction_hash)
Index("ix_dvn_fee_paid_transaction_hash", StargateDVNFeePaid.transaction_hash)
Index(
    "ix_bus_cross_chain_transaction_transaction_hash",
    StargateBusCrossChainTransaction.user_transaction_hash,
    StargateBusCrossChainTransaction.dst_transaction_hash,
)
Index("ix_packet_nonce", StargatePacket.nonce, StargatePacket.transaction_hash)
Index(
    "ix_packet_received_nonce",
    StargatePacketReceived.nonce,
    StargatePacketReceived.transaction_hash,
)


Index(
    "ix_packet",
    StargatePacket.transaction_hash,
    StargatePacket.dst_blockchain,
    StargatePacket.nonce,
)
Index("ix_packet_delivered_transaction_hash", StargatePacketDelivered.transaction_hash)
Index("ix_payload_verified_transaction_hash", StargatePayloadVerified.transaction_hash)
Index("ix_packet_verified_transaction_hash", StargatePacketVerified.transaction_hash)
Index("ix_packet_received_transaction_hash", StargatePacketReceived.transaction_hash)
Index(
    "ix_uln_config_set_transaction_hash",
    StargateUlnConfigSet.transaction_hash,
    StargateUlnConfigSet.dst_blockchain,
    StargateUlnConfigSet.oapp,
)
Index(
    "ix_oft_sent_transaction_hash",
    StargateOFTSent.transaction_hash,
    StargateOFTSent.guid,
    StargateOFTSent.amount_received_ld,
)
Index(
    "ix_oft_send_to_chain_transaction_hash",
    StargateOFTSendToChain.transaction_hash,
    StargateOFTSendToChain.dst_blockchain,
)
Index(
    "ix_oft_receive_from_chain_transaction_hash",
    StargateOFTReceiveFromChain.transaction_hash,
    StargateOFTReceiveFromChain.src_blockchain,
)
Index("ix_bus_rode_transaction_hash", StargateBusRode.transaction_hash, StargateBusRode.ticket_id)
Index("ix_bus_driven_guid", StargateBusDriven.guid)
Index("ix_swap_remote_transaction_hash", StargateSwapRemote.transaction_hash)
Index("ix_compose_sent_guid", StargateComposeSent.guid)
Index("ix_compose_delivered_guid", StargateComposeDelivered.guid)
