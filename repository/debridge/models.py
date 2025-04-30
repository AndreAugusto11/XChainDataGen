from sqlalchemy import (BigInteger, Column, Float, ForeignKey, Integer,
                        Numeric, String)

from repository.database import Base

class DeBridgeCreatedOrder(Base):
    __tablename__ = "debridge_created_order"

    id                             = Column(Integer,       nullable=False, autoincrement=True, primary_key=True)
    blockchain                     = Column(String(10),    nullable=False)
    transaction_hash               = Column(String(66),    nullable=False)
    maker_order_nonce              = Column(BigInteger,    nullable=False)
    maker_src                      = Column(String(42),    nullable=False)
    src_blockchain                 = Column(String(10),    nullable=False)
    give_token_address             = Column(String(42),    nullable=False)
    give_amount                    = Column(Numeric(30,0), nullable=False)
    dst_blockchain                 = Column(String(10),    nullable=False)
    take_token_address             = Column(String(42),    nullable=False)
    take_amount                    = Column(Numeric(30,0), nullable=False)
    receiver_dst                   = Column(String(42),    nullable=False)
    give_patch_authority_src       = Column(String(42),    nullable=False)
    order_authority_address_dst    = Column(String(42),    nullable=False)
    allowed_taker_dst              = Column(String(42),    nullable=True)
    allowed_cancel_beneficiary_src = Column(String(42),    nullable=True)
    external_call                  = Column(String,        nullable=True)
    order_id                       = Column(String(66),    nullable=False)
    affiliate_fee                  = Column(String,        nullable=True)
    native_fix_fee                 = Column(Numeric(30,0), nullable=False)
    percent_fee                    = Column(Numeric(30,0), nullable=False)
    referral_code                  = Column(Integer,       nullable=False)
    _metadata                       = Column(String,        nullable=True) # we added the underscore to avoid conflicts with the metadata column in the base class

    def __init__(
        self, blockchain, transaction_hash, maker_order_nonce, maker_src, src_blockchain, give_token_address, give_amount, dst_blockchain,
        take_token_address, take_amount, receiver_dst, give_patch_authority_src, order_authority_address_dst,
        allowed_taker_dst, allowed_cancel_beneficiary_src, external_call, order_id, affiliate_fee, native_fix_fee,
        percent_fee, referral_code, _metadata
    ):
        self.blockchain = blockchain
        self.transaction_hash = transaction_hash
        self.maker_order_nonce = maker_order_nonce
        self.maker_src = maker_src
        self.src_blockchain = src_blockchain
        self.give_token_address = give_token_address
        self.give_amount = give_amount
        self.dst_blockchain = dst_blockchain
        self.take_token_address = take_token_address
        self.take_amount = take_amount
        self.receiver_dst = receiver_dst
        self.give_patch_authority_src = give_patch_authority_src
        self.order_authority_address_dst = order_authority_address_dst
        self.allowed_taker_dst = allowed_taker_dst
        self.allowed_cancel_beneficiary_src = allowed_cancel_beneficiary_src
        self.external_call = external_call
        self.order_id = order_id
        self.affiliate_fee = affiliate_fee
        self.native_fix_fee = native_fix_fee
        self.percent_fee = percent_fee
        self.referral_code = referral_code
        self._metadata = _metadata

    def __repr__(self):
        return f"<DeBridgeOrder(blockchain={self.blockchain}, transaction_hash={self.transaction_hash}, maker_order_nonce={self.maker_order_nonce}, maker_src={self.maker_src}, src_blockchain={self.src_blockchain}, give_token_address={self.give_token_address}, give_amount={self.give_amount}, dst_blockchain={self.dst_blockchain}, take_token_address={self.take_token_address}, take_amount={self.take_amount}, receiver_dst={self.receiver_dst}, give_patch_authority_src={self.give_patch_authority_src}, order_authority_address_dst={self.order_authority_address_dst}, allowed_taker_dst={self.allowed_taker_dst}, allowed_cancel_beneficiary_src={self.allowed_cancel_beneficiary_src}, external_call={self.external_call}, order_id={self.order_id}, affiliate_fee={self.affiliate_fee}, native_fix_fee={self.native_fix_fee}, percent_fee={self.percent_fee}, referral_code={self.referral_code}, _metadata={self._metadata})>"


