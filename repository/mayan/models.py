# ruff: noqa: E501
from sqlalchemy import BigInteger, Boolean, Column, Float, Integer, Numeric, String

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
        self.blockchain = blockchain
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
    middle_dst_token = Column(String(44), nullable=True)
    middle_dst_amount = Column(Numeric(30, 0), nullable=True)

    def __init__(
        self,
        key,
        blockchain,
        transaction_hash,
        sequence,
        net_amount,
        middle_dst_token,
        middle_dst_amount,
    ):
        self.key = key
        self.blockchain = blockchain
        self.transaction_hash = transaction_hash
        self.sequence = sequence
        self.net_amount = net_amount
        self.middle_dst_token = middle_dst_token
        self.middle_dst_amount = middle_dst_amount

    def __repr__(self):
        return (
            f"<MayanOrderFulfilled(key={self.key}, "
            f"blockchain={self.blockchain}, "
            f"transaction_hash={self.transaction_hash}, "
            f"sequence={self.sequence}, "
            f"net_amount={self.net_amount}, "
            f"middle_dst_token={self.middle_dst_token}, "
            f"middle_dst_amount={self.middle_dst_amount}>)"
        )


class MayanOrderUnlocked(Base):
    __tablename__ = "mayan_order_unlocked"

    key = Column(String(64), nullable=False, primary_key=True)
    blockchain = Column(String(10), nullable=False)
    transaction_hash = Column(String(66), nullable=False)

    def __init__(self, key, blockchain, transaction_hash):
        self.blockchain = blockchain
        self.transaction_hash = transaction_hash
        self.key = key

    def __repr__(self):
        return (
            f"<MayanOrderUnlocked(key={self.key}, "
            f"blockchain={self.blockchain}, "
            f"transaction_hash={self.transaction_hash})>"
        )


### SOLANA SPECIFIC MODELS ###


class MayanInitOrder(Base):
    __tablename__ = "mayan_init_order"

    order_hash = Column(String(64), primary_key=True, nullable=False)
    signature = Column(String(88), nullable=False)
    trader = Column(String(44), nullable=False)
    relayer = Column(String(44), nullable=False)
    state = Column(String(44), nullable=False)
    state_from_acc = Column(String(44), nullable=False)
    relayer_fee_acc = Column(String(44), nullable=False)
    middle_src_token = Column(String(44), nullable=True)
    fee_manager_program = Column(String(44), nullable=False)
    token_program = Column(String(44), nullable=False)
    system_program = Column(String(44), nullable=False)
    middle_src_amount_min = Column(Numeric(30, 0), nullable=True)
    middle_src_amount = Column(Numeric(30, 0), nullable=True)
    native_input = Column(Boolean, nullable=False)
    fee_submit = Column(Numeric(30, 0), nullable=False)
    addr_dest = Column(String(128), nullable=False)
    chain_dest = Column(String(10), nullable=False)
    token_out = Column(String(128), nullable=False)
    amount_out_min = Column(Numeric(30, 0), nullable=False)
    gas_drop = Column(Numeric(30, 0), nullable=False)
    fee_cancel = Column(Numeric(30, 0), nullable=False)
    fee_refund = Column(Numeric(30, 0), nullable=False)
    deadline = Column(BigInteger, nullable=False)
    addr_ref = Column(String(128), nullable=False)
    fee_rate_ref = Column(Integer, nullable=False)
    fee_rate_mayan = Column(Integer, nullable=False)
    auction_mode = Column(Integer, nullable=False)
    key_rnd = Column(String(128), nullable=False)
    original_src_token = Column(String(44), nullable=False)
    original_src_amount = Column(Numeric(30, 0), nullable=False)
    amm = Column(String(44), nullable=True)

    def __init__(
        self,
        order_hash,
        signature,
        trader,
        relayer,
        state,
        state_from_acc,
        relayer_fee_acc,
        middle_src_token,
        fee_manager_program,
        token_program,
        system_program,
        middle_src_amount_min,
        middle_src_amount,
        native_input,
        fee_submit,
        addr_dest,
        chain_dest,
        token_out,
        amount_out_min,
        gas_drop,
        fee_cancel,
        fee_refund,
        deadline,
        addr_ref,
        fee_rate_ref,
        fee_rate_mayan,
        auction_mode,
        key_rnd,
        original_src_token,
        original_src_amount,
        amm,
    ):
        self.trader = trader
        self.order_hash = order_hash
        self.signature = signature
        self.relayer = relayer
        self.state = state
        self.state_from_acc = state_from_acc
        self.relayer_fee_acc = relayer_fee_acc
        self.middle_src_token = middle_src_token
        self.fee_manager_program = fee_manager_program
        self.token_program = token_program
        self.system_program = system_program
        self.middle_src_amount_min = middle_src_amount_min
        self.middle_src_amount = middle_src_amount
        self.native_input = native_input
        self.fee_submit = fee_submit
        self.addr_dest = addr_dest
        self.chain_dest = chain_dest
        self.token_out = token_out
        self.amount_out_min = amount_out_min
        self.gas_drop = gas_drop
        self.fee_cancel = fee_cancel
        self.fee_refund = fee_refund
        self.deadline = deadline
        self.addr_ref = addr_ref
        self.fee_rate_ref = fee_rate_ref
        self.fee_rate_mayan = fee_rate_mayan
        self.auction_mode = auction_mode
        self.key_rnd = key_rnd
        self.original_src_token = original_src_token
        self.original_src_amount = original_src_amount
        self.amm = amm

    def __repr__(self):
        return (
            f"<MayanInitOrder(trader={self.trader}, relayer={self.relayer}, state={self.state}, "
            f"state_from_acc={self.state_from_acc}, relayer_fee_acc={self.relayer_fee_acc}, "
            f"mint_from={self.middle_src_token}, fee_manager_program={self.fee_manager_program}, "
            f"token_program={self.token_program}, system_program={self.system_program}, "
            f"middle_src_amount_min={self.middle_src_amount_min}, middle_src_amount={self.middle_src_amount}, "
            f"native_input={self.native_input}, fee_submit={self.fee_submit}, "
            f"addr_dest={self.addr_dest}, chain_dest={self.chain_dest}, "
            f"token_out={self.token_out}, amount_out_min={self.amount_out_min}, gas_drop={self.gas_drop}, "
            f"fee_cancel={self.fee_cancel}, fee_refund={self.fee_refund}, deadline={self.deadline}, "
            f"addr_ref={self.addr_ref}, fee_rate_ref={self.fee_rate_ref}, "
            f"fee_rate_mayan={self.fee_rate_mayan}, auction_mode={self.auction_mode}, "
            f"key_rnd={self.key_rnd}, order_hash={self.order_hash}, "
            f"signature={self.signature}, original_src_token={self.original_src_token}, "
            f"original_src_amount={self.original_src_amount}, amm={self.amm}>)"
        )


