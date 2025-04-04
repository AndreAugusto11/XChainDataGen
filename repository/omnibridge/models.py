from sqlalchemy import (BigInteger, Column, Float, ForeignKey, Integer,
                        Numeric, String)

from repository.database import Base


class OmnibridgeTokensBridgingInitiated(Base):
    __tablename__ = "omnibridge_tokens_bridging_initiated"

    id                    = Column(Integer,       nullable=False, autoincrement=True, primary_key=True)
    blockchain            = Column(String(10),    nullable=False)
    transaction_hash      = Column(String(66),    nullable=False)
    token                 = Column(String(42),    nullable=False)
    sender                = Column(String(42),    nullable=False)
    value                 = Column(Numeric(30,0), nullable=False)
    message_id            = Column(String(66),    nullable=False)

    def __init__(self, blockchain, transaction_hash, token, sender, value, message_id):
        self.blockchain = blockchain
        self.transaction_hash = transaction_hash
        self.token = token
        self.sender = sender
        self.value = value
        self.message_id = message_id
    
    def __repr__(self):
        return f"<OmnibridgeTokensBridgingInitiated(blockchain={self.blockchain}, transaction_hash={self.transaction_hash}, token={self.token}, sender={self.sender}, value={self.value}, message_id={self.message_id})>"


# TokensBridged (index_topic_1 address token, index_topic_2 address recipient, uint256 value, index_topic_3 bytes32 messageId)
class OmnibridgeTokensBridged(Base):
    __tablename__ = "omnibridge_tokens_bridged"

    id                    = Column(Integer,       nullable=False, autoincrement=True, primary_key=True)
    blockchain            = Column(String(10),    nullable=False)
    transaction_hash      = Column(String(66),    nullable=False)
    token                 = Column(String(42),    nullable=False)
    recipient             = Column(String(42),    nullable=False)
    value                 = Column(Numeric(30,0), nullable=False)
    message_id            = Column(String(66),    nullable=False)

    def __init__(self, blockchain, transaction_hash, token, recipient, value, message_id):
        self.blockchain = blockchain
        self.transaction_hash = transaction_hash
        self.token = token
        self.recipient = recipient
        self.value = value
        self.message_id = message_id
    
    def __repr__(self):
        return f"<OmnibridgeTokensBridged(blockchain={self.blockchain}, transaction_hash={self.transaction_hash}, token={self.token}, recipient={self.recipient}, value={self.value}, message_id={self.message_id})>"


class OmnibridgeRelayedMessage(Base):
    __tablename__ = "omnibridge_relayed_message"

    id                    = Column(Integer,       nullable=False, autoincrement=True, primary_key=True)
    blockchain            = Column(String(10),    nullable=False)
    transaction_hash      = Column(String(66),    nullable=False)
    recipient             = Column(String(42),    nullable=False)
    value                 = Column(Numeric(30,0), nullable=False)
    src_transaction_hash  = Column(String(66),    nullable=False)

    def __init__(self, blockchain, transaction_hash, recipient, value, src_transaction_hash):
        self.blockchain = blockchain
        self.transaction_hash = transaction_hash
        self.recipient = recipient
        self.value = value
        self.src_transaction_hash = src_transaction_hash
    
    def __repr__(self):
        return f"<OmnibridgeRelayedMessage(blockchain={self.blockchain}, transaction_hash={self.transaction_hash}, recipient={self.recipient}, value={self.value}, src_transaction_hash={self.src_transaction_hash})>"


# SignedForUserRequest (index_topic_1 address signer, bytes32 messageHash)
class OmnibridgeSignedForUserRequest(Base):
    __tablename__ = "omnibridge_signed_for_user_request"

    id                    = Column(Integer,    nullable=False, autoincrement=True, primary_key=True)
    blockchain            = Column(String(10), nullable=False)
    transaction_hash      = Column(String(66), nullable=False)
    signer                = Column(String(42), nullable=False)
    message_hash          = Column(String(66), nullable=False)

    def __init__(self, blockchain, transaction_hash, signer, message_hash):
        self.blockchain = blockchain
        self.transaction_hash = transaction_hash
        self.signer = signer
        self.message_hash = message_hash
    
    def __repr__(self):
        return f"<OmnibridgeSignedForUserRequest(blockchain={self.blockchain}, transaction_hash={self.transaction_hash}, signer={self.signer}, message_hash={self.message_hash})>"