class DeBridgeFulfilledOrder(Base):
    __tablename__ = "debridge_fulfilled_order"

    id                             = Column(Integer,       nullable=False, autoincrement=True, primary_key=True)
    blockchain                     = Column(String(10),    nullable=False)
    transaction_hash               = Column(String(66),    nullable=False)
    maker_order_nonce              = Column(BigInteger,    nullable=False)
    maker_src                      = Column(String(42),    nullable=False)
    src_blockchain                 = Column(String(10),    nullable=False)
    give_token_address             = Column(String(42),    nullable=False)
    give_amount                    = Column(Numeric(30,0), nullable=False)
    dst_blockchain                 = Column(String(10),    nullable=False)
    take_token_address             = Column(String(42),    nullable=False)
    take_amount                    = Column(Numeric(30,0), nullable=False)
    receiver_dst                   = Column(String(42),    nullable=False)
    give_patch_authority_src       = Column(String(42),    nullable=False)
    order_authority_address_dst    = Column(String(42),    nullable=False)
    allowed_taker_dst              = Column(String(42),    nullable=True)
    allowed_cancel_beneficiary_src = Column(String(42),    nullable=True)
    external_call                  = Column(String,        nullable=True)
    order_id                       = Column(String(66),    nullable=False)
    sender                         = Column(String(42),    nullable=False)
    unlock_authority               = Column(String(42),    nullable=False)
    
    def __init__(
        self, blockchain, transaction_hash, maker_order_nonce, maker_src, src_blockchain, give_token_address, give_amount, dst_blockchain,
        take_token_address, take_amount, receiver_dst, give_patch_authority_src, order_authority_address_dst,
        allowed_taker_dst, allowed_cancel_beneficiary_src, external_call, order_id, sender, unlock_authority
    ):
        self.blockchain = blockchain
        self.transaction_hash = transaction_hash
        self.maker_order_nonce = maker_order_nonce
        self.maker_src = maker_src
        self.src_blockchain = src_blockchain
        self.give_token_address = give_token_address
        self.give_amount = give_amount
        self.dst_blockchain = dst_blockchain
        self.take_token_address = take_token_address
        self.take_amount = take_amount
        self.receiver_dst = receiver_dst
        self.give_patch_authority_src = give_patch_authority_src
        self.order_authority_address_dst = order_authority_address_dst
        self.allowed_taker_dst = allowed_taker_dst
        self.allowed_cancel_beneficiary_src = allowed_cancel_beneficiary_src
        self.external_call = external_call
        self.order_id = order_id
        self.sender = sender
        self.unlock_authority = unlock_authority

    def __repr__(self):
        return f"<DeBridgeOrder(blockchain={self.blockchain}, maker_order_nonce={self.maker_order_nonce}, maker_src={self.maker_src}, src_blockchain={self.src_blockchain}, give_token_address={self.give_token_address}, give_amount={self.give_amount}, dst_blockchain={self.dst_blockchain}, take_token_address={self.take_token_address}, take_amount={self.take_amount}, receiver_dst={self.receiver_dst}, give_patch_authority_src={self.give_patch_authority_src}, order_authority_address_dst={self.order_authority_address_dst}, allowed_taker_dst={self.allowed_taker_dst}, allowed_cancel_beneficiary_src={self.allowed_cancel_beneficiary_src}, external_call={self.external_call}, order_id={self.order_id}, sender={self.sender}, unlock_authority={self.unlock_authority})>"


class DeBridgeClaimedUnlock(Base):
    __tablename__ = "debridge_claimed_unlock"

    id                             = Column(Integer,       nullable=False, autoincrement=True, primary_key=True)
    blockchain                     = Column(String(10),    nullable=False)
    transaction_hash               = Column(String(66),    nullable=False)
    order_id                       = Column(String(66),    nullable=False)
    beneficiary                    = Column(String(42),    nullable=False)
    give_amount                    = Column(Numeric(30,0), nullable=False)
    give_token_address             = Column(String(42),    nullable=False)

    def __init__(self, blockchain, transaction_hash, order_id, beneficiary, give_amount, give_token_address):
        self.blockchain = blockchain
        self.transaction_hash = transaction_hash
        self.order_id = order_id
        self.beneficiary = beneficiary
        self.give_amount = give_amount
        self.give_token_address = give_token_address

    def __repr__(self):
        return f"<DeBridgeClaimedUnlock(blockchain={self.blockchain}, order_id={self.order_id}, beneficiary={self.beneficiary}, give_amount={self.give_amount}, give_token_address={self.give_token_address})>"


