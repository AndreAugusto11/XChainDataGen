from sqlalchemy import BigInteger, Column, Float, Integer, Numeric, String

from repository.common.models import BlockchainTransaction
from repository.database import Base


class AcrossRelayerRefund(Base):
    __tablename__ = "across_relayer_refund"

    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    blockchain = Column(String(10), nullable=False)
    transaction_hash = Column(String(66), nullable=False)
    root_bundle_id = Column(Integer, nullable=False)
    amount_to_return = Column(Numeric(30, 0), nullable=False)
    refund_amount = Column(Numeric(30, 0), nullable=False)
    l2_token_address = Column(String(42), nullable=False)
    refund_address = Column(String(42), nullable=False)
    caller = Column(String(42), nullable=False)

    def __init__(
        self,
        blockchain,
        transaction_hash,
        root_bundle_id,
        amount_to_return,
        refund_amount,
        l2_token_address,
        refund_address,
        caller,
    ):
        self.blockchain = blockchain
        self.transaction_hash = transaction_hash
        self.root_bundle_id = root_bundle_id
        self.amount_to_return = amount_to_return
        self.refund_amount = refund_amount
        self.l2_token_address = l2_token_address
        self.refund_address = refund_address
        self.caller = caller

    def __repr__(self):
        return (
            f"<AcrossRelayerRefund(blockchain={self.blockchain}, "
            f"transaction_hash={self.transaction_hash}, "
            f"root_bundle_id={self.root_bundle_id}, "
            f"amount_to_return={self.amount_to_return}, "
            f"refund_amount={self.refund_amount}, "
            f"l2_token_address={self.l2_token_address}, "
            f"refund_address={self.refund_address}, "
            f"caller={self.caller})>"
        )


class AcrossFilledV3Relay(Base):
    __tablename__ = "across_filled_v3_relay"

    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    blockchain = Column(String(10), nullable=False)
    transaction_hash = Column(String(66), nullable=False)
    src_chain = Column(String(10), nullable=False)
    deposit_id = Column(Integer, nullable=False)
    relayer = Column(String(42), nullable=False)
    input_token = Column(String(42), nullable=False)
    output_token = Column(String(42), nullable=False)
    input_amount = Column(Numeric(30, 0), nullable=False)
    output_amount = Column(Numeric(30, 0), nullable=False)
    repayment_chain = Column(String(10), nullable=False)
    fill_deadline = Column(BigInteger, nullable=False)
    exclusivity_deadline = Column(BigInteger, nullable=False)
    exclusive_relayer = Column(String(42), nullable=False)
    depositor = Column(String(42), nullable=False)
    recipient = Column(String(42), nullable=False)
    message = Column(String(10000), nullable=True)
    updated_recipient = Column(String(42), nullable=False)
    updated_message = Column(String(10000), nullable=True)
    updated_output_amount = Column(String(30), nullable=False)
    fill_type = Column(Integer, nullable=False)

    def __init__(
        self,
        blockchain,
        transaction_hash,
        src_chain,
        deposit_id,
        relayer,
        input_token,
        output_token,
        input_amount,
        output_amount,
        repayment_chain,
        fill_deadline,
        exclusivity_deadline,
        exclusive_relayer,
        depositor,
        recipient,
        message,
        updated_recipient,
        updated_message,
        updated_output_amount,
        fill_type,
    ):
        self.blockchain = blockchain
        self.transaction_hash = transaction_hash
        self.src_chain = src_chain
        self.deposit_id = deposit_id
        self.relayer = relayer
        self.input_token = input_token
        self.output_token = output_token
        self.input_amount = input_amount
        self.output_amount = output_amount
        self.repayment_chain = repayment_chain
        self.fill_deadline = fill_deadline
        self.exclusivity_deadline = exclusivity_deadline
        self.exclusive_relayer = exclusive_relayer
        self.depositor = depositor
        self.recipient = recipient
        self.message = message
        self.updated_recipient = updated_recipient
        self.updated_message = updated_message
        self.updated_output_amount = updated_output_amount
        self.fill_type = fill_type

    def __repr__(self):
        return (
            f"<AcrossFilledV3Relay(blockchain={self.blockchain},"
            f"transaction_hash={self.transaction_hash}, "
            f"src_chain={self.src_chain}, "
            f"deposit_id={self.deposit_id}, "
            f"relayer={self.relayer}, "
            f"input_token={self.input_token}, "
            f"output_token={self.output_token}, "
            f"input_amount={self.input_amount}, "
            f"output_amount={self.output_amount}, "
            f"repayment_chain={self.repayment_chain}, "
            f"fill_deadline={self.fill_deadline}, "
            f"exclusivity_deadline={self.exclusivity_deadline}, "
            f"exclusive_relayer={self.exclusive_relayer}, "
            f"depositor={self.depositor}, "
            f"recipient={self.recipient}, "
            f"message={self.message}, "
            f"updated_recipient={self.updated_recipient}, "
            f"updated_message={self.updated_message}, "
            f"updated_output_amount={self.updated_output_amount}, "
            f"fill_type={self.fill_type})>"
        )


