from sqlalchemy import BigInteger, Column, Float, Integer, Numeric, String

from repository.common.models import BlockchainTransaction
from repository.database import Base


class DeBridgeCreatedOrder(Base):
    __tablename__ = "debridge_created_order"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    blockchain = Column(String(10), nullable=False)
    transaction_hash = Column(String(88), nullable=False)
    maker_order_nonce = Column(Numeric(30, 0), nullable=False)
    maker_src = Column(String(44), nullable=False)
    src_blockchain = Column(String(10), nullable=False)
    give_token_address = Column(String(44), nullable=False)
    give_amount = Column(Numeric(30, 0), nullable=False)
    dst_blockchain = Column(String(10), nullable=False)
    take_token_address = Column(String(44), nullable=False)
    take_amount = Column(Numeric(30, 0), nullable=False)
    receiver_dst = Column(String(44), nullable=False)
    give_patch_authority_src = Column(String(44), nullable=False)
    order_authority_address_dst = Column(String(44), nullable=False)
    allowed_taker_dst = Column(String(44), nullable=True)
    allowed_cancel_beneficiary_src = Column(String(44), nullable=True)
    external_call = Column(String, nullable=True)
    order_id = Column(String(66), nullable=True)
    affiliate_fee = Column(String, nullable=True)
    native_fix_fee = Column(Numeric(30, 0), nullable=True)
    percent_fee = Column(Numeric(30, 0), nullable=True)
    referral_code = Column(Integer, nullable=False)
    _metadata = Column(
        String, nullable=True
    )  # we added the underscore to avoid conflicts with the metadata column in the base class
    original_token = Column(String(44), nullable=True)
    original_amount = Column(Numeric(30, 0), nullable=True)

    def __init__(
        self,
        blockchain,
        transaction_hash,
        maker_order_nonce,
        maker_src,
        src_blockchain,
        give_token_address,
        give_amount,
        dst_blockchain,
        take_token_address,
        take_amount,
        receiver_dst,
        give_patch_authority_src,
        order_authority_address_dst,
        allowed_taker_dst,
        allowed_cancel_beneficiary_src,
        external_call,
        order_id,
        affiliate_fee,
        native_fix_fee,
        percent_fee,
        referral_code,
        _metadata,
        original_token=None,
        original_amount=None,
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
        self.original_token = original_token
        self.original_amount = original_amount

    def __repr__(self):
        return (
            f"<DeBridgeOrder(blockchain={self.blockchain}, "
            f"transaction_hash={self.transaction_hash}, "
            f"maker_order_nonce={self.maker_order_nonce}, "
            f"maker_src={self.maker_src}, "
            f"src_blockchain={self.src_blockchain}, "
            f"give_token_address={self.give_token_address}, "
            f"give_amount={self.give_amount}, "
            f"dst_blockchain={self.dst_blockchain}, "
            f"take_token_address={self.take_token_address}, "
            f"take_amount={self.take_amount}, "
            f"receiver_dst={self.receiver_dst}, "
            f"give_patch_authority_src={self.give_patch_authority_src}, "
            f"order_authority_address_dst={self.order_authority_address_dst}, "
            f"allowed_taker_dst={self.allowed_taker_dst}, "
            f"allowed_cancel_beneficiary_src={self.allowed_cancel_beneficiary_src}, "
            f"external_call={self.external_call}, "
            f"order_id={self.order_id}, "
            f"affiliate_fee={self.affiliate_fee}, "
            f"native_fix_fee={self.native_fix_fee}, "
            f"percent_fee={self.percent_fee}, "
            f"referral_code={self.referral_code}, "
            f"_metadata={self._metadata}, "
            f"original_token={self.original_token}, "
            f"original_amount={self.original_amount})>"
        )


class DeBridgeFulfilledOrder(Base):
    __tablename__ = "debridge_fulfilled_order"

    blockchain = Column(String(10), nullable=False)
    transaction_hash = Column(String(88), nullable=False)
    maker_order_nonce = Column(Numeric(30, 0), nullable=False)
    maker_src = Column(String(44), nullable=False)
    src_blockchain = Column(String(10), nullable=False)
    give_token_address = Column(String(44), nullable=False)
    give_amount = Column(Numeric(30, 0), nullable=False)
    dst_blockchain = Column(String(10), nullable=False)
    take_token_address = Column(String(44), nullable=False)
    take_amount = Column(Numeric(30, 0), nullable=False)
    receiver_dst = Column(String(44), nullable=False)
    give_patch_authority_src = Column(String(44), nullable=False)
    order_authority_address_dst = Column(String(44), nullable=False)
    allowed_taker_dst = Column(String(44), nullable=True)
    allowed_cancel_beneficiary_src = Column(String(44), nullable=True)
    external_call = Column(String, nullable=True)
    order_id = Column(String(66), nullable=False, primary_key=True)
    sender = Column(String(44), nullable=True)
    unlock_authority = Column(String(44), nullable=False)
    taker = Column(String(44), nullable=True)
    middle_dst_token = Column(String(44), nullable=True)
    middle_dst_amount = Column(Numeric(30, 0), nullable=True)

    def __init__(
        self,
        blockchain,
        transaction_hash,
        maker_order_nonce,
        maker_src,
        src_blockchain,
        give_token_address,
        give_amount,
        dst_blockchain,
        take_token_address,
        take_amount,
        receiver_dst,
        give_patch_authority_src,
        order_authority_address_dst,
        allowed_taker_dst,
        allowed_cancel_beneficiary_src,
        external_call,
        order_id,
        sender,
        unlock_authority,
        taker,
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
        self.taker = taker

    def __repr__(self):
        return (
            f"<DeBridgeOrder(blockchain={self.blockchain}, "
            f"maker_order_nonce={self.maker_order_nonce}, "
            f"maker_src={self.maker_src}, "
            f"src_blockchain={self.src_blockchain}, "
            f"give_token_address={self.give_token_address}, "
            f"give_amount={self.give_amount}, "
            f"dst_blockchain={self.dst_blockchain}, "
            f"take_token_address={self.take_token_address}, "
            f"take_amount={self.take_amount}, "
            f"receiver_dst={self.receiver_dst}, "
            f"give_patch_authority_src={self.give_patch_authority_src}, "
            f"order_authority_address_dst={self.order_authority_address_dst}, "
            f"allowed_taker_dst={self.allowed_taker_dst}, "
            f"allowed_cancel_beneficiary_src={self.allowed_cancel_beneficiary_src}, "
            f"external_call={self.external_call}, "
            f"order_id={self.order_id}, "
            f"sender={self.sender}, "
            f"unlock_authority={self.unlock_authority}, "
            f"taker={self.taker}, "
            f"middle_dst_token={self.middle_dst_token}, "
            f"middle_dst_amount={self.middle_dst_amount})>"
        )


class DeBridgeClaimedUnlock(Base):
    __tablename__ = "debridge_claimed_unlock"

    blockchain = Column(String(10), nullable=False)
    transaction_hash = Column(String(88), nullable=False)
    order_id = Column(String(66), nullable=False, primary_key=True)
    beneficiary = Column(String(44), nullable=False)
    give_amount = Column(Numeric(30, 0), nullable=False)
    give_token_address = Column(String(44), nullable=False)
    fee = Column(Numeric(30, 0), nullable=True)

    def __init__(
        self,
        blockchain,
        transaction_hash,
        order_id,
        beneficiary,
        give_amount,
        give_token_address,
        fee,
    ):
        self.blockchain = blockchain
        self.transaction_hash = transaction_hash
        self.order_id = order_id
        self.beneficiary = beneficiary
        self.give_amount = give_amount
        self.give_token_address = give_token_address
        self.fee = fee

    def __repr__(self):
        return (
            f"<DeBridgeClaimedUnlock(blockchain={self.blockchain}, "
            f"order_id={self.order_id}, "
            f"beneficiary={self.beneficiary}, "
            f"give_amount={self.give_amount}, "
            f"give_token_address={self.give_token_address}, "
            f"fee={self.fee}>"
        )


class DeBridgeBlockchainTransaction(BlockchainTransaction):
    __tablename__ = "debridge_blockchain_transaction"

    def __repr__(self):
        return (
            f"<OmnibridgeBlockchainTransaction(blockchain={self.blockchain}, "
            f"transaction_hash={self.transaction_hash}, "
            f"block_number={self.block_number}, "
            f"timestamp={self.timestamp} from_address={self.from_address}, "
            f"to_address={self.to_address}, "
            f"status={self.status})>"
        )


########## Processed Data ##########


class DeBridgeCrossChainTransactions(Base):
    __tablename__ = "debridge_cross_chain_transactions"

    src_blockchain = Column(String(10), nullable=False)
    src_transaction_hash = Column(String(88), nullable=False)
    src_from_address = Column(String(44), nullable=False)
    src_to_address = Column(String(44), nullable=False)
    src_fee = Column(Numeric(30, 0), nullable=False)
    src_value = Column(Numeric(30, 0), nullable=True)
    src_fee_usd = Column(Float, nullable=True)
    src_timestamp = Column(BigInteger, nullable=False)
    dst_blockchain = Column(String(10), nullable=False)
    dst_transaction_hash = Column(String(88), nullable=False)
    dst_from_address = Column(String(44), nullable=False)
    dst_to_address = Column(String(44), nullable=False)
    dst_fee = Column(Numeric(30, 0), nullable=False)
    dst_value = Column(Numeric(30, 0), nullable=True)
    dst_fee_usd = Column(Float, nullable=True)
    dst_timestamp = Column(BigInteger, nullable=False)
    refund_blockchain = Column(String(10), nullable=True)
    refund_transaction_hash = Column(String(88), nullable=True)
    refund_from_address = Column(String(44), nullable=True)
    refund_to_address = Column(String(44), nullable=True)
    refund_fee = Column(Numeric(30, 0), nullable=True)
    refund_value = Column(Numeric(30, 0), nullable=True)
    refund_fee_usd = Column(Float, nullable=True)
    refund_timestamp = Column(BigInteger, nullable=True)
    intent_id = Column(String(64), nullable=False, primary_key=True)
    depositor = Column(String(44), nullable=False)
    recipient = Column(String(44), nullable=False)
    src_contract_address = Column(String(44), nullable=True)
    dst_contract_address = Column(String(44), nullable=True)
    input_amount = Column(Numeric(30, 0), nullable=True)
    input_amount_usd = Column(Float, nullable=True)
    middle_src_token = Column(String(44), nullable=True)
    middle_src_amount = Column(Numeric(30, 0), nullable=True)
    middle_src_amount_usd = Column(Float, nullable=True)
    middle_dst_token = Column(String(44), nullable=True)
    middle_dst_amount = Column(Numeric(30, 0), nullable=True)
    middle_dst_amount_usd = Column(Float, nullable=True)
    output_amount = Column(Numeric(30, 0), nullable=False)
    output_amount_usd = Column(Float, nullable=True)
    refund_amount = Column(Numeric(30, 0), nullable=True)
    refund_amount_usd = Column(Float, nullable=True)
    refund_token = Column(String(44), nullable=True)
    native_fix_fee = Column(Numeric(30, 0), nullable=False)
    native_fix_fee_usd = Column(Float, nullable=True)
    percent_fee = Column(Numeric(30, 0), nullable=False)
    percent_fee_usd = Column(Float, nullable=True)

    # in debridge, percent_fee is usually 0.04% and goes to the protocol (paid on the src chain)
    # native_fee depends on the blockchain and goes to the protocol
    # native_fee + percent_fee + give_amount = total cost of the transaction for the user

    def __init__(
        self,
        src_blockchain,
        src_transaction_hash,
        src_from_address,
        src_to_address,
        src_fee,
        src_value,
        src_fee_usd,
        src_timestamp,
        dst_blockchain,
        dst_transaction_hash,
        dst_from_address,
        dst_to_address,
        dst_fee,
        dst_value,
        dst_fee_usd,
        dst_timestamp,
        refund_blockchain,
        refund_transaction_hash,
        refund_from_address,
        refund_to_address,
        refund_fee,
        refund_value,
        refund_fee_usd,
        refund_timestamp,
        intent_id,
        depositor,
        recipient,
        src_contract_address,
        dst_contract_address,
        input_amount,
        input_amount_usd,
        middle_src_token,
        middle_src_amount,
        middle_src_amount_usd,
        middle_dst_token,
        middle_dst_amount,
        middle_dst_amount_usd,
        output_amount,
        output_amount_usd,
        refund_amount,
        refund_amount_usd,
        refund_token,
        native_fix_fee,
        native_fix_fee_usd,
        percent_fee,
        percent_fee_usd,
    ):
        self.src_blockchain = src_blockchain
        self.src_transaction_hash = src_transaction_hash
        self.src_from_address = src_from_address
        self.src_to_address = src_to_address
        self.src_fee = src_fee
        self.src_value = src_value
        self.src_fee_usd = src_fee_usd
        self.src_timestamp = src_timestamp
        self.dst_blockchain = dst_blockchain
        self.dst_transaction_hash = dst_transaction_hash
        self.dst_from_address = dst_from_address
        self.dst_to_address = dst_to_address
        self.dst_fee = dst_fee
        self.dst_value = dst_value
        self.dst_fee_usd = dst_fee_usd
        self.dst_timestamp = dst_timestamp
        self.refund_blockchain = refund_blockchain
        self.refund_transaction_hash = refund_transaction_hash
        self.refund_from_address = refund_from_address
        self.refund_to_address = refund_to_address
        self.refund_fee = refund_fee
        self.refund_value = refund_value
        self.refund_fee_usd = refund_fee_usd
        self.refund_timestamp = refund_timestamp
        self.intent_id = intent_id
        self.depositor = depositor
        self.recipient = recipient
        self.src_contract_address = src_contract_address
        self.dst_contract_address = dst_contract_address
        self.input_amount = input_amount
        self.input_amount_usd = input_amount_usd
        self.middle_src_token = middle_src_token
        self.middle_src_amount = middle_src_amount
        self.middle_src_amount_usd = middle_src_amount_usd
        self.middle_dst_token = middle_dst_token
        self.middle_dst_amount = middle_dst_amount
        self.middle_dst_amount_usd = middle_dst_amount_usd
        self.output_amount = output_amount
        self.output_amount_usd = output_amount_usd
        self.refund_amount = refund_amount
        self.refund_amount_usd = refund_amount_usd
        self.refund_token = refund_token
        self.native_fix_fee = native_fix_fee
        self.native_fix_fee_usd = native_fix_fee_usd
        self.percent_fee = percent_fee
        self.percent_fee_usd = percent_fee_usd