# SignedForAffirmation (index_topic_1 address signer, bytes32 messageHash)
# SignedForAffirmation (index_topic_1 address signer, bytes32 transactionHash)
class OmnibridgeSignedForAffirmation(Base):
    __tablename__ = "omnibridge_signed_for_affirmation"

    id                    = Column(Integer,    nullable=False, autoincrement=True, primary_key=True)
    blockchain            = Column(String(10), nullable=False)
    transaction_hash      = Column(String(66), nullable=False)
    signer                = Column(String(42), nullable=False)
    message_hash          = Column(String(66), nullable=True)
    src_transaction_hash  = Column(String(66), nullable=True)

    def __init__(self, blockchain, transaction_hash, signer, message_hash, src_transaction_hash):
        self.blockchain = blockchain
        self.transaction_hash = transaction_hash
        self.signer = signer
        self.message_hash = message_hash
        self.src_transaction_hash = src_transaction_hash

    def __repr__(self):
        return f"<OmnibridgeSignedForAffirmation(blockchain={self.blockchain}, transaction_hash={self.transaction_hash}, signer={self.signer}, message_hash={self.message_hash}, src_transaction_hash={self.src_transaction_hash})>"


#UserRequestForSignature (address recipient, uint256 value)
#UserRequestForSignature (index_topic_1 bytes32 messageId, bytes encodedData)
class OmnibridgeUserRequestForSignature(Base):
    __tablename__ = "omnibridge_user_request_for_signature"

    id                    = Column(Integer,       nullable=False, autoincrement=True, primary_key=True)
    blockchain            = Column(String(10),    nullable=False)
    transaction_hash      = Column(String(66),    nullable=False)
    message_id            = Column(String(66),    nullable=True)
    encoded_data          = Column(String(66),    nullable=True)
    encoded_data_hash     = Column(String(66),    nullable=True)
    recipient             = Column(String(42),    nullable=True)
    value                 = Column(Numeric(30,0), nullable=True)

    def __init__(self, blockchain, transaction_hash, message_id, encoded_data, encoded_data_hash, recipient, value):
        self.blockchain = blockchain
        self.transaction_hash = transaction_hash
        self.message_id = message_id
        self.encoded_data = encoded_data
        self.encoded_data_hash = encoded_data_hash
        self.recipient = recipient
        self.value = value

    def __repr__(self):
        return f"<OmnibridgeUserRequestForSignature(blockchain={self.blockchain}, transaction_hash={self.transaction_hash}, message_id={self.message_id}, encoded_data={self.encoded_data}, recipient={self.recipient}, value={self.value})>"


#AffirmationCompleted (address recipient, uint256 value, bytes32 transactionHash)
class OmnibridgeAffirmationCompleted(Base):
    __tablename__ = "omnibridge_affirmation_completed"

    id                    = Column(Integer,       nullable=False, autoincrement=True, primary_key=True)
    blockchain            = Column(String(10),    nullable=False)
    transaction_hash      = Column(String(66),    nullable=False)
    recipient             = Column(String(42),    nullable=False)
    value                 = Column(Numeric(30,0), nullable=False)
    src_transaction_hash  = Column(String(66),    nullable=False)

    def __init__(self, blockchain, transaction_hash, recipient, value, src_transaction_hash):
        self.blockchain = blockchain
        self.transaction_hash = transaction_hash
        self.recipient = recipient
        self.value = value
        self.src_transaction_hash = src_transaction_hash
    
    def __repr__(self):
        return f"<OmnibridgeAffirmationCompleted(blockchain={self.blockchain}, transaction_hash={self.transaction_hash}, recipient={self.recipient}, value={self.value}, src_transaction_hash={self.src_transaction_hash})>"


# UserRequestForAffirmation (index_topic_1 bytes32 messageId, bytes encodedData)
# UserRequestForAffirmation (address recipient, uint256 value)
class OmnibridgeUserRequestForAffirmation(Base):
    __tablename__ = "omnibridge_user_request_for_affirmation"

    id                    = Column(Integer,       nullable=False, autoincrement=True, primary_key=True)
    blockchain            = Column(String(10),    nullable=False)
    transaction_hash      = Column(String(66),    nullable=False)
    message_id            = Column(String(66),    nullable=True)
    encoded_data          = Column(String(66),    nullable=True)
    recipient             = Column(String(42),    nullable=True)
    value                 = Column(Numeric(30,0), nullable=True)

    def __init__(self, blockchain, transaction_hash, message_id, encoded_data, recipient, value):
        self.blockchain = blockchain
        self.transaction_hash = transaction_hash
        self.message_id = message_id
        self.encoded_data = encoded_data
        self.recipient = recipient
        self.value = value

    def __repr__(self):
        return f"<OmnibridgeUserRequestForAffirmation(blockchain={self.blockchain}, transaction_hash={self.transaction_hash}, message_id={self.message_id}, encoded_data={self.encoded_data}, recipient={self.recipient}, value={self.value})>"


class OmnibridgeBlockchainTransaction(Base):
    __tablename__ = "omnibridge_blockchain_transaction"

    blockchain            = Column(String(10),    nullable=False)
    transaction_hash      = Column(String(66),    nullable=False, primary_key=True)
    block_number          = Column(BigInteger,    nullable=False)
    timestamp             = Column(BigInteger,    nullable=False)
    from_address          = Column(String(42),    nullable=False)
    to_address            = Column(String(42),    nullable=False)
    status                = Column(Integer,       nullable=False)
    fee                   = Column(Numeric(30,0), nullable=False)

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
        return f"<OmnibridgeBlockchainTransaction(blockchain={self.blockchain}, transaction_hash={self.transaction_hash}, block_number={self.block_number}, timestamp={self.timestamp} from_address={self.from_address}, to_address={self.to_address}, status={self.status})>"