class AcrossV3FundsDeposited(Base):
    __tablename__ = "across_v3_funds_deposited"

    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    blockchain = Column(String(10), nullable=False)
    transaction_hash = Column(String(66), nullable=False)
    destination_chain = Column(String(24), nullable=False)
    deposit_id = Column(Integer, nullable=False)
    depositor = Column(String(42), nullable=False)
    input_token = Column(String(42), nullable=False)
    output_token = Column(String(42), nullable=False)
    input_amount = Column(Numeric(30, 0), nullable=False)
    output_amount = Column(Numeric(30, 0), nullable=False)
    quote_timestamp = Column(BigInteger, nullable=False)
    fill_deadline = Column(BigInteger, nullable=False)
    exclusivity_deadline = Column(BigInteger, nullable=False)
    recipient = Column(String(42), nullable=False)
    exclusive_relayer = Column(String(42), nullable=False)
    message = Column(String, nullable=True)

    def __init__(
        self,
        blockchain,
        transaction_hash,
        destination_chain,
        deposit_id,
        depositor,
        input_token,
        output_token,
        input_amount,
        output_amount,
        quote_timestamp,
        fill_deadline,
        exclusivity_deadline,
        recipient,
        exclusive_relayer,
        message,
    ):
        self.blockchain = blockchain
        self.transaction_hash = transaction_hash
        self.destination_chain = destination_chain
        self.deposit_id = deposit_id
        self.depositor = depositor
        self.input_token = input_token
        self.output_token = output_token
        self.input_amount = input_amount
        self.output_amount = output_amount
        self.quote_timestamp = quote_timestamp
        self.fill_deadline = fill_deadline
        self.exclusivity_deadline = exclusivity_deadline
        self.recipient = recipient
        self.exclusive_relayer = exclusive_relayer
        self.message = message

    def __repr__(self):
        return (
            f"<AcrossV3FundsDeposited(blockchain={self.blockchain},"
            f"transaction_hash={self.transaction_hash}, "
            f"destination_chain={self.destination_chain}, "
            f"deposit_id={self.deposit_id}, "
            f"depositor={self.depositor}, "
            f"input_token={self.input_token}, "
            f"output_token={self.output_token}, "
            f"input_amount={self.input_amount}, "
            f"output_amount={self.output_amount}, "
            f"quote_timestamp={self.quote_timestamp}, "
            f"fill_deadline={self.fill_deadline}, "
            f"exclusivity_deadline={self.exclusivity_deadline}, "
            f"recipient={self.recipient}, "
            f"exclusive_relayer={self.exclusive_relayer}, message={self.message})>"
        )


