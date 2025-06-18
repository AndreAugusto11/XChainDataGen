from sqlalchemy import BigInteger, Boolean, Column, Float, Integer, Numeric, String

from repository.common.models import BlockchainTransaction
from repository.database import Base


class CCIPSendRequested(Base):
    __tablename__ = "ccip_send_requested"

    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    blockchain = Column(String(10), nullable=False)
    transaction_hash = Column(String(66), nullable=False)
    nonce = Column(Integer, nullable=False)
    sender = Column(String(42), nullable=False)
    receiver = Column(String(42), nullable=False)
    sequence_number = Column(Integer, nullable=False)
    gas_limit = Column(Integer, nullable=False)
    strict = Column(Boolean, nullable=False)
    fee_token = Column(String(42), nullable=False)
    fee_token_amount = Column(Numeric(30, 0), nullable=False)
    input_token = Column(String(42), nullable=True)
    output_token = Column(String(42), nullable=True)
    amount = Column(Numeric(30, 0), nullable=True)
    message_id = Column(String(66), nullable=False)

    def __init__(
        self,
        blockchain,
        transaction_hash,
        nonce,
        sender,
        receiver,
        sequence_number,
        gas_limit,
        strict,
        fee_token,
        fee_token_amount,
        input_token,
        output_token,
        amount,
        message_id,
    ):
        self.blockchain = blockchain
        self.transaction_hash = transaction_hash
        self.nonce = nonce
        self.sender = sender
        self.receiver = receiver
        self.sequence_number = sequence_number
        self.gas_limit = gas_limit
        self.strict = strict
        self.fee_token = fee_token
        self.fee_token_amount = fee_token_amount
        self.input_token = input_token
        self.output_token = output_token
        self.amount = amount
        self.message_id = message_id

    def __repr__(self):
        return (
            f"<CCIPSendRequested {self.blockchain}, "
            f"{self.transaction_hash}, "
            f"{self.nonce}, "
            f"{self.sender}, "
            f"{self.receiver}, "
            f"{self.sequence_number}, "
            f"{self.gas_limit}, "
            f"{self.strict}, "
            f"{self.fee_token}, "
            f"{self.fee_token_amount}, "
            f"{self.input_token}, "
            f"{self.output_token}, "
            f"{self.amount}, "
            f"{self.message_id}>"
        )


class CCIPExecutionStateChanged(Base):
    __tablename__ = "ccip_execution_state_changed"

    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    blockchain = Column(String(10), nullable=False)
    transaction_hash = Column(String(66), nullable=False)
    sequence_number = Column(Integer, nullable=False)
    message_id = Column(String(66), nullable=False)
    state = Column(Integer, nullable=False)
    return_data = Column(String(500), nullable=False)

    def __init__(
        self, blockchain, transaction_hash, sequence_number, message_id, state, return_data
    ):
        self.blockchain = blockchain
        self.transaction_hash = transaction_hash
        self.sequence_number = sequence_number
        self.message_id = message_id
        self.state = state
        self.return_data = return_data

    def __repr__(self):
        return (
            f"<CCIPExecutionStateChanged {self.blockchain}, "
            f"{self.transaction_hash}, "
            f"{self.sequence_number}, "
            f"{self.message_id}, "
            f"{self.state}, "
            f"{self.return_data}>"
        )


class CCIPBlockchainTransaction(BlockchainTransaction):
    __tablename__ = "ccip_blockchain_transactions"

    def __repr__(self):
        return (
            f"<CCIPBlockchainTransaction(blockchain={self.blockchain}, "
            f"transaction_hash={self.transaction_hash}, "
            f"block_number={self.block_number}, "
            f"timestamp={self.timestamp} from_address={self.from_address}, "
            f"to_address={self.to_address}, "
            f"status={self.status})>"
        )


######### Processed Data ##########


class CCIPCrossChainTransactions(Base):
    __tablename__ = "ccip_cross_chain_transactions"

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
    fee_token = Column(String(42), nullable=False)
    fee_token_amount = Column(Numeric(30, 0), nullable=False)
    fee_token_amount_usd = Column(Float, nullable=True)
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
