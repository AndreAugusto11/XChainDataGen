from sqlalchemy import BigInteger, Column, Float, Integer, Numeric, String

from repository.common.models import BlockchainTransaction
from repository.database import Base


class MayanSwapAndForwarded(Base):
    __tablename__ = "mayan_swap_and_forwarded"

    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    blockchain = Column(String(10), nullable=False)
    transaction_hash = Column(String(66), nullable=False)
    token_in = Column(String(42), nullable=False)
    amount_in = Column(Numeric(30, 0), nullable=False)
    swap_protocol = Column(String(42), nullable=False)
    middle_token = Column(String(42), nullable=False)
    middle_amount = Column(Numeric(30, 0), nullable=False)
    mayan_protocol = Column(String(42), nullable=False)
    trader = Column(String(42), nullable=False)
    token_out = Column(String(42), nullable=False)
    min_amount_out = Column(Numeric(30, 0), nullable=False)
    gas_drop = Column(Integer, nullable=True)
    cancel_fee = Column(Integer, nullable=True)
    refund_fee = Column(Integer, nullable=True)
    deadline = Column(BigInteger, nullable=True)
    dst_addr = Column(String(42), nullable=True)
    dst_chain = Column(String(10), nullable=True)
    referrer_addr = Column(String(42), nullable=True)
    referrer_bps = Column(Integer, nullable=True)
    auction_mode = Column(Integer, nullable=True)
    random = Column(String(66), nullable=True)

    def __init__(
        self,
        blockchain,
        transaction_hash,
        token_in,
        amount_in,
        swap_protocol,
        middle_token,
        middle_amount,
        mayan_protocol,
        trader,
        token_out,
        min_amount_out,
        gas_drop,
        cancel_fee,
        refund_fee,
        deadline,
        dst_addr,
        dst_chain,
        referrer_addr,
        referrer_bps,
        auction_mode,
        random,
    ):
        self.blockchain = blockchain
        self.transaction_hash = transaction_hash
        self.token_in = token_in
        self.amount_in = amount_in
        self.swap_protocol = swap_protocol
        self.middle_token = middle_token
        self.middle_amount = middle_amount
        self.mayan_protocol = mayan_protocol
        self.trader = trader
        self.token_out = token_out
        self.min_amount_out = min_amount_out
        self.gas_drop = gas_drop
        self.cancel_fee = cancel_fee
        self.refund_fee = refund_fee
        self.deadline = deadline
        self.dst_addr = dst_addr
        self.dst_chain = dst_chain
        self.referrer_addr = referrer_addr
        self.referrer_bps = referrer_bps
        self.auction_mode = auction_mode
        self.random = random

    def __repr__(self):
        return (
            f"<MayanSwapAndForwarded(blockchain={self.blockchain}, "
            f"transaction_hash={self.transaction_hash}, "
            f"token_in={self.token_in}, "
            f"amount_in={self.amount_in}, "
            f"swap_protocol={self.swap_protocol}, "
            f"middle_token={self.middle_token}, "
            f"middle_amount={self.middle_amount}, "
            f"mayan_protocol={self.mayan_protocol}, "
            f"trader={self.trader}, "
            f"token_out={self.token_out}, "
            f"min_amount_out={self.min_amount_out}, "
            f"gas_drop={self.gas_drop}, "
            f"cancel_fee={self.cancel_fee}, "
            f"refund_fee={self.refund_fee}, "
            f"deadline={self.deadline}, "
            f"dst_addr={self.dst_addr}, "
            f"dst_chain={self.dst_chain}, "
            f"referrer_addr={self.referrer_addr}, "
            f"referrer_bps={self.referrer_bps}, "
            f"auction_mode={self.auction_mode}, "
            f"random={self.random})>"
        )


