from sqlalchemy import BigInteger, Column, Float, Integer, Numeric, String

from repository.common.models import BlockchainTransaction
from repository.database import Base


class RoninDepositRequested(Base):
    __tablename__ = "ronin_deposit_requested"

    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    blockchain = Column(String(10), nullable=False)
    transaction_hash = Column(String(66), nullable=False)
    deposit_id = Column(Integer, nullable=False)
    kind = Column(String(10), nullable=False)
    depositor = Column(String(42), nullable=False)
    input_token = Column(String(42), nullable=False)
    recipient = Column(String(42), nullable=False)
    output_token = Column(String(42), nullable=False)
    dst_blockchain = Column(String(10), nullable=False)
    token_standard = Column(String(10), nullable=False)
    amount = Column(Numeric(30, 0), nullable=False)

    def __init__(
        self,
        blockchain,
        transaction_hash,
        deposit_id,
        kind,
        depositor,
        input_token,
        recipient,
        output_token,
        dst_blockchain,
        token_standard,
        amount,
    ):
        self.blockchain = blockchain
        self.transaction_hash = transaction_hash
        self.deposit_id = deposit_id
        self.kind = kind
        self.depositor = depositor
        self.input_token = input_token
        self.recipient = recipient
        self.output_token = output_token
        self.dst_blockchain = dst_blockchain
        self.token_standard = token_standard
        self.amount = amount

    def __repr__(self):
        return (
            f"<RoninDepositRequested(blockchain={self.blockchain}, "
            f"transaction_hash={self.transaction_hash}, "
            f"deposit_id={self.deposit_id}, "
            f"kind={self.kind}, "
            f"depositor={self.depositor}, "
            f"input_token={self.input_token}, "
            f"recipient={self.recipient}, "
            f"output_token={self.output_token}, "
            f"dst_blockchain={self.dst_blockchain}, "
            f"token_standard={self.token_standard}, "
            f"amount={self.amount})>"
        )


class RoninTokenDeposited(Base):
    __tablename__ = "ronin_token_deposited"

    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    blockchain = Column(String(10), nullable=False)
    transaction_hash = Column(String(66), nullable=False)
    deposit_id = Column(Integer, nullable=False)
    kind = Column(String(10), nullable=False)
    src_blockchain = Column(String(10), nullable=False)
    depositor = Column(String(42), nullable=False)
    input_token = Column(String(42), nullable=False)
    recipient = Column(String(42), nullable=False)
    output_token = Column(String(42), nullable=False)
    token_standard = Column(String(10), nullable=False)
    amount = Column(Numeric(30, 0), nullable=False)

    def __init__(
        self,
        blockchain,
        transaction_hash,
        deposit_id,
        kind,
        src_blockchain,
        depositor,
        input_token,
        recipient,
        output_token,
        amount,
        token_standard,
    ):
        self.blockchain = blockchain
        self.transaction_hash = transaction_hash
        self.deposit_id = deposit_id
        self.kind = kind
        self.src_blockchain = src_blockchain
        self.depositor = depositor
        self.input_token = input_token
        self.recipient = recipient
        self.output_token = output_token
        self.amount = amount
        self.token_standard = token_standard

    def __repr__(self):
        return (
            f"<RoninTokenDeposited(blockchain={self.blockchain}, "
            f"transaction_hash={self.transaction_hash}, "
            f"deposit_id={self.deposit_id}, "
            f"kind={self.kind}, "
            f"src_blockchain={self.src_blockchain}, "
            f"depositor={self.depositor}, "
            f"input_token={self.input_token}, "
            f"recipient={self.recipient}, "
            f"output_token={self.output_token}, "
            f"amount={self.amount}, "
            f"token_standard={self.token_standard})>"
        )


