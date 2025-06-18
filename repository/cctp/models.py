from sqlalchemy import BigInteger, Column, Float, Integer, Numeric, String

from repository.common.models import BlockchainTransaction
from repository.database import Base


class CCTPDepositForBurn(Base):
    __tablename__ = "cctp_deposit_for_burn"

    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    blockchain = Column(String(10), nullable=False)
    transaction_hash = Column(String(66), nullable=False)
    nonce = Column(Integer, nullable=False)
    depositor = Column(String(42), nullable=False)
    burn_token = Column(String(42), nullable=False)
    recipient = Column(String(42), nullable=False)
    dst_blockchain = Column(String(10), nullable=False)
    amount = Column(Numeric(30, 0), nullable=False)

    def __init__(
        self,
        blockchain,
        transaction_hash,
        nonce,
        depositor,
        burn_token,
        recipient,
        dst_blockchain,
        amount,
    ):
        self.blockchain = blockchain
        self.transaction_hash = transaction_hash
        self.nonce = nonce
        self.depositor = depositor
        self.burn_token = burn_token
        self.recipient = recipient
        self.dst_blockchain = dst_blockchain
        self.amount = amount

    def __repr__(self):
        return (
            f"<CCTPDepositForBurn {self.blockchain}, "
            f"{self.transaction_hash}, "
            f"{self.nonce}, "
            f"{self.depositor}, "
            f"{self.burn_token}, "
            f"{self.recipient}, "
            f"{self.dst_blockchain}, "
            f"{self.amount}>"
        )


class CCTPMessageReceived(Base):
    __tablename__ = "cctp_message_received"

    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    blockchain = Column(String(10), nullable=False)
    transaction_hash = Column(String(66), nullable=False)
    nonce = Column(Integer, nullable=False)
    src_blockchain = Column(String(10), nullable=False)
    input_token = Column(String(42), nullable=False)
    depositor = Column(String(42), nullable=False)
    recipient = Column(String(42), nullable=False)
    amount = Column(Numeric(30, 0), nullable=False)

    def __init__(
        self,
        blockchain,
        transaction_hash,
        nonce,
        src_blockchain,
        input_token,
        depositor,
        recipient,
        amount,
    ):
        self.blockchain = blockchain
        self.transaction_hash = transaction_hash
        self.nonce = nonce
        self.src_blockchain = src_blockchain
        self.input_token = input_token
        self.depositor = depositor
        self.recipient = recipient
        self.amount = amount

    def __repr__(self):
        return (
            f"<CCTPMessageReceived {self.blockchain}, "
            f"{self.transaction_hash}, "
            f"{self.nonce}, "
            f"{self.src_blockchain}, "
            f"{self.input_token}, "
            f"{self.depositor}, "
            f"{self.recipient}, "
            f"{self.amount}>"
        )


class CCTPBlockchainTransaction(BlockchainTransaction):
    __tablename__ = "cctp_blockchain_transactions"

    def __repr__(self):
        return (
            f"<CCTPBlockchainTransaction(blockchain={self.blockchain}, "
            f"transaction_hash={self.transaction_hash}, "
            f"block_number={self.block_number}, "
            f"timestamp={self.timestamp} from_address={self.from_address}, "
            f"to_address={self.to_address}, "
            f"status={self.status})>"
        )


######### Processed Data ##########


class CctpCrossChainTransactions(Base):
    __tablename__ = "cctp_cross_chain_transactions"

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
        self.amount = amount
        self.amount_usd = amount_usd