class AcrossBlockchainTransaction(BlockchainTransaction):
    __tablename__ = "across_blockchain_transactions"

    def __repr__(self):
        return (
            f"<AcrossBlockchainTransaction(blockchain={self.blockchain},"
            f"transaction_hash={self.transaction_hash}, block_number={self.block_number}, "
            f"timestamp={self.timestamp} from_address={self.from_address}, "
            f"to_address={self.to_address}, status={self.status})>"
        )


########## Processed Data ##########


class AcrossCrossChainTransaction(Base):
    __tablename__ = "across_cross_chain_transactions"

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
    input_amount = Column(Numeric(30, 0), nullable=False)
    input_amount_usd = Column(Float, nullable=True)
    output_amount = Column(Numeric(30, 0), nullable=False)
    output_amount_usd = Column(Float, nullable=True)
    quote_timestamp = Column(BigInteger, nullable=False)
    fill_deadline = Column(BigInteger, nullable=False)
    exclusivity_deadline = Column(BigInteger, nullable=False)
    exclusive_relayer = Column(String(42), nullable=False)
    fill_type = Column(BigInteger, nullable=False)

    def __init__(
        self,
        src_blockchain,
        src_transaction_hash,
        src_timestamp,
        src_from_address,
        src_to_address,
        src_fee,
        dst_blockchain,
        dst_transaction_hash,
        dst_timestamp,
        dst_from_address,
        dst_to_address,
        dst_fee,
        deposit_id,
        depositor,
        recipient,
        src_contract_address,
        dst_contract_address,
        input_amount,
        output_amount,
        quote_timestamp,
        fill_deadline,
        exclusivity_deadline,
        exclusive_relayer,
        fill_type,
    ):
        self.src_blockchain = src_blockchain
        self.src_transaction_hash = src_transaction_hash
        self.src_timestamp = src_timestamp
        self.src_from_address = src_from_address
        self.src_to_address = src_to_address
        self.src_fee = src_fee
        self.dst_blockchain = dst_blockchain
        self.dst_transaction_hash = dst_transaction_hash
        self.dst_timestamp = dst_timestamp
        self.dst_from_address = dst_from_address
        self.dst_to_address = dst_to_address
        self.dst_fee = dst_fee
        self.deposit_id = deposit_id
        self.depositor = depositor
        self.recipient = recipient
        self.src_contract_address = src_contract_address
        self.dst_contract_address = dst_contract_address
        self.input_amount = input_amount
        self.output_amount = output_amount
        self.quote_timestamp = quote_timestamp
        self.fill_deadline = fill_deadline
        self.exclusivity_deadline = exclusivity_deadline
        self.exclusive_relayer = exclusive_relayer
        self.fill_type = fill_type

    def __repr__(self):
        return (
            f"<AcrossCrossChainTransaction(src_blockchain={self.src_blockchain},"
            f"src_transaction_hash={self.src_transaction_hash}, "
            f"src_timestamp={self.src_timestamp}, "
            f"src_from_address={self.src_from_address}, "
            f"src_to_address={self.src_to_address}, "
            f"src_fee={self.src_fee}, "
            f"dst_blockchain={self.dst_blockchain}, "
            f"dst_transaction_hash={self.dst_transaction_hash}, "
            f"dst_timestamp={self.dst_timestamp}, "
            f"dst_from_address={self.dst_from_address}, "
            f"dst_to_address={self.dst_to_address}, "
            f"dst_fee={self.dst_fee}, "
            f"deposit_id={self.deposit_id}, "
            f"depositor={self.depositor}, "
            f"recipient={self.recipient}, "
            f"src_contract_address={self.src_contract_address}, "
            f"dst_contract_address={self.dst_contract_address}, "
            f"input_amount={self.input_amount}, "
            f"output_amount={self.output_amount}, "
            f"quote_timestamp={self.quote_timestamp}, "
            f"fill_deadline={self.fill_deadline}, "
            f"exclusivity_deadline={self.exclusivity_deadline}, "
            f"exclusive_relayer={self.exclusive_relayer}, "
            f"fill_type={self.fill_type})>"
        )