class DeBridgeSentOrderUnlock(Base):
    __tablename__ = "debridge_sent_order_unlock"

    id                             = Column(Integer,       nullable=False, autoincrement=True, primary_key=True)
    blockchain                     = Column(String(10),    nullable=False)
    transaction_hash               = Column(String(66),    nullable=False)
    order_id                       = Column(String(66),    nullable=False)
    beneficiary                    = Column(String(42),    nullable=False)
    submission_id                  = Column(String(66),    nullable=False)

    def __init__(self, blockchain, transaction_hash, order_id, beneficiary, submission_id):
        self.blockchain = blockchain
        self.transaction_hash = transaction_hash
        self.order_id = order_id
        self.beneficiary = beneficiary
        self.submission_id = submission_id

    def __repr__(self):
        return f"<DeBridgeSentOrderUnlock(blockchain={self.blockchain}, order_id={self.order_id}, beneficiary={self.beneficiary}, submission_id={self.submission_id})>"


class DeBridgeBlockchainTransaction(Base):
    __tablename__ = "debridge_blockchain_transaction"

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

class DeBridgeCrossChainTransactions(Base):
    __tablename__ = "debridge_cross_chain_transactions"

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
    input_amount         = Column(Numeric(30, 0), nullable=False)
    input_amount_usd     = Column(Float,          nullable=True)
    output_amount        = Column(Numeric(30, 0), nullable=False)
    output_amount_usd    = Column(Float,          nullable=True)
    native_fix_fee       = Column(Numeric(30, 0), nullable=False)
    native_fix_fee_usd   = Column(Float,          nullable=True)
    percent_fee          = Column(Numeric(30, 0), nullable=False)
    percent_fee_usd      = Column(Float,          nullable=True)

    def __init__(
        self, src_blockchain, src_transaction_hash, src_from_address, src_to_address, src_fee, src_fee_usd, src_timestamp,
        dst_blockchain, dst_transaction_hash, dst_from_address, dst_to_address, dst_fee, dst_fee_usd, dst_timestamp,
        depositor, recipient, src_contract_address, dst_contract_address, input_amount, input_amount_usd,
        output_amount, output_amount_usd, native_fix_fee, native_fix_fee_usd, percent_fee, percent_fee_usd
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
        self.input_amount = input_amount
        self.input_amount_usd = input_amount_usd
        self.output_amount = output_amount
        self.output_amount_usd = output_amount_usd
        self.native_fix_fee = native_fix_fee
        self.native_fix_fee_usd = native_fix_fee_usd
        self.percent_fee = percent_fee
        self.percent_fee_usd = percent_fee_usd
    
    def __repr__(self):
        return f"<DeBridgeCrossChainTransactions(src_blockchain={self.src_blockchain}, src_transaction_hash={self.src_transaction_hash}, src_from_address={self.src_from_address}, src_to_address={self.src_to_address}, src_fee={self.src_fee}, src_fee_usd={self.src_fee_usd}, src_timestamp={self.src_timestamp}, dst_blockchain={self.dst_blockchain}, dst_transaction_hash={self.dst_transaction_hash}, dst_from_address={self.dst_from_address}, dst_to_address={self.dst_to_address}, dst_fee={self.dst_fee}, dst_fee_usd={self.dst_fee_usd}, dst_timestamp={self.dst_timestamp}, depositor={self.depositor}, recipient={self.recipient}, src_contract_address={self.src_contract_address}, dst_contract_address={self.dst_contract_address}, input_amount={self.input_amount}, input_amount_usd={self.input_amount_usd}, output_amount={self.output_amount}, output_amount_usd={self.output_amount_usd}, native_fix_fee={self.native_fix_fee}, native_fix_fee_usd={self.native_fix_fee_usd}, percent_fee={self.percent_fee}, percent_fee_usd={self.percent_fee_usd})>"