class MayanUnlock(Base):
    __tablename__ = "mayan_unlock"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    signature = Column(String(88), nullable=False)
    vaa_unlock = Column(String(44), nullable=False)
    state = Column(String(44), nullable=False)
    state_from_acc = Column(String(44), nullable=False)
    mint_from = Column(String(44), nullable=False)
    driver = Column(String(44), nullable=False)
    driver_acc = Column(String(44), nullable=False)
    token_program = Column(String(44), nullable=False)
    system_program = Column(String(44), nullable=False)
    amount = Column(Numeric(30, 0), nullable=False)

    def __init__(
        self,
        signature,
        vaa_unlock,
        state,
        state_from_acc,
        mint_from,
        driver,
        driver_acc,
        token_program,
        system_program,
        amount,
    ):
        self.signature = signature
        self.vaa_unlock = vaa_unlock
        self.state = state
        self.state_from_acc = state_from_acc
        self.mint_from = mint_from
        self.driver = driver
        self.driver_acc = driver_acc
        self.token_program = token_program
        self.system_program = system_program
        self.amount = amount

    def __repr__(self):
        return (
            f"<MayanUnlock(signature={self.signature}, vaa_unlock={self.vaa_unlock}, "
            f"state={self.state}, state_from_acc={self.state_from_acc}, mint_from={self.mint_from}, "
            f"driver={self.driver}, driver_acc={self.driver_acc}, token_program={self.token_program}, "
            f"system_program={self.system_program}, amount={self.amount}>"
        )


