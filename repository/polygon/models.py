from sqlalchemy import (BigInteger, Boolean, Column, Float, Integer, Numeric,
                        String)

from repository.database import Base


class PolygonStateSynced(Base):
    __tablename__ = "polygon_state_synced"

    blockchain            = Column(String(10),     nullable=False)
    transaction_hash      = Column(String(66),     nullable=False)
    state_id              = Column(Integer,        nullable=False, primary_key=True)
    contract_address      = Column(String(42),     nullable=False)
    data                  = Column(String(10000),   nullable=False)

    def __init__(
        self, blockchain, transaction_hash, state_id, contract_address, data
    ):
        self.blockchain = blockchain
        self.transaction_hash = transaction_hash
        self.state_id = state_id
        self.contract_address = contract_address
        self.data = data

    def __repr__(self):
        return f"<PolygonStateSynced {self.blockchain} {self.transaction_hash} {self.state_id} {self.contract_address} {self.data}>"


class PolygonStateCommitted(Base):
    __tablename__ = "polygon_state_comitted"

    blockchain            = Column(String(10),     nullable=False)
    transaction_hash      = Column(String(66),     nullable=False)
    state_id              = Column(Integer,        nullable=False, primary_key=True)
    success               = Column(Boolean,        nullable=False)

    def __init__(
        self, blockchain, transaction_hash, state_id, success
    ):
        self.blockchain = blockchain
        self.transaction_hash = transaction_hash
        self.state_id = state_id
        self.success = success

    def __repr__(self):
        return f"<PolygonStateCommitted {self.blockchain} {self.transaction_hash} {self.state_id} {self.success}>"


class PolygonLockedToken(Base):
    __tablename__ = "polygon_locked_token"

    id                    = Column(Integer,        nullable=False, autoincrement=True, primary_key=True)
    blockchain            = Column(String(10),     nullable=False)
    transaction_hash      = Column(String(66),     nullable=False)
    depositor             = Column(String(42),     nullable=False)
    deposit_receiver      = Column(String(42),     nullable=False)
    root_token            = Column(String(42),     nullable=False)
    amount                = Column(Numeric(30, 0), nullable=False)

    def __init__(
        self, blockchain, transaction_hash, depositor, deposit_receiver, root_token, amount
    ):
        self.blockchain = blockchain
        self.transaction_hash = transaction_hash
        self.depositor = depositor
        self.deposit_receiver = deposit_receiver
        self.root_token = root_token
        self.amount = amount

    def __repr__(self):
        return f"<PolygonLockedToken {self.blockchain} {self.transaction_hash} {self.depositor} {self.deposit_receiver} {self.root_token} {self.amount}>"


class PolygonExitedToken(Base):
    __tablename__ = "polygon_exited_token"

    id                    = Column(Integer,        nullable=False, autoincrement=True, primary_key=True)
    blockchain            = Column(String(10),     nullable=False)
    transaction_hash      = Column(String(66),     nullable=False)
    exitor                = Column(String(42),     nullable=False)
    root_token            = Column(String(42),     nullable=False)
    amount                = Column(Numeric(30, 0), nullable=False)

    def __init__(
        self, blockchain, transaction_hash, exitor, root_token, amount
    ):
        self.blockchain = blockchain
        self.transaction_hash = transaction_hash
        self.exitor = exitor
        self.root_token = root_token
        self.amount = amount

    def __repr__(self):
        return f"<PolygonExitedToken {self.blockchain} {self.transaction_hash} {self.exitor} {self.root_token} {self.amount}>"


class PolygonNewDepositBlock(Base):
    __tablename__ = "polygon_new_deposit_block"

    id                    = Column(Integer,        nullable=False, autoincrement=True, primary_key=True)
    blockchain            = Column(String(10),     nullable=False)
    transaction_hash      = Column(String(66),     nullable=False)
    owner                 = Column(String(42),     nullable=False)
    token                 = Column(String(42),     nullable=False)
    amount                = Column(Numeric(30, 0), nullable=False)
    deposit_block_id      = Column(Integer,        nullable=False)

    def __init__(
        self, blockchain, transaction_hash, owner, token, amount, deposit_block_id
    ):
        self.blockchain = blockchain
        self.transaction_hash = transaction_hash
        self.owner = owner
        self.token = token
        self.amount = amount
        self.deposit_block_id = deposit_block_id

    def __repr__(self):
        return f"<PolygonNewDepositBlock {self.blockchain} {self.transaction_hash} {self.owner} {self.token} {self.amount} {self.deposit_block_id}>"