########## Processed Data ##########

class OmnibridgeCrossChainTransactions(Base):
    __tablename__ = "omnibridge_cross_chain_transactions"

    id                   = Column(Integer,       nullable=False, autoincrement=True, primary_key=True)
    src_blockchain       = Column(String(10),    nullable=False)
    src_transaction_hash = Column(String(66),    nullable=False)
    src_from_address     = Column(String(42),    nullable=False)
    src_to_address       = Column(String(42),    nullable=False)
    src_fee              = Column(Numeric(30,0), nullable=False)
    src_fee_usd          = Column(Float,         nullable=True)
    src_timestamp        = Column(BigInteger,    nullable=False)
    dst_blockchain       = Column(String(10),    nullable=False)
    dst_transaction_hash = Column(String(66),    nullable=False)
    dst_from_address     = Column(String(42),    nullable=False)
    dst_to_address       = Column(String(42),    nullable=False)
    dst_fee              = Column(Numeric(30,0), nullable=False)
    dst_fee_usd          = Column(Float,         nullable=True)
    dst_timestamp        = Column(BigInteger,    nullable=False)
    message_id           = Column(String(66),    nullable=True)
    depositor            = Column(String(42),    nullable=False)
    recipient            = Column(String(42),    nullable=False)
    src_contract_address = Column(String(42),    nullable=False)
    dst_contract_address = Column(String(42),    nullable=False)
    amount               = Column(Numeric(30,0), nullable=False)
    amount_usd           = Column(Float,         nullable=True)

    def __init__(
        self, src_blockchain, src_transaction_hash, src_from_address, src_to_address, src_fee, src_fee_usd, src_timestamp,
        dst_blockchain, dst_transaction_hash, dst_from_address, dst_to_address, dst_fee, dst_fee_usd, dst_timestamp,
        depositor, recipient, src_contract_address, dst_contract_address, amount, amount_usd
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
        self.depositor = depositor
        self.recipient = recipient
        self.src_contract_address = src_contract_address
        self.dst_contract_address = dst_contract_address
        self.amount = amount
        self.amount_usd = amount_usd
    
    def __repr__(self):
        return f"<OmnibridgeCrossChainTransactions(src_blockchain={self.src_blockchain}, src_transaction_hash={self.src_transaction_hash}, src_from_address={self.src_from_address}, src_to_address={self.src_to_address}, src_fee={self.src_fee}, src_fee_usd={self.src_fee_usd}, src_timestamp={self.src_timestamp}, dst_blockchain={self.dst_blockchain}, dst_transaction_hash={self.dst_transaction_hash}, dst_from_address={self.dst_from_address}, dst_to_address={self.dst_to_address}, dst_fee={self.dst_fee}, dst_fee_usd={self.dst_fee_usd}, dst_timestamp={self.dst_timestamp}, message_id={self.message_id}, depositor={self.depositor}, recipient={self.recipient}, src_contract_address={self.src_contract_address}, dst_contract_address={self.dst_contract_address}, amount={self.amount}, amount_usd={self.amount_usd})>"


class OmnibridgeOperatorTransactions(Base):
    __tablename__ = "omnibridge_operator_transactions"

    id                   = Column(Integer,       nullable=False, autoincrement=True, primary_key=True)
    blockchain           = Column(String(10),    nullable=False)
    transaction_hash     = Column(String(66),    nullable=False)
    from_address         = Column(String(42),    nullable=False)
    to_address           = Column(String(42),    nullable=False)
    signer               = Column(String(42),    nullable=False)
    fee                  = Column(Numeric(30,0), nullable=False)
    fee_usd              = Column(Float,         nullable=True)
    timestamp            = Column(BigInteger,    nullable=False)
    status               = Column(Integer,       nullable=False)

    def __init__(
        self, blockchain, transaction_hash, from_address, to_address, signer, fee, fee_usd, timestamp, status
    ):
        self.blockchain = blockchain
        self.transaction_hash = transaction_hash
        self.from_address = from_address
        self.to_address = to_address
        self.signer = signer
        self.fee = fee
        self.fee_usd = fee_usd
        self.timestamp = timestamp
        self.status = status

    def __repr__(self):
        return f"<OmnibridgeOperatorTransactions(blockchain={self.blockchain}, transaction_hash={self.transaction_hash}, from_address={self.from_address}, to_address={self.to_address}, signer={self.signer}, fee={self.fee}, fee_usd={self.fee_usd}, timestamp={self.timestamp}, status={self.status})>"