class MayanFulfillOrder(Base):
    __tablename__ = "mayan_fulfill_order"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    signature = Column(String(88), nullable=False)
    state = Column(String(44), nullable=False)
    driver = Column(String(44), nullable=False)
    state_to_acc = Column(String(44), nullable=False)
    mint_to = Column(String(44), nullable=False)
    dest = Column(String(44), nullable=False)
    system_program = Column(String(44), nullable=False)
    addr_unlocker = Column(String(64), nullable=True)
    amount = Column(Numeric(30, 0), nullable=False)
    middle_dst_token = Column(String(44), nullable=True)
    middle_dst_amount = Column(Numeric(30, 0), nullable=True)
    amm = Column(String(44), nullable=True)

    def __init__(
        self,
        signature,
        state,
        driver,
        state_to_acc,
        mint_to,
        dest,
        system_program,
        addr_unlocker,
        amount,
        middle_dst_token,
        middle_dst_amount,
        amm,
    ):
        self.signature = signature
        self.state = state
        self.driver = driver
        self.state_to_acc = state_to_acc
        self.mint_to = mint_to
        self.dest = dest
        self.system_program = system_program
        self.addr_unlocker = addr_unlocker
        self.amount = amount
        self.middle_dst_token = middle_dst_token
        self.middle_dst_amount = middle_dst_amount
        self.amm = amm

    def __repr__(self):
        return (
            f"<MayanFulfillOrder(signature={self.signature}, state={self.state}, driver={self.driver}, "
            f"state_to_acc={self.state_to_acc}, mint_to={self.mint_to}, dest={self.dest}, "
            f"system_program={self.system_program}, addr_unlocker={self.addr_unlocker}), "
            f"amount={self.amount}, middle_dst_token={self.middle_dst_token}, "
            f"middle_dst_amount={self.middle_dst_amount}, amm={self.amm}>)"
        )


class MayanSettle(Base):
    __tablename__ = "mayan_settle"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    signature = Column(String(88), nullable=False)
    state = Column(String(44), nullable=False)
    state_to_acc = Column(String(44), nullable=False)
    relayer = Column(String(44), nullable=False)
    mint_to = Column(String(44), nullable=False)
    dest = Column(String(44), nullable=False)
    referrer = Column(String(44), nullable=False)
    fee_collector = Column(String(44), nullable=False)
    referrer_fee_acc = Column(String(44), nullable=False)
    mayan_fee_acc = Column(String(44), nullable=False)
    dest_acc = Column(String(44), nullable=False)
    token_program = Column(String(44), nullable=False)
    system_program = Column(String(44), nullable=False)
    associated_token_program = Column(String(44), nullable=False)

    def __init__(
        self,
        signature,
        state,
        state_to_acc,
        relayer,
        mint_to,
        dest,
        referrer,
        fee_collector,
        referrer_fee_acc,
        mayan_fee_acc,
        dest_acc,
        token_program,
        system_program,
        associated_token_program,
    ):
        self.signature = signature
        self.state = state
        self.state_to_acc = state_to_acc
        self.relayer = relayer
        self.mint_to = mint_to
        self.dest = dest
        self.referrer = referrer
        self.fee_collector = fee_collector
        self.referrer_fee_acc = referrer_fee_acc
        self.mayan_fee_acc = mayan_fee_acc
        self.dest_acc = dest_acc
        self.token_program = token_program
        self.system_program = system_program
        self.associated_token_program = associated_token_program

    def __repr__(self):
        return (
            f"<MayanSettle(signature={self.signature}, state={self.state}, state_to_acc={self.state_to_acc}, "
            f"relayer={self.relayer}, mint_to={self.mint_to}, dest={self.dest}, referrer={self.referrer}, "
            f"fee_collector={self.fee_collector}, referrer_fee_acc={self.referrer_fee_acc}, "
            f"mayan_fee_acc={self.mayan_fee_acc}, dest_acc={self.dest_acc}, token_program={self.token_program}, "
            f"system_program={self.system_program}, associated_token_program={self.associated_token_program})>"
        )


class MayanSetAuctionWinner(Base):
    __tablename__ = "mayan_set_auction_winner"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    signature = Column(String(88), nullable=False)
    state = Column(String(44), nullable=False)
    auction = Column(String(44), nullable=False)
    expected_winner = Column(String(64), nullable=False)

    def __init__(
        self,
        signature,
        state,
        auction,
        expected_winner,
    ):
        self.signature = signature
        self.state = state
        self.auction = auction
        self.expected_winner = expected_winner

    def __repr__(self):
        return (
            f"<MayanSetAuctionWinner(signature={self.signature}, state={self.state}, "
            f"auction={self.auction}, expected_winner={self.expected_winner})>"
        )


