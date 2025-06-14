from sqlalchemy import BigInteger, Column, Float, Integer, Numeric, String

from repository.database import Base


class PortalLogMessagePublished(Base):
    __tablename__ = "portal_log_message_published"

    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    amount = Column(Numeric(30, 0), nullable=False)
    token_address = Column(String(42), nullable=False)
    token_chain = Column(Integer, nullable=False)
    recipient = Column(String(42), nullable=False)
    recipient_chain = Column(String(10), nullable=False)
    fee = Column(Numeric(30, 0), nullable=False)
    nonce = Column(Integer, nullable=False)
    sequence_number = Column(BigInteger, nullable=False)

    def __init__(
        self,
        amount,
        token_address,
        token_chain,
        recipient,
        recipient_chain,
        fee,
        nonce,
        sequence_number,
    ):
        self.amount = amount
        self.token_address = token_address
        self.token_chain = token_chain
        self.recipient = recipient
        self.recipient_chain = recipient_chain
        self.fee = fee
        self.nonce = nonce
        self.sequence_number = sequence_number

    def __repr__(self):
        return (
            f"<PortalLogMessagePublished(amount={self.amount}, "
            f"token_address={self.token_address}, "
            f"token_chain={self.token_chain}, "
            f"recipient={self.recipient}, "
            f"recipient_chain={self.recipient_chain}, "
            f"fee={self.fee}, "
            f"nonce={self.nonce}, "
            f"sequence_number={self.sequence_number})>"
        )


class PortalTransferRedeemed(Base):
    __tablename__ = "portal_transfer_redeemed"

    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    emitter_chain_id = Column(Integer, nullable=False)
    emitter_address = Column(String(42), nullable=False)
    sequence_number = Column(BigInteger, nullable=False)
    data = Column(String, nullable=True)

    def __init__(self, emitter_chain_id, emitter_address, sequence_number, data):
        self.emitter_chain_id = emitter_chain_id
        self.emitter_address = emitter_address
        self.sequence_number = sequence_number
        self.data = data

    def __repr__(self):
        return (
            f"<PortalTransferRedeemed(emitter_chain_id={self.emitter_chain_id}, "
            f"emitter_address={self.emitter_address}, "
            f"sequence_number={self.sequence_number}, "
            f"data={self.data})>"
        )


class PortalBlockchainTransaction(Base):
    __tablename__ = "portal_blockchain_transactions"

    blockchain = Column(String(10), nullable=False)
    transaction_hash = Column(String(66), nullable=False, primary_key=True)
    block_number = Column(Integer, nullable=False)
    timestamp = Column(BigInteger, nullable=False)
    from_address = Column(String(42), nullable=False)
    to_address = Column(String(42), nullable=False)
    status = Column(Integer, nullable=False)
    fee = Column(Numeric(30, 0), nullable=False)

    def __init__(
        self,
        blockchain,
        transaction_hash,
        block_number,
        timestamp,
        from_address,
        to_address,
        status,
        fee,
    ):
        self.blockchain = blockchain
        self.transaction_hash = transaction_hash
        self.block_number = block_number
        self.timestamp = timestamp
        self.from_address = from_address
        self.to_address = to_address
        self.status = status
        self.fee = fee

    def __repr__(self):
        return (
            f"<PortalBlockchainTransaction(blockchain={self.blockchain}, "
            f"transaction_hash={self.transaction_hash}, "
            f"block_number={self.block_number}, "
            f"timestamp={self.timestamp} from_address={self.from_address}, "
            f"to_address={self.to_address}, "
            f"status={self.status})>"
        )


########## Processed Data ##########


class PortalCrossChainTransaction(Base):
    __tablename__ = "portal_cross_chain_transactions"

    id = Column(BigInteger, nullable=False, autoincrement=True, primary_key=True)
    src_blockchain = Column(String(10), nullable=False)
    src_transaction_hash = Column(String(66), nullable=False)
    src_from_address = Column(String(42), nullable=False)
    src_to_address = Column(String(42), nullable=False)
    src_fee = Column(Numeric(30, 0), nullable=False)
    src_fee_usd = Column(Float, nullable=True)
    src_timestamp = Column(BigInteger, nullable=False)
    dst_blockchain = Column(String(10), nullable=False)
    dst_transaction_hash = Column(String(66), nullable=False)
    dst_from_address = Column(String(42), nullable=False)
    dst_to_address = Column(String(42), nullable=False)
    dst_fee = Column(Numeric(30, 0), nullable=False)
    dst_fee_usd = Column(Float, nullable=True)
    dst_timestamp = Column(BigInteger, nullable=False)
    sequence_number = Column(BigInteger, nullable=False)
    depositor = Column(String(42), nullable=False)
    recipient = Column(String(42), nullable=False)
    src_contract_address = Column(String(42), nullable=False)
    amount = Column(Numeric(30, 0), nullable=False)
    fee = Column(Numeric(30, 0), nullable=False)
    fee_usd = Column(Float, nullable=True)
    amount_usd = Column(Float, nullable=True)

    def __init__(
        self,
        src_blockchain,
        src_transaction_hash,
        src_from_address,
        src_to_address,
        src_fee,
        src_fee_usd,
        src_timestamp,
        dst_blockchain,
        dst_transaction_hash,
        dst_from_address,
        dst_to_address,
        dst_fee,
        dst_fee_usd,
        dst_timestamp,
        deposit_id,
        depositor,
        recipient,
        src_contract_address,
        dst_contract_address,
        amount,
        amount_usd,
    ):
        self.src_blockchain = src_blockchain
        self.src_transaction_hash = src_transaction_hash
        self.src_from_address = src_from_address
        self.src_to_address = src_to_address
        self.src_fee = src_fee
        self.src_fee_usd = src_fee_usd
        self.src_timestamp = src_timestamp
        self.dst_blockchain = dst_blockchain
        self.dst_transaction_hash = dst_transaction_hash
        self.dst_from_address = dst_from_address
        self.dst_to_address = dst_to_address
        self.dst_fee = dst_fee
        self.dst_fee_usd = dst_fee_usd
        self.dst_timestamp = dst_timestamp
        self.deposit_id = deposit_id
        self.depositor = depositor
        self.recipient = recipient
        self.src_contract_address = src_contract_address
        self.dst_contract_address = dst_contract_address
        self.amount = amount
        self.amount_usd = amount_usd