class PolygonTokenDeposited(Base):
    __tablename__ = "polygon_token_deposited"

    id                    = Column(Integer,        nullable=False, autoincrement=True, primary_key=True)
    blockchain            = Column(String(10),     nullable=False)
    transaction_hash      = Column(String(66),     nullable=False)
    root_token            = Column(String(42),     nullable=False)
    child_token           = Column(String(42),     nullable=False)
    user                  = Column(String(42),     nullable=False)
    amount                = Column(Numeric(30, 0), nullable=False)
    deposit_count         = Column(BigInteger,     nullable=False)

    def __init__(
        self, blockchain, transaction_hash, root_token, child_token, user, amount, deposit_count
    ):
        self.blockchain = blockchain
        self.transaction_hash = transaction_hash
        self.root_token = root_token
        self.child_token = child_token
        self.user = user
        self.amount = amount
        self.deposit_count = deposit_count

    def __repr__(self):
        return f"<PolygonTokenDeposited {self.root_token} {self.blockchain} {self.transaction_hash} {self.child_token} {self.user} {self.amount} {self.deposit_count}>"


class PolygonPOLWithdraw(Base):
    __tablename__ = "polygon_pol_withdraw"

    id                    = Column(Integer,        nullable=False, autoincrement=True, primary_key=True)
    blockchain            = Column(String(10),     nullable=False)
    transaction_hash      = Column(String(66),     nullable=False)
    token                 = Column(String(42),     nullable=False)
    from_address          = Column(String(42),     nullable=False)
    amount                = Column(Numeric(30, 0), nullable=False)
    input1                = Column(String(100),    nullable=True)
    output1               = Column(String(100),    nullable=True)

    def __init__(
        self, blockchain, transaction_hash, token, from_address, amount, input1=None, output1=None
    ):
        self.blockchain = blockchain
        self.transaction_hash = transaction_hash
        self.token = token
        self.from_address = from_address
        self.amount = amount
        self.input1 = input1
        self.output1 = output1

    def __repr__(self):
        return f"<PolygonPOLWithdraw {self.blockchain} {self.transaction_hash} {self.token} {self.from_address} {self.amount} {self.input1} {self.output1}>"


class PolygonBridgeWithdraw(Base):
    __tablename__ = "polygon_bridge_withdraw"

    id                   = Column(BigInteger,     nullable=False, autoincrement=True, primary_key=True)
    blockchain           = Column(String(10),     nullable=False)
    transaction_hash     = Column(String(66),     nullable=False)
    exit_id              = Column(String(48),     nullable=False)
    user                 = Column(String(42),     nullable=False)
    token                = Column(String(42),     nullable=False)
    amount               = Column(Numeric(30, 0), nullable=False)

    def __init__(
        self, blockchain, transaction_hash, exit_id, user, token, amount
    ):
        self.blockchain = blockchain
        self.transaction_hash = transaction_hash
        self.exit_id = exit_id
        self.user = user
        self.token = token
        self.amount = amount

    def __repr__(self):
        return f"<PolygonBridgeWithdraw {self.blockchain} {self.transaction_hash} {self.exit_id} {self.user} {self.token} {self.amount}>"