class MayanRegisterOrder(Base):
    __tablename__ = "mayan_register_order"

    order_hash = Column(String(64), primary_key=True, nullable=False)
    signature = Column(String(88), nullable=False)
    relayer = Column(String(44), nullable=False)
    state = Column(String(44), nullable=False)
    system_program = Column(String(44), nullable=False)
    trader = Column(String(128), nullable=False)
    chain_source = Column(String(10), nullable=False)
    token_in = Column(String(128), nullable=False)
    addr_dest = Column(String(128), nullable=False)
    chain_dest = Column(String(10), nullable=False)
    token_out = Column(String(128), nullable=False)
    amount_out_min = Column(Numeric(30, 0), nullable=False)
    gas_drop = Column(Numeric(30, 0), nullable=False)
    fee_cancel = Column(Numeric(30, 0), nullable=False)
    fee_refund = Column(Numeric(30, 0), nullable=False)
    deadline = Column(BigInteger, nullable=False)
    addr_ref = Column(String(128), nullable=False)
    fee_rate_ref = Column(Integer, nullable=False)
    fee_rate_mayan = Column(Integer, nullable=False)
    auction_mode = Column(Integer, nullable=False)
    key_rnd = Column(String(128), nullable=False)

    def __init__(
        self,
        order_hash,
        signature,
        relayer,
        state,
        system_program,
        trader,
        chain_source,
        token_in,
        addr_dest,
        chain_dest,
        token_out,
        amount_out_min,
        gas_drop,
        fee_cancel,
        fee_refund,
        deadline,
        addr_ref,
        fee_rate_ref,
        fee_rate_mayan,
        auction_mode,
        key_rnd,
    ):
        self.order_hash = order_hash
        self.signature = signature
        self.relayer = relayer
        self.state = state
        self.system_program = system_program
        self.trader = trader
        self.chain_source = chain_source
        self.token_in = token_in
        self.addr_dest = addr_dest
        self.chain_dest = chain_dest
        self.token_out = token_out
        self.amount_out_min = amount_out_min
        self.gas_drop = gas_drop
        self.fee_cancel = fee_cancel
        self.fee_refund = fee_refund
        self.deadline = deadline
        self.addr_ref = addr_ref
        self.fee_rate_ref = fee_rate_ref
        self.fee_rate_mayan = fee_rate_mayan
        self.auction_mode = auction_mode
        self.key_rnd = key_rnd

    def __repr__(self):
        return (
            f"<MayanRegisterOrder(order_hash={self.order_hash}, relayer={self.relayer}, "
            f"state={self.state}, system_program={self.system_program}, trader={self.trader}, "
            f"chain_source={self.chain_source}, token_in={self.token_in}, addr_dest={self.addr_dest}, "
            f"chain_dest={self.chain_dest}, token_out={self.token_out}, amount_out_min={self.amount_out_min}, "
            f"gas_drop={self.gas_drop}, fee_cancel={self.fee_cancel}, fee_refund={self.fee_refund}, "
            f"deadline={self.deadline}, addr_ref={self.addr_ref}, fee_rate_ref={self.fee_rate_ref}, "
            f"fee_rate_mayan={self.fee_rate_mayan}, auction_mode={self.auction_mode}, key_rnd={self.key_rnd})>"
        )