class RoninWithdrawalRequested(Base):
    __tablename__ = "ronin_withdrawal_requested"

    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    blockchain = Column(String(10), nullable=False)
    transaction_hash = Column(String(66), nullable=False)
    withdrawal_id = Column(Integer, nullable=False)
    kind = Column(String(10), nullable=False)
    withdrawer = Column(String(42), nullable=False)
    input_token = Column(String(42), nullable=False)
    recipient = Column(String(42), nullable=False)
    dst_blockchain = Column(String(10), nullable=False)
    output_token = Column(String(42), nullable=False)
    token_standard = Column(String(10), nullable=False)
    amount = Column(Numeric(30, 0), nullable=False)

    def __init__(
        self,
        blockchain,
        transaction_hash,
        withdrawal_id,
        kind,
        withdrawer,
        input_token,
        recipient,
        dst_blockchain,
        output_token,
        amount,
        token_standard,
    ):
        self.blockchain = blockchain
        self.transaction_hash = transaction_hash
        self.withdrawal_id = withdrawal_id
        self.kind = kind
        self.withdrawer = withdrawer
        self.input_token = input_token
        self.recipient = recipient
        self.dst_blockchain = dst_blockchain
        self.output_token = output_token
        self.amount = amount
        self.token_standard = token_standard

    def __repr__(self):
        return (
            f"<RoninWithdrawalRequested(blockchain={self.blockchain}, "
            f"transaction_hash={self.transaction_hash}, "
            f"withdrawal_id={self.withdrawal_id}, "
            f"kind={self.kind}, "
            f"withdrawer={self.withdrawer}, "
            f"input_token={self.input_token}, "
            f"recipient={self.recipient}, "
            f"dst_blockchain={self.dst_blockchain}, "
            f"output_token={self.output_token}, "
            f"amount={self.amount}, "
            f"token_standard={self.token_standard})>"
        )


class RoninTokenWithdrew(Base):
    __tablename__ = "ronin_token_withdrew"

    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    blockchain = Column(String(10), nullable=False)
    transaction_hash = Column(String(66), nullable=False)
    withdrawal_id = Column(Integer, nullable=False)
    kind = Column(String(10), nullable=False)
    src_blockchain = Column(String(10), nullable=False)
    withdrawer = Column(String(42), nullable=False)
    input_token = Column(String(42), nullable=False)
    recipient = Column(String(42), nullable=False)
    output_token = Column(String(42), nullable=False)
    token_standard = Column(String(10), nullable=False)
    amount = Column(Numeric(30, 0), nullable=False)

    def __init__(
        self,
        blockchain,
        transaction_hash,
        withdrawal_id,
        kind,
        src_blockchain,
        withdrawer,
        input_token,
        recipient,
        output_token,
        amount,
        token_standard,
    ):
        self.blockchain = blockchain
        self.transaction_hash = transaction_hash
        self.withdrawal_id = withdrawal_id
        self.kind = kind
        self.src_blockchain = src_blockchain
        self.withdrawer = withdrawer
        self.input_token = input_token
        self.recipient = recipient
        self.output_token = output_token
        self.amount = amount
        self.token_standard = token_standard

    def __repr__(self):
        return (
            f"<RoninTokenWithdrew(blockchain={self.blockchain}, "
            f"transaction_hash={self.transaction_hash}, "
            f"withdrawal_id={self.withdrawal_id}, "
            f"kind={self.kind}, "
            f"src_blockchain={self.src_blockchain}, "
            f"withdrawer={self.withdrawer}, "
            f"input_token={self.input_token}, "
            f"recipient={self.recipient}, "
            f"output_token={self.output_token}, "
            f"amount={self.amount}, "
            f"token_standard={self.token_standard})>"
        )


class RoninBlockchainTransaction(BlockchainTransaction):
    __tablename__ = "ronin_blockchain_transactions"

    def __repr__(self):
        return (
            f"<RoninBlockchainTransaction(blockchain={self.blockchain}, "
            f"transaction_hash={self.transaction_hash}, "
            f"block_number={self.block_number}, "
            f"timestamp={self.timestamp} from_address={self.from_address}, "
            f"to_address={self.to_address}, "
            f"status={self.status})>"
        )


########## Processed Data ##########


class RoninCrossChainTransaction(Base):
    __tablename__ = "ronin_cross_chain_transactions"

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