class PolygonBlockchainTransaction(Base):
    __tablename__ = "polygon_blockchain_transactions"

    blockchain          = Column(String(10),     nullable=False)
    transaction_hash    = Column(String(66),     nullable=False, primary_key=True)
    block_number        = Column(Integer,        nullable=False)
    timestamp           = Column(BigInteger,     nullable=False)
    from_address        = Column(String(42),     nullable=False)
    to_address          = Column(String(42),     nullable=False)
    status              = Column(Integer,        nullable=False)
    fee                 = Column(Numeric(30, 0), nullable=False)

    def __init__(
        self, blockchain, transaction_hash, block_number, timestamp, from_address, to_address, status, fee
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
        return f"<PolygonBlockchainTransaction(blockchain={self.blockchain}, transaction_hash={self.transaction_hash}, block_number={self.block_number}, timestamp={self.timestamp} from_address={self.from_address}, to_address={self.to_address}, status={self.status})>"


# ######### Processed Data ##########


class PolygonCrossChainTransactions(Base):
    __tablename__ = "polygon_cross_chain_transactions"

    id                   = Column(BigInteger,     nullable=False, autoincrement=True, primary_key=True)
    src_blockchain       = Column(String(10),     nullable=False)
    src_transaction_hash = Column(String(66),     nullable=False)
    src_from_address     = Column(String(42),     nullable=False)
    src_to_address       = Column(String(42),     nullable=False)
    src_fee              = Column(Numeric(30, 0), nullable=False)
    src_fee_usd          = Column(Float,          nullable=True)
    src_timestamp        = Column(BigInteger,     nullable=False)
    dst_blockchain       = Column(String(10),     nullable=False)
    dst_transaction_hash = Column(String(66),     nullable=False)
    dst_from_address     = Column(String(42),     nullable=False)
    dst_to_address       = Column(String(42),     nullable=False)
    dst_fee              = Column(Numeric(30, 0), nullable=False)
    dst_fee_usd          = Column(Float,          nullable=True)
    dst_timestamp        = Column(BigInteger,     nullable=False)
    deposit_id           = Column(String(48),     nullable=False)
    depositor            = Column(String(42),     nullable=False)
    recipient            = Column(String(42),     nullable=False)
    src_contract_address = Column(String(42),     nullable=False)
    amount               = Column(Numeric(30, 0), nullable=False)
    amount_usd           = Column(Float,          nullable=True)

    def __init__(
        self, src_blockchain, src_transaction_hash, src_from_address, src_to_address, src_fee, src_fee_usd, src_timestamp, dst_blockchain, dst_transaction_hash, dst_from_address, dst_to_address, dst_fee, dst_fee_usd, dst_timestamp, deposit_id, depositor, recipient, src_contract_address, dst_contract_address, amount, amount_usd
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



class PolygonPlasmaCrossChainTransactions(Base):
    __tablename__ = "polygon_plasma_cross_chain_transactions"

    id                   = Column(BigInteger,     nullable=False, autoincrement=True, primary_key=True)
    src_blockchain       = Column(String(10),     nullable=False)
    src_transaction_hash = Column(String(66),     nullable=False)
    src_from_address     = Column(String(42),     nullable=False)
    src_to_address       = Column(String(42),     nullable=False)
    src_fee              = Column(Numeric(30, 0), nullable=False)
    src_fee_usd          = Column(Float,          nullable=True)
    src_timestamp        = Column(BigInteger,     nullable=False)
    dst_blockchain       = Column(String(10),     nullable=False)
    dst_transaction_hash = Column(String(66),     nullable=False)
    dst_from_address     = Column(String(42),     nullable=False)
    dst_to_address       = Column(String(42),     nullable=False)
    dst_fee              = Column(Numeric(30, 0), nullable=False)
    dst_fee_usd          = Column(Float,          nullable=True)
    dst_timestamp        = Column(BigInteger,     nullable=False)
    deposit_id           = Column(String(48),     nullable=False)
    depositor            = Column(String(42),     nullable=False)
    recipient            = Column(String(42),     nullable=False)
    src_contract_address = Column(String(42),     nullable=False)
    amount               = Column(Numeric(30, 0), nullable=False)
    amount_usd           = Column(Float,          nullable=True)

    def __init__(
        self, src_blockchain, src_transaction_hash, src_from_address, src_to_address, src_fee, src_fee_usd, src_timestamp, dst_blockchain, dst_transaction_hash, dst_from_address, dst_to_address, dst_fee, dst_fee_usd, dst_timestamp, deposit_id, depositor, recipient, src_contract_address, dst_contract_address, amount, amount_usd
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