class MayanAuctionBid(Base):
    __tablename__ = "mayan_auction_bid"

    signature = Column(String(88), primary_key=True, nullable=False)
    config = Column(String(128), nullable=False)
    driver = Column(String(44), nullable=False)
    auction_state = Column(String(44), nullable=False)
    system_program = Column(String(44), nullable=False)
    trader = Column(String(128), nullable=False)
    chain_source = Column(String(10), nullable=False)
    token_in = Column(String(128), nullable=False)
    addr_dest = Column(String(128), nullable=False)
    chain_dest = Column(String(10), nullable=False)
    token_out = Column(String(128), nullable=False)
    amount_out_min = Column(Numeric(30, 0), nullable=False)
    gas_drop = Column(Numeric(30, 0), nullable=False)
    fee_cancel = Column(Numeric(30, 0), nullable=False)
    fee_refund = Column(Numeric(30, 0), nullable=False)
    deadline = Column(BigInteger, nullable=False)
    addr_ref = Column(String(128), nullable=False)
    fee_rate_ref = Column(Integer, nullable=False)
    fee_rate_mayan = Column(Integer, nullable=False)
    auction_mode = Column(Integer, nullable=False)
    key_rnd = Column(String(128), nullable=False)
    amount_bid = Column(Numeric(30, 0), nullable=False)
    order_hash = Column(String(64), primary_key=True, nullable=False)

    def __init__(
        self,
        signature,
        config,
        driver,
        auction_state,
        system_program,
        trader,
        chain_source,
        token_in,
        addr_dest,
        chain_dest,
        token_out,
        amount_out_min,
        gas_drop,
        fee_cancel,
        fee_refund,
        deadline,
        addr_ref,
        fee_rate_ref,
        fee_rate_mayan,
        auction_mode,
        key_rnd,
        amount_bid,
        order_hash,
    ):
        self.config = config
        self.signature = signature
        self.driver = driver
        self.auction_state = auction_state
        self.system_program = system_program
        self.trader = trader
        self.chain_source = chain_source
        self.token_in = token_in
        self.addr_dest = addr_dest
        self.chain_dest = chain_dest
        self.token_out = token_out
        self.amount_out_min = amount_out_min
        self.gas_drop = gas_drop
        self.fee_cancel = fee_cancel
        self.fee_refund = fee_refund
        self.deadline = deadline
        self.addr_ref = addr_ref
        self.fee_rate_ref = fee_rate_ref
        self.fee_rate_mayan = fee_rate_mayan
        self.auction_mode = auction_mode
        self.key_rnd = key_rnd
        self.amount_bid = amount_bid
        self.order_hash = order_hash

    def __repr__(self):
        return (
            f"<MayanAuctionBid(signature={self.signature}, config={self.config}, "
            f"driver={self.driver}, auction_state={self.auction_state}, system_program={self.system_program}, "
            f"trader={self.trader}, chain_source={self.chain_source}, token_in={self.token_in}, "
            f"addr_dest={self.addr_dest}, chain_dest={self.chain_dest}, "
            f"token_out={self.token_out}, amount_out_min={self.amount_out_min}, "
            f"gas_drop={self.gas_drop}, fee_cancel={self.fee_cancel}, "
            f"fee_refund={self.fee_refund}, deadline={self.deadline}, "
            f"addr_ref={self.addr_ref}, fee_rate_ref={self.fee_rate_ref}, "
            f"fee_rate_mayan={self.fee_rate_mayan}, auction_mode={self.auction_mode}, "
            f"key_rnd={self.key_rnd}, amount_bid={self.amount_bid}), order_hash={self.order_hash})>"
        )


class MayanAuctionClose(Base):
    __tablename__ = "mayan_auction_close"

    signature = Column(String(88), nullable=False)
    auction = Column(String(44), primary_key=True, nullable=False)
    initializer = Column(String(44), nullable=False)

    def __init__(self, signature, auction, initializer):
        self.signature = signature
        self.auction = auction
        self.initializer = initializer

    def __repr__(self):
        return (
            f"<MayanAuctionClose(signature={self.signature}, auction={self.auction}, "
            f"initializer={self.initializer})>"
        )


class MayanBlockchainTransaction(BlockchainTransaction):
    __tablename__ = "mayan_blockchain_transactions"

    def __repr__(self):
        return (
            f"<MayanBlockchainTransaction(blockchain={self.blockchain}, "
            f"transaction_hash={self.transaction_hash}, "
            f"block_number={self.block_number}, "
            f"timestamp={self.timestamp} "
            f"from_address={self.from_address}, "
            f"to_address={self.to_address}, "
            f"value={self.value}, "
            f"status={self.status}, "
            f"fee={self.fee}>"
        )


########## Processed Data ##########


class MayanCrossChainTransaction(Base):
    __tablename__ = "mayan_cross_chain_transactions"

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
    src_contract_address = Column(String(44), nullable=False)
    dst_contract_address = Column(String(44), nullable=False)
    input_amount = Column(Numeric(30, 0), nullable=False)
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
    auction_id = Column(String(64), nullable=True)
    auction_first_bid_timestamp = Column(BigInteger, nullable=True)
    auction_last_bid_timestamp = Column(BigInteger, nullable=True)
    auction_number_of_bids = Column(Integer, nullable=True)
    native_fix_fee = Column(Numeric(30, 0), nullable=False)
    native_fix_fee_usd = Column(Float, nullable=True)
    percent_fee = Column(Numeric(30, 0), nullable=False)
    percent_fee_usd = Column(Float, nullable=True)

    # in mayan, percent_fee is usually 0.03% and goes to the protocol (paid on the dst chain)
    # there is no fix fee (native_fix_fee)
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
        auction_id,
        auction_first_bid_timestamp,
        auction_last_bid_timestamp,
        auction_number_of_bids,
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
        self.auction_id = auction_id
        self.auction_first_bid_timestamp = auction_first_bid_timestamp
        self.auction_last_bid_timestamp = auction_last_bid_timestamp
        self.auction_number_of_bids = auction_number_of_bids
        self.native_fix_fee = native_fix_fee
        self.native_fix_fee_usd = native_fix_fee_usd
        self.percent_fee = percent_fee
        self.percent_fee_usd = percent_fee_usd