class MayanForwarded(Base):
    __tablename__ = "mayan_forwarded"

    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    blockchain = Column(String(10), nullable=False)
    transaction_hash = Column(String(66), nullable=False)
    token = Column(String(42), nullable=False)
    amount = Column(Numeric(30, 0), nullable=True)
    mayan_protocol = Column(String(42), nullable=False)
    trader = Column(String(42), nullable=False)
    token_out = Column(String(42), nullable=False)
    min_amount_out = Column(Numeric(30, 0), nullable=False)
    gas_drop = Column(Integer, nullable=True)
    cancel_fee = Column(Integer, nullable=True)
    refund_fee = Column(Integer, nullable=True)
    deadline = Column(BigInteger, nullable=True)
    dst_addr = Column(String(42), nullable=True)
    dst_chain = Column(String(10), nullable=True)
    referrer_addr = Column(String(42), nullable=True)
    referrer_bps = Column(Integer, nullable=True)
    auction_mode = Column(Integer, nullable=True)
    random = Column(String(66), nullable=True)

    def __init__(
        self,
        blockchain,
        transaction_hash,
        token,
        amount,
        mayan_protocol,
        trader,
        token_out,
        min_amount_out,
        gas_drop,
        cancel_fee,
        refund_fee,
        deadline,
        dst_addr,
        dst_chain,
        referrer_addr,
        referrer_bps,
        auction_mode,
        random,
    ):
        self.blockchain = blockchain
        self.transaction_hash = transaction_hash
        self.token = token
        self.amount = amount
        self.mayan_protocol = mayan_protocol
        self.trader = trader
        self.token_out = token_out
        self.min_amount_out = min_amount_out
        self.gas_drop = gas_drop
        self.cancel_fee = cancel_fee
        self.refund_fee = refund_fee
        self.deadline = deadline
        self.dst_addr = dst_addr
        self.dst_chain = dst_chain
        self.referrer_addr = referrer_addr
        self.referrer_bps = referrer_bps
        self.auction_mode = auction_mode
        self.random = random

    def __repr__(self):
        return (
            f"<MayanForwarded(blockchain={self.blockchain}, "
            f"transaction_hash={self.transaction_hash}, "
            f"token={self.token}, "
            f"amount={self.amount}, "
            f"mayan_protocol={self.mayan_protocol}, "
            f"trader={self.trader}, "
            f"token_out={self.token_out}, "
            f"min_amount_out={self.min_amount_out}, "
            f"gas_drop={self.gas_drop}, "
            f"cancel_fee={self.cancel_fee}, "
            f"refund_fee={self.refund_fee}, "
            f"deadline={self.deadline}, "
            f"dst_addr={self.dst_addr}, "
            f"dst_chain={self.dst_chain}, "
            f"referrer_addr={self.referrer_addr}, "
            f"referrer_bps={self.referrer_bps}, "
            f"auction_mode={self.auction_mode}, "
            f"random={self.random})>"
        )


class MayanOrderCreated(Base):
    __tablename__ = "mayan_order_created"

    key = Column(String(64), nullable=False, primary_key=True)
    blockchain = Column(String(10), nullable=False)
    transaction_hash = Column(String(66), nullable=False)

    def __init__(self, key, blockchain, transaction_hash):
        self.key = key
        self.blockchain = (blockchain,)
        self.transaction_hash = transaction_hash

    def __repr__(self):
        return (
            f"<MayanOrderCreated(key={self.key}, "
            f"blockchain={self.blockchain}, "
            f"transaction_hash={self.transaction_hash})>"
        )


class MayanOrderFulfilled(Base):
    __tablename__ = "mayan_order_fulfilled"

    key = Column(String(64), nullable=False, primary_key=True)
    sequence = Column(Integer, nullable=False)
    net_amount = Column(Numeric(30, 0), nullable=False)
    blockchain = Column(String(10), nullable=False)
    transaction_hash = Column(String(66), nullable=False)

    def __init__(self, key, blockchain, transaction_hash, sequence, net_amount):
        self.key = key
        self.blockchain = (blockchain,)
        self.transaction_hash = transaction_hash
        self.sequence = sequence
        self.net_amount = net_amount

    def __repr__(self):
        return (
            f"<MayanOrderFulfilled(key={self.key}, "
            f"blockchain={self.blockchain}, "
            f"transaction_hash={self.transaction_hash}, "
            f"sequence={self.sequence}, "
            f"net_amount={self.net_amount})>"
        )


class MayanOrderUnlocked(Base):
    __tablename__ = "mayan_order_unlocked"

    key = Column(String(64), nullable=False, primary_key=True)
    blockchain = Column(String(10), nullable=False)
    transaction_hash = Column(String(66), nullable=False)

    def __init__(self, key, blockchain, transaction_hash):
        self.blockchain = (blockchain,)
        self.transaction_hash = transaction_hash
        self.key = key

    def __repr__(self):
        return (
            f"<MayanOrderUnlocked(key={self.key}, "
            f"blockchain={self.blockchain}, "
            f"transaction_hash={self.transaction_hash})>"
        )


class MayanBlockchainTransaction(BlockchainTransaction):
    __tablename__ = "mayan_blockchain_transactions"

    def __repr__(self):
        return (
            f"<MayanBlockchainTransaction(blockchain={self.blockchain}, "
            f"transaction_hash={self.transaction_hash}, "
            f"block_number={self.block_number}, "
            f"timestamp={self.timestamp} from_address={self.from_address}, "
            f"to_address={self.to_address}, "
            f"status={self.status}, "
            f"value={self.value}, "
            f"fee={self.fee})>"
        )


########## Processed Data ##########


class MayanCrossChainTransaction(Base):
    __tablename__ = "mayan_cross_chain_transactions"

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
    deposit_id = Column(BigInteger, nullable=False)
    depositor = Column(String(42), nullable=False)
    recipient = Column(String(42), nullable=False)
    src_contract_address = Column(String(42), nullable=False)
    dst_contract_address = Column(String(42), nullable=False)
    amount = Column(Numeric(30, 0), nullable=False)
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
