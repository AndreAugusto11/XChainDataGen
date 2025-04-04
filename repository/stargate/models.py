from sqlalchemy import BigInteger, Column, Float, Integer, Numeric, String

from repository.database import Base


class StargateOFTSent(Base):
    __tablename__ = "stargate_oft_sent"

    id                  = Column(Integer,       nullable=False, autoincrement=True, primary_key=True)
    blockchain          = Column(String(10),    nullable=False)
    transaction_hash    = Column(String(66),    nullable=False)
    contract_address    = Column(String(42),    nullable=False)
    guid                = Column(String(66),    nullable=False)
    dst_blockchain      = Column(String(10),    nullable=False)
    from_address        = Column(String(42),    nullable=False)
    amount_sent_ld      = Column(Numeric(30,0), nullable=False)
    amount_received_ld  = Column(Numeric(30,0), nullable=False)

    def __init__(
        self,
        blockchain,
        transaction_hash,
        contract_address,
        guid,
        dst_blockchain,
        from_address,
        amount_sent_ld,
        amount_received_ld,
    ):
        self.blockchain = blockchain
        self.transaction_hash = transaction_hash
        self.contract_address = contract_address
        self.guid = guid
        self.dst_blockchain = dst_blockchain
        self.from_address = from_address
        self.amount_sent_ld = amount_sent_ld
        self.amount_received_ld = amount_received_ld

    def __repr__(self):
        return f"<StargateOFTSent(blockchain={self.blockchain}, transaction_hash={self.transaction_hash}, contract_address={self.contract_address} guid={self.guid}, dst_blockchain={self.dst_blockchain}, from_address={self.from_address}, amount_sent_ld={self.amount_sent_ld}, amount_received_ld={self.amount_received_ld})>"


class StargateOFTReceived(Base):
    __tablename__ = "stargate_oft_received"

    id                  = Column(Integer,       nullable=False, autoincrement=True, primary_key=True)
    blockchain          = Column(String(10),    nullable=False)
    transaction_hash    = Column(String(66),    nullable=False)
    contract_address    = Column(String(42),    nullable=False)
    guid                = Column(String(66),    nullable=False)
    src_blockchain      = Column(String(10),    nullable=False)
    to_address          = Column(String(42),    nullable=False)
    amount_received_ld  = Column(Numeric(30,0), nullable=False)

    def __init__(self, blockchain, transaction_hash, contract_address, guid, src_blockchain, to_address, amount_received_ld):
        self.blockchain = blockchain
        self.transaction_hash = transaction_hash
        self.contract_address = contract_address
        self.guid = guid
        self.src_blockchain = src_blockchain
        self.to_address = to_address
        self.amount_received_ld = amount_received_ld

    def __repr__(self):
        return f"<StargateOFTReceived(blockchain={self.blockchain}, transaction_hash={self.transaction_hash}, contract_address={self.contract_address}, guid={self.guid}, src_blockchain={self.src_blockchain}, to_address={self.to_address}, amount_received_ld={self.amount_received_ld})>"


class StargateOFTSendToChain(Base):
    __tablename__ = "stargate_oft_send_to_chain"

    id                  = Column(Integer,       nullable=False, autoincrement=True, primary_key=True)
    blockchain          = Column(String(10),    nullable=False)
    transaction_hash    = Column(String(66),    nullable=False)
    contract_address    = Column(String(42),    nullable=False)
    dst_blockchain      = Column(String(10),    nullable=False)
    from_address        = Column(String(42))
    to_address          = Column(String(42),    nullable=False)
    amount              = Column(Numeric(30,0), nullable=False)

    def __init__(self, blockchain, transaction_hash, contract_address, dst_blockchain, from_address, to_address, amount):
        self.blockchain = blockchain
        self.transaction_hash = transaction_hash
        self.contract_address = contract_address
        self.dst_blockchain = dst_blockchain
        self.from_address = from_address
        self.to_address = to_address
        self.amount = amount

    def __repr__(self):
        return f"<StargateOFTSendToChain(blockchain={self.blockchain}, transaction_hash={self.transaction_hash}, contract_address={self.contract_address}, dst_blockchain={self.dst_blockchain}, to_address={self.to_address}, amount={self.amount})>"


class StargateOFTReceiveFromChain(Base):
    __tablename__ = "stargate_oft_receive_from_chain"

    id                  = Column(Integer,    nullable=False, autoincrement=True, primary_key=True)
    blockchain          = Column(String(10), nullable=False)
    transaction_hash    = Column(String(66), nullable=False)
    contract_address    = Column(String(42), nullable=False)
    src_blockchain      = Column(String(10), nullable=False)
    to_address          = Column(String(42))
    nonce               = Column(Integer)
    amount              = Column(Numeric(30,0), nullable=False)

    def __init__(self, blockchain, transaction_hash, contract_address, src_blockchain, to_address, nonce, amount):
        self.blockchain = blockchain
        self.transaction_hash = transaction_hash
        self.contract_address = contract_address
        self.src_blockchain = src_blockchain
        self.to_address = to_address
        self.nonce = nonce
        self.amount = amount

    def __repr__(self):
        return f"<StargateOFTReceiveFromChain(blockchain={self.blockchain}, transaction_hash={self.transaction_hash}, contract_address={self.contract_address}, src_blockchain={self.src_blockchain}, amount={self.amount})>"


class StargateUlnConfigSet(Base):
    __tablename__ = "stargate_uln_config_set"

    id                     = Column(Integer,     nullable=False, autoincrement=True, primary_key=True)
    blockchain             = Column(String(10),  nullable=False)
    transaction_hash       = Column(String(66),  nullable=False)
    oapp                   = Column(String(42),  nullable=False)
    dst_blockchain         = Column(String(10),  nullable=False)
    confirmations          = Column(Integer,     nullable=False)
    required_dvn_count     = Column(Integer,     nullable=False)
    optional_dvn_count     = Column(Integer,     nullable=False)
    optional_dvn_threshold = Column(Integer,     nullable=False)
    required_dvns          = Column(String(255), nullable=False)
    optional_dvns          = Column(String(255), nullable=False)

    def __init__(
        self,
        blockchain,
        transaction_hash,
        oapp,
        dst_blockchain,
        confirmations,
        required_dvn_count,
        optional_dvn_count,
        optional_dvn_threshold,
        required_dvns,
        optional_dvns,
    ):
        self.blockchain = blockchain
        self.transaction_hash = transaction_hash
        self.oapp = oapp
        self.dst_blockchain = dst_blockchain
        self.confirmations = confirmations
        self.required_dvn_count = required_dvn_count
        self.optional_dvn_count = optional_dvn_count
        self.optional_dvn_threshold = optional_dvn_threshold
        self.required_dvns = required_dvns
        self.optional_dvns = optional_dvns

    def __repr__(self):
        return f"<StargateUlnConfigSet(blockchain={self.blockchain}, transaction_hash={self.transaction_hash}, oapp={self.oapp}, dst_blockchain={self.dst_blockchain}, confirmations={self.confirmations}, required_dvn_count={self.required_dvn_count}, optional_dvn_count={self.optional_dvn_count}, optional_dvn_threshold={self.optional_dvn_threshold}, required_dvns={self.required_dvns}, optional_dvns={self.optional_dvns})>"


class StargateExecutorFeePaid(Base):
    __tablename__ = "stargate_executor_fee_paid"

    id                  = Column(Integer,       nullable=False, autoincrement=True, primary_key=True)
    blockchain          = Column(String(10),    nullable=False)
    transaction_hash    = Column(String(66),    nullable=False)
    executor            = Column(String(42),    nullable=False)
    fee                 = Column(Numeric(30,0), nullable=False)

    def __init__(self, blockchain, transaction_hash, executor, fee):
        self.blockchain = blockchain
        self.transaction_hash = transaction_hash
        self.executor = executor
        self.fee = fee

    def __repr__(self):
        return f"<StargateExecutorFeePaid(id={self.id}, blockchain={self.blockchain}, transaction_hash={self.transaction_hash}, executor={self.executor}, fee={self.fee})>"


class StargateDVNFeePaid(Base):
    __tablename__ = "stargate_dvn_fee_paid"

    id                  = Column(Integer,       nullable=False, autoincrement=True, primary_key=True)
    blockchain          = Column(String(10),    nullable=False)
    transaction_hash    = Column(String(66),    nullable=False)
    fee                 = Column(Numeric(30,0), nullable=False)

    def __init__(self, blockchain, transaction_hash, fee):
        self.blockchain = blockchain
        self.transaction_hash = transaction_hash
        self.fee = fee

    def __repr__(self):
        return f"<StargateDVNFeePaid(blockchain={self.blockchain}, transaction_hash={self.transaction_hash}, fees={self.fee})>"


class StargateBusRode(Base):
    __tablename__ = "stargate_bus_rode"

    blockchain          = Column(String(10),    nullable=False, primary_key=True)
    transaction_hash    = Column(String(66),    nullable=False)
    dst_blockchain      = Column(String(10),    nullable=False, primary_key=True)
    ticket_id           = Column(Integer,       nullable=False, primary_key=True)
    fare                = Column(Numeric(30,0), nullable=False)
    passenger           = Column(String(256),   nullable=False)

    def __init__(self, blockchain, transaction_hash, dst_blockchain, ticket_id, fare, passenger):
        self.blockchain = blockchain
        self.transaction_hash = transaction_hash
        self.dst_blockchain = dst_blockchain
        self.ticket_id = ticket_id
        self.fare = fare
        self.passenger = passenger

    def __repr__(self):
        return f"<StargateBusRode(blockchain={self.blockchain}, transaction_hash={self.transaction_hash}, dst_blockchain={self.dst_blockchain}, ticket_id={self.ticket_id}, fare={self.fare}, passenger={self.passenger})>"


class StargateBusDriven(Base):
    __tablename__ = "stargate_bus_driven"

    id                  = Column(Integer,    nullable=False, autoincrement=True, primary_key=True)
    blockchain          = Column(String(10), nullable=False)
    transaction_hash    = Column(String(66), nullable=False)
    dst_blockchain      = Column(String(10), nullable=False)
    start_ticket_id     = Column(BigInteger, nullable=False)
    num_passengers      = Column(Integer,    nullable=False)
    guid                = Column(String(66), nullable=False)

    def __init__(
        self, blockchain, transaction_hash, dst_blockchain, start_ticket_id, num_passengers, guid
    ):
        self.blockchain = blockchain
        self.transaction_hash = transaction_hash
        self.dst_blockchain = dst_blockchain
        self.start_ticket_id = start_ticket_id
        self.num_passengers = num_passengers
        self.guid = guid

    def __repr__(self):
        return f"<StargateBusDriven(blockchain={self.blockchain}, transaction_hash={self.transaction_hash}, dst_blockchain={self.dst_blockchain}, start_ticket_id={self.start_ticket_id}, num_passengers={self.num_passengers}, guid={self.guid})>"


class StargatePacketSent(Base):
    __tablename__ = "stargate_packet_sent"


    guid                = Column(String(66),    nullable=False, primary_key=True)
    blockchain          = Column(String(10),    nullable=False)
    transaction_hash    = Column(String(66),    nullable=False)
    nonce               = Column(Integer,       nullable=False)
    version             = Column(String(1),     nullable=False)
    src_blockchain      = Column(String(10),    nullable=False)
    sender              = Column(String(42),    nullable=False)
    dst_blockchain      = Column(String(10),    nullable=False)
    receiver            = Column(String(42),    nullable=False)
    message             = Column(String(10000), nullable=False)

    def __init__(
        self,
        blockchain,
        guid,
        transaction_hash,
        nonce,
        version,
        src_blockchain,
        sender,
        dst_blockchain,
        receiver,
        message,
    ):
        self.blockchain = blockchain
        self.guid = guid
        self.transaction_hash = transaction_hash
        self.nonce = nonce
        self.version = version
        self.src_blockchain = src_blockchain
        self.sender = sender
        self.dst_blockchain = dst_blockchain
        self.receiver = receiver
        self.message = message

    def __repr__(self):
        return f"<StargatePacketSent(blockchain={self.blockchain}, guid={self.guid}, transaction_hash={self.transaction_hash}, version={self.version}, nonce={self.nonce}, src_blockchain={self.src_blockchain}, sender={self.sender}, dst_blockchain={self.dst_blockchain}, receiver={self.receiver}, message={self.message})>"


class StargatePacketReceived(Base):
    __tablename__ = "stargate_packet_received"

    id                  = Column(Integer,    nullable=False, autoincrement=True, primary_key=True)
    blockchain          = Column(String(10), nullable=False)
    transaction_hash    = Column(String(66), nullable=False)
    src_blockchain      = Column(String(10), nullable=False)
    src_address         = Column(String(42), nullable=False)
    dst_address         = Column(String(42), nullable=False)
    nonce               = Column(Integer,    nullable=False)
    payload_hash        = Column(String(66), nullable=False)

    def __init__(
        self,
        blockchain,
        transaction_hash,
        src_blockchain,
        src_address,
        dst_address,
        nonce,
        payload_hash,
    ):
        self.blockchain = blockchain
        self.transaction_hash = transaction_hash
        self.src_blockchain = src_blockchain
        self.src_address = src_address
        self.dst_address = dst_address
        self.nonce = nonce
        self.payload_hash = payload_hash

    def __repr__(self):
        return f"<StargatePacketReceived(blockchain={self.blockchain}, transaction_hash={self.transaction_hash}, src_blockchain={self.src_blockchain}, src_address={self.src_address}, dst_address={self.dst_address}, nonce={self.nonce}, payload_hash={self.payload_hash})>"    


class StargatePacket(Base):
    __tablename__ = "stargate_packet"

    id                  = Column(Integer,       nullable=False, autoincrement=True, primary_key=True)
    blockchain          = Column(String(10),    nullable=False)
    transaction_hash    = Column(String(66),    nullable=False)
    nonce               = Column(Integer,       nullable=False)
    src_blockchain      = Column(String(10),    nullable=False)
    src_address         = Column(String(42),    nullable=False)
    dst_blockchain      = Column(String(10),    nullable=False)
    dst_address         = Column(String(42),    nullable=False)
    payload             = Column(String(10000), nullable=False)

    def __init__(
        self,
        blockchain,
        transaction_hash,
        nonce,
        src_blockchain,
        src_address,
        dst_blockchain,
        dst_address,
        payload,
    ):
        self.blockchain = blockchain
        self.transaction_hash = transaction_hash
        self.nonce = nonce
        self.src_blockchain = src_blockchain
        self.src_address = src_address
        self.dst_blockchain = dst_blockchain
        self.dst_address = dst_address
        self.payload = payload

    def __repr__(self):
        return f"<StargatePacket(blockchain={self.blockchain}, transaction_hash={self.transaction_hash}, nonce={self.nonce}, src_blockchain={self.src_blockchain}, src_address={self.src_address}, dst_blockchain={self.dst_blockchain}, dst_address={self.dst_address}, payload={self.payload})>"


class StargatePacketDelivered(Base):
    __tablename__ = "stargate_packet_delivered"

    id                  = Column(Integer,    nullable=False, autoincrement=True, primary_key=True)
    blockchain          = Column(String(10), nullable=False)
    transaction_hash    = Column(String(66), nullable=False)
    src_blockchain      = Column(String(10), nullable=False)
    sender              = Column(String(42), nullable=False)
    nonce               = Column(Integer,    nullable=False)
    receiver            = Column(String(42), nullable=False)

    def __init__(self, blockchain, transaction_hash, src_blockchain, sender, nonce, receiver):
        self.blockchain = blockchain
        self.transaction_hash = transaction_hash
        self.src_blockchain = src_blockchain
        self.sender = sender
        self.nonce = nonce
        self.receiver = receiver

    def __repr__(self):
        return f"<StargatePacketDelivered(blockchain={self.blockchain}, transaction_hash={self.transaction_hash}, src_blockchain={self.src_blockchain}, sender={self.sender}, nonce={self.nonce}, receiver={self.receiver})>"


class StargatePacketVerified(Base):
    __tablename__ = "stargate_packet_verified"

    id                  = Column(Integer,     nullable=False, autoincrement=True, primary_key=True)
    blockchain          = Column(String(10),  nullable=False)
    transaction_hash    = Column(String(66),  nullable=False)
    src_blockchain      = Column(String(10),  nullable=False)
    nonce               = Column(Integer,     nullable=False)
    sender              = Column(String(66),  nullable=False)
    receiver            = Column(String(42),  nullable=False)
    payload_hash         = Column(String(255), nullable=False)

    def __init__(self, blockchain, transaction_hash, src_blockchain, sender, nonce, receiver, payload_hash):
        self.blockchain = blockchain
        self.transaction_hash = transaction_hash
        self.src_blockchain = src_blockchain
        self.sender = sender
        self.nonce = nonce
        self.receiver = receiver
        self.payload_hash = payload_hash

    def __repr__(self):
        return f"<StargatePacketVerified(blockchain={self.blockchain}, transaction_hash={self.transaction_hash}, src_blockchain={self.src_blockchain}, sender={self.sender}, nonce={self.nonce}, receiver={self.receiver}, payload_hash={self.payload_hash})>"


class StargatePayloadVerified(Base):
    __tablename__ = "stargate_payload_verified"

    id                  = Column(Integer,     nullable=False, autoincrement=True, primary_key=True)
    blockchain          = Column(String(10),  nullable=False)
    transaction_hash    = Column(String(66),  nullable=False)
    dvn                 = Column(String(42),  nullable=False)
    header              = Column(String(255), nullable=False)
    confirmations       = Column(String(30),  nullable=False)
    proof_hash          = Column(String(66),  nullable=False)

    def __init__(self, blockchain, transaction_hash, dvn, header, confirmations, proof_hash):
        self.blockchain = blockchain
        self.transaction_hash = transaction_hash
        self.dvn = dvn
        self.header = header
        self.confirmations = confirmations
        self.proof_hash = proof_hash

    def __repr__(self):
        return f"<PayloadVerified(blockchain={self.blockchain}, transaction_hash={self.transaction_hash}, dvn={self.dvn}, header={self.header}, confirmations={self.confirmations}, proof_hash={self.proof_hash})>"


class StargateSwap(Base):
    __tablename__ = "stargate_swap"

    id                  = Column(Integer,       nullable=False, autoincrement=True, primary_key=True)
    blockchain          = Column(String(10),    nullable=False)
    transaction_hash    = Column(String(66),    nullable=False)
    contract_address    = Column(String(42),    nullable=False)
    dst_blockchain      = Column(String(10),    nullable=False)
    dst_pool_id         = Column(Integer,       nullable=False)
    from_address        = Column(String(42),    nullable=False)
    amount_sd           = Column(Numeric(30,0), nullable=False)
    eq_reward           = Column(Numeric(30,0), nullable=False)
    eq_fee              = Column(Numeric(30,0), nullable=False)
    protocol_fee        = Column(Numeric(30,0), nullable=False)
    lp_fee              = Column(Numeric(30,0), nullable=False)
    

    def __init__(
        self,
        blockchain,
        transaction_hash,
        contract_address,
        dst_blockchain,
        dst_pool_id,
        from_address,
        amount_sd,
        eq_reward,
        eq_fee,
        protocol_fee,
        lp_fee,
    ):
        self.blockchain = blockchain
        self.transaction_hash = transaction_hash
        self.contract_address = contract_address
        self.dst_blockchain = dst_blockchain
        self.dst_pool_id = dst_pool_id
        self.from_address = from_address
        self.amount_sd = amount_sd
        self.eq_reward = eq_reward
        self.eq_fee = eq_fee
        self.protocol_fee = protocol_fee
        self.lp_fee = lp_fee

    def __repr__(self):
        return f"<StargateSwap(blockchain={self.blockchain}, transaction_hash={self.transaction_hash}, contract_address={self.contract_address}, dst_blockchain={self.dst_blockchain}, dst_pool_id={self.dst_pool_id}, from_address={self.from_address}, amount_sd={self.amount_sd}, eq_reward={self.eq_reward}, eq_fee={self.eq_fee}, protocol_fee={self.protocol_fee}, lp_fee={self.lp_fee})>"


class StargateSwapRemote(Base):
    __tablename__ = "stargate_swap_remote"

    id                  = Column(Integer,       nullable=False, autoincrement=True, primary_key=True)
    blockchain          = Column(String(10),    nullable=False)
    transaction_hash    = Column(String(66),    nullable=False)
    contract_address    = Column(String(42),    nullable=False)
    to_address          = Column(String(42),    nullable=False)
    amount_sd           = Column(Numeric(30,0), nullable=False)
    protocol_fee        = Column(Numeric(30,0), nullable=False)
    dst_fee             = Column(Numeric(30,0), nullable=False)

    def __init__(self, blockchain, transaction_hash, contract_address, to_address, amount_sd, protocol_fee, dst_fee):
        self.blockchain = blockchain
        self.transaction_hash = transaction_hash
        self.contract_address = contract_address
        self.to_address = to_address
        self.amount_sd = amount_sd
        self.protocol_fee = protocol_fee
        self.dst_fee = dst_fee

    def __repr__(self):
        return f"<StargateSwapRemote(blockchain={self.blockchain}, transaction_hash={self.transaction_hash}, contract_address={self.contract_address}, to_address={self.to_address}, amount_sd={self.amount_sd}, protocol_fee={self.protocol_fee}, dst_fee={self.dst_fee})>"


class StargateComposeSent(Base):
    __tablename__ = "stargate_compose_sent"

    id                  = Column(Integer,       nullable=False, autoincrement=True, primary_key=True)
    blockchain          = Column(String(10),    nullable=False)
    transaction_hash    = Column(String(66),    nullable=False)
    from_address        = Column(String(42),    nullable=False)
    to_address          = Column(String(42),    nullable=False)
    guid                = Column(String(66),    nullable=False)
    index               = Column(Integer,       nullable=False)
    message             = Column(String(10000), nullable=False)

    def __init__(self, blockchain, transaction_hash, from_address, to_address, guid, index, message):
        self.blockchain = blockchain
        self.transaction_hash = transaction_hash
        self.from_address = from_address
        self.to_address = to_address
        self.guid = guid
        self.index = index
        self.message = message

    def __repr__(self):
        return f"<StargateComposeSent(blockchain={self.blockchain}, transaction_hash={self.transaction_hash}, from_address={self.from_address}, to_address={self.to_address}, guid={self.guid}, index={self.index}, message={self.message})>"


class StargateComposeDelivered(Base):
    __tablename__ = "stargate_compose_delivered"

    id                  = Column(Integer,    nullable=False, autoincrement=True, primary_key=True)
    blockchain          = Column(String(10), nullable=False)
    transaction_hash    = Column(String(66), nullable=False)
    from_address        = Column(String(42), nullable=False)
    to_address          = Column(String(42), nullable=False)
    guid                = Column(String(66), nullable=False)
    index               = Column(Integer,    nullable=False)

    def __init__(self, blockchain, transaction_hash, from_address, to_address, guid, index):
        self.blockchain = blockchain
        self.transaction_hash = transaction_hash
        self.from_address = from_address
        self.to_address = to_address
        self.guid = guid
        self.index = index

    def __repr__(self):
        return f"<StargateComposeDelivered(blockchain={self.blockchain}, transaction_hash={self.transaction_hash}, from_address={self.from_address}, to_address={self.to_address}, guid={self.guid}, index={self.index})>"


class StargateVerifierFee(Base):
    __tablename__ = "stargate_verifier_fee"

    id                  = Column(Integer,       nullable=False, autoincrement=True, primary_key=True)
    blockchain          = Column(String(10),    nullable=False)
    transaction_hash    = Column(String(66),    nullable=False)
    fee                 = Column(Numeric(30,0), nullable=False)

    def __init__(self, blockchain, transaction_hash, fee):
        self.blockchain = blockchain
        self.transaction_hash = transaction_hash
        self.fee = fee

    def __repr__(self):
        return f"<StargateVerifierFee(blockchain={self.blockchain}, transaction_hash={self.transaction_hash}, fee={self.fee})>"


class StargateRelayerFee(Base):
    __tablename__ = "stargate_relayer_fee"

    id                  = Column(Integer,       nullable=False, autoincrement=True, primary_key=True)
    blockchain          = Column(String(10),    nullable=False)
    transaction_hash    = Column(String(66),    nullable=False)
    fee                 = Column(Numeric(30,0), nullable=False)

    def __init__(self, blockchain, transaction_hash, fee):
        self.blockchain = blockchain
        self.transaction_hash = transaction_hash
        self.fee = fee

    def __repr__(self):
        return f"<StargateRelayerFee(blockchain={self.blockchain}, transaction_hash={self.transaction_hash}, fee={self.fee})>"


class StargateBlockchainTransaction(Base):
    __tablename__ = "stargate_blockchain_transactions"

    blockchain          = Column(String(10),    nullable=False)
    transaction_hash    = Column(String(66),    nullable=False, primary_key=True)
    block_number        = Column(Integer,       nullable=False)
    timestamp           = Column(BigInteger,    nullable=False)
    from_address        = Column(String(42),    nullable=False)
    to_address          = Column(String(42),    nullable=False)
    status              = Column(Integer,       nullable=False)
    fee                 = Column(Numeric(30,0), nullable=False)

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
        return f"<StargateBlockchainTransaction(blockchain={self.blockchain}, transaction_hash={self.transaction_hash}, block_number={self.block_number}, timestamp={self.timestamp} from_address={self.from_address}, to_address={self.to_address}, status={self.status})>"


########## Processed Data ##########


class StargateBusCrossChainTransaction(Base):
    __tablename__ = "stargate_bus_cross_chain_transactions"

    id                     = Column(Integer,       nullable=False, autoincrement=True, primary_key=True)
    src_blockchain         = Column(String(10),    nullable=False)
    user_transaction_hash  = Column(String(66),    nullable=False)
    user_from_address      = Column(String(42),    nullable=False)
    user_to_address        = Column(String(42),    nullable=False)
    user_fee               = Column(Numeric(30,0), nullable=False)
    user_fee_usd           = Column(Float,         nullable=True)
    user_timestamp         = Column(BigInteger,    nullable=False)
    bus_transaction_hash   = Column(String(66),    nullable=False)
    bus_from_address       = Column(String(42),    nullable=False)
    bus_to_address         = Column(String(42),    nullable=False)
    bus_fee                = Column(Numeric(30,0), nullable=False)
    bus_fee_usd            = Column(Float,         nullable=True)
    bus_timestamp          = Column(BigInteger,    nullable=False)
    bus_ticket_id          = Column(Integer,       nullable=False)
    bus_fare               = Column(Numeric(30,0), nullable=False)
    bus_fare_usd           = Column(Float,         nullable=True)
    bus_guid               = Column(String(66),    nullable=False)
    passenger              = Column(String(256),   nullable=False)
    dst_blockchain         = Column(String(10),    nullable=False)
    executor_fee           = Column(Numeric(30,0), nullable=False)
    executor_fee_usd       = Column(Float,         nullable=True)
    dvn_fee                = Column(Numeric(30,0), nullable=False)
    dvn_fee_usd            = Column(Float,         nullable=True)
    src_contract_address   = Column(String(42),    nullable=False)
    dst_contract_address   = Column(String(42),    nullable=False)
    amount_sent_ld         = Column(Numeric(30,0), nullable=False)
    amount_sent_ld_usd     = Column(Float,         nullable=True)
    amount_received_ld     = Column(Numeric(30,0), nullable=False)
    amount_received_ld_usd = Column(Float,        nullable=True)
    dst_transaction_hash   = Column(String(66),    nullable=False)
    dst_from_address       = Column(String(42),    nullable=False)
    dst_to_address         = Column(String(42),    nullable=False)
    dst_fee                = Column(Numeric(30,0), nullable=False)
    dst_fee_usd            = Column(Float,         nullable=True)
    dst_timestamp          = Column(BigInteger,    nullable=False)

    def __init__(
        self,
        src_blockchain,
        user_transaction_hash,
        user_from_address,
        user_to_address,
        user_fee,
        user_timestamp,
        bus_transaction_hash,
        bus_from_address,
        bus_to_address,
        bus_ticket_id,
        bus_fare,
        bus_fee,
        bus_timestamp,
        passenger,
        bus_guid,
        dst_blockchain,
        executor_fee,
        dvn_fee,
        src_contract_address,
        dst_contract_address,
        amount_sent_ld,
        amount_received_ld,
        dst_transaction_hash,
        dst_from_address,
        dst_to_address,
        dst_fee,
        dst_timestamp,
    ):
        self.src_blockchain = src_blockchain
        self.user_transaction_hash = user_transaction_hash
        self.user_from_address = user_from_address
        self.user_to_address = user_to_address
        self.user_fee = user_fee
        self.user_timestamp = user_timestamp
        self.bus_transaction_hash = bus_transaction_hash
        self.bus_from_address = bus_from_address
        self.bus_to_address = bus_to_address
        self.bus_fee = bus_fee
        self.bus_timestamp = bus_timestamp
        self.bus_ticket_id = bus_ticket_id
        self.bus_fare = bus_fare
        self.passenger = passenger
        self.bus_guid = bus_guid
        self.dst_blockchain = dst_blockchain
        self.executor_fee = executor_fee
        self.dvn_fee = dvn_fee
        self.src_contract_address = src_contract_address
        self.dst_contract_address = dst_contract_address
        self.amount_sent_ld = amount_sent_ld
        self.amount_received_ld = amount_received_ld
        self.dst_transaction_hash = dst_transaction_hash
        self.dst_from_address = dst_from_address
        self.dst_to_address = dst_to_address
        self.dst_fee = dst_fee
        self.dst_timestamp = dst_timestamp

    def __repr__(self):
        return f"<StargateBusCrossChainTransaction(src_blockchain={self.src_blockchain}, user_transaction_hash={self.user_transaction_hash}, user_from_address={self.user_from_address}, user_to_address={self.user_to_address}, user_fee={self.user_fee}, user_timestamp={self.user_timestamp}, bus_transaction_hash={self.bus_transaction_hash}, bus_from_address={self.bus_from_address}, bus_to_address={self.bus_to_address}, bus_fee={self.bus_fee}, bus_timestamp={self.bus_timestamp}, bus_ticket_id={self.bus_ticket_id}, bus_fare={self.bus_fare}, passenger={self.passenger}, bus_guid={self.bus_guid}, dst_blockchain={self.dst_blockchain}, executor_fee={self.executor_fee}, dvn_fee={self.dvn_fee}, src_contract_address={self.src_contract_address}, dst_contract_address={self.dst_contract_address}, amount_sent_ld={self.amount_sent_ld}, amount_received_ld={self.amount_received_ld}, dst_transaction_hash={self.dst_transaction_hash}, dst_from_address={self.dst_from_address}, dst_to_address={self.dst_to_address}, dst_fee={self.dst_fee}, dst_timestamp={self.dst_timestamp})>"


class StargateCrossChainSwap(Base):
    __tablename__ = "stargate_cross_chain_swaps"

    id                  = Column(Integer,       nullable=False, autoincrement=True, primary_key=True)
    src_blockchain      = Column(String(10),    nullable=False)
    src_transaction_hash= Column(String(66),    nullable=False)
    src_from_address    = Column(String(42),    nullable=False)
    src_to_address      = Column(String(42),    nullable=False)
    src_fee             = Column(Numeric(30,0), nullable=False)
    src_fee_usd         = Column(Float,         nullable=True)
    src_timestamp       = Column(BigInteger,    nullable=False)
    dst_blockchain      = Column(String(10),    nullable=False)
    dst_transaction_hash= Column(String(66),    nullable=False)
    dst_from_address    = Column(String(42),    nullable=False)
    dst_to_address      = Column(String(42),    nullable=False)
    dst_fee             = Column(Numeric(30,0), nullable=False)
    dst_fee_usd         = Column(Float,         nullable=True)
    dst_timestamp       = Column(BigInteger,    nullable=False)
    verifier_fee        = Column(Numeric(30,0), nullable=False)
    verifier_fee_usd    = Column(Float,         nullable=True)
    relayer_fee         = Column(Numeric(30,0), nullable=False)
    relayer_fee_usd     = Column(Float,         nullable=True)
    src_contract_address= Column(String(42),    nullable=False)
    dst_contract_address= Column(String(42),    nullable=False)
    dst_pool_id         = Column(Integer,       nullable=False)
    depositor           = Column(String(42),    nullable=False)
    recipient           = Column(String(42),    nullable=False)
    amount_sd           = Column(Numeric(30,0), nullable=False)
    protocol_fee        = Column(Numeric(30,0), nullable=False)
    protocol_fee_usd    = Column(Float,         nullable=True)
    eq_fee              = Column(Numeric(30,0), nullable=False)
    eq_fee_usd          = Column(Float,         nullable=True)
    eq_reward           = Column(Numeric(30,0), nullable=False)
    lp_fee              = Column(Numeric(30,0), nullable=False)
    lp_fee_usd          = Column(Float,         nullable=True)
    amount_usd          = Column(Float,         nullable=True)

    def __init__(
        self,
        src_blockchain,
        src_transaction_hash,
        src_from_address,
        src_to_address,
        src_fee,
        src_timestamp,
        src_contract_address,
        amount_sd,
        eq_reward,
        eq_fee,
        protocol_fee,
        lp_fee,
        verifier_fee,
        relayer_fee,
        dst_blockchain,
        dst_transaction_hash,
        dst_from_address,
        dst_to_address,
        dst_fee,
        dst_timestamp,
        dst_contract_address,
        dst_pool_id,
        depositor,
        recipient,
    ):
        self.src_blockchain = src_blockchain
        self.src_transaction_hash = src_transaction_hash
        self.src_from_address = src_from_address
        self.src_to_address = src_to_address
        self.src_fee = src_fee
        self.src_timestamp = src_timestamp
        self.src_contract_address = src_contract_address
        self.amount_sd = amount_sd
        self.eq_reward = eq_reward
        self.eq_fee = eq_fee
        self.protocol_fee = protocol_fee
        self.lp_fee = lp_fee
        self.verifier_fee = verifier_fee
        self.relayer_fee = relayer_fee
        self.dst_blockchain = dst_blockchain
        self.dst_transaction_hash = dst_transaction_hash
        self.dst_from_address = dst_from_address
        self.dst_to_address = dst_to_address
        self.dst_fee = dst_fee
        self.dst_timestamp = dst_timestamp
        self.dst_contract_address = dst_contract_address
        self.dst_pool_id = dst_pool_id
        self.depositor = depositor
        self.recipient = recipient

    def __repr__(self):
        return f"<StargateCrossChainSwap(src_blockchain={self.src_blockchain}, src_transaction_hash={self.src_transaction_hash}, src_from_address={self.src_from_address}, src_to_address={self.src_to_address}, src_fee={self.src_fee}, src_timestamp={self.src_timestamp}, src_contract_address={self.src_contract_address}, amount_sd={self.amount_sd}, eq_reward={self.eq_reward}, eq_fee={self.eq_fee}, protocol_fee={self.protocol_fee}, lp_fee={self.lp_fee}, verifier_fee={self.verifier_fee}, relayer_fee={self.relayer_fee}, dst_blockchain={self.dst_blockchain}, dst_transaction_hash={self.dst_transaction_hash}, dst_from_address={self.dst_from_address}, dst_to_address={self.dst_to_address}, dst_fee={self.dst_fee}, dst_timestamp={self.dst_timestamp}, dst_contract_address={self.dst_contract_address}, dst_pool_id={self.dst_pool_id}, depositor={self.depositor}, recipient={self.recipient})>"


class StargateOFTCrossChainTransaction(Base):
    __tablename__ = "stargate_oft_cross_chain_transactions"

    id                  = Column(Integer,       nullable=False, autoincrement=True, primary_key=True)
    src_blockchain      = Column(String(10),    nullable=False)
    src_transaction_hash= Column(String(66),    nullable=False)
    src_from_address    = Column(String(42),    nullable=False)
    src_to_address      = Column(String(42),    nullable=False)
    src_fee             = Column(Numeric(30,0), nullable=False)
    src_fee_usd         = Column(Float,         nullable=True)
    src_timestamp       = Column(BigInteger,    nullable=False)
    executor_fee        = Column(Numeric(30,0), nullable=False)
    executor_fee_usd    = Column(Float,         nullable=True)
    dvn_fee             = Column(Numeric(30,0), nullable=False)
    dvn_fee_usd         = Column(Float,         nullable=True)
    dst_blockchain      = Column(String(10),    nullable=False)
    dst_transaction_hash= Column(String(66),    nullable=False)
    dst_from_address    = Column(String(42),    nullable=False)
    dst_to_address      = Column(String(42),    nullable=False)
    dst_fee             = Column(Numeric(30,0), nullable=False)
    dst_fee_usd         = Column(Float,         nullable=True)
    dst_timestamp       = Column(BigInteger,    nullable=False)
    src_contract_address= Column(String(42),    nullable=False)
    dst_contract_address= Column(String(42),    nullable=False)
    depositor           = Column(String(42),    nullable=False)
    recipient           = Column(String(42),    nullable=False)
    amount              = Column(Numeric(30,0), nullable=False)
    amount_usd          = Column(Float,         nullable=True)

    def __init__(
        self,
        src_blockchain,
        src_transaction_hash,
        src_from_address,
        src_to_address,
        src_fee,
        src_timestamp,
        executor_fee,
        dvn_fee,
        dst_blockchain,
        dst_transaction_hash,
        dst_from_address,
        dst_to_address,
        dst_fee,
        dst_timestamp,
        src_contract_address,
        dst_contract_address,
        depositor,
        recipient,
        amount,
    ):
        self.src_blockchain = src_blockchain
        self.src_transaction_hash = src_transaction_hash
        self.src_from_address = src_from_address
        self.src_to_address = src_to_address
        self.src_fee = src_fee
        self.src_timestamp = src_timestamp
        self.executor_fee = executor_fee
        self.dvn_fee = dvn_fee
        self.dst_blockchain = dst_blockchain
        self.dst_transaction_hash = dst_transaction_hash
        self.dst_from_address = dst_from_address
        self.dst_to_address = dst_to_address
        self.dst_fee = dst_fee
        self.dst_timestamp = dst_timestamp
        self.src_contract_address = src_contract_address,
        self.dst_contract_address = dst_contract_address,
        self.depositor = depositor
        self.recipient = recipient
        self.amount = amount

    def __repr__(self):
        return f"<StargateOFTCrossChainTransaction(src_blockchain={self.src_blockchain}, src_transaction_hash={self.src_transaction_hash}, src_from_address={self.src_from_address}, src_to_address={self.src_to_address}, src_fee={self.src_fee}, src_timestamp={self.src_timestamp}, executor_fee={self.executor_fee}, dvn_fee={self.dvn_fee}, dst_blockchain={self.dst_blockchain}, dst_transaction_hash={self.dst_transaction_hash}, dst_from_address={self.dst_from_address}, dst_to_address={self.dst_to_address}, dst_fee={self.dst_fee}, dst_timestamp={self.dst_timestamp}, src_contract_address={self.src_contract_address}, dst_contract_address={self.dst_contract_address}, depositor={self.depositor}, recipient={self.recipient}, amount={self.amount})>"


class StargateCrossChainTokenTransfers(Base):
    __tablename__ = "stargate_cross_chain_token_transfers"

    id                  = Column(Integer,       nullable=False, autoincrement=True, primary_key=True)
    src_blockchain      = Column(String(10),    nullable=False)
    src_transaction_hash= Column(String(66),    nullable=False)
    src_from_address    = Column(String(42),    nullable=False)
    src_to_address      = Column(String(42),    nullable=False)
    src_fee             = Column(Numeric(30,0), nullable=False)
    src_fee_usd         = Column(Float,         nullable=True)
    src_timestamp       = Column(BigInteger,    nullable=False)
    verifier_fee        = Column(Numeric(30,0), nullable=False)
    verifier_fee_usd    = Column(Float,         nullable=True)
    relayer_fee         = Column(Numeric(30,0), nullable=False)
    relayer_fee_usd     = Column(Float,         nullable=True)
    dst_blockchain      = Column(String(10),    nullable=False)
    dst_transaction_hash= Column(String(66),    nullable=False)
    dst_from_address    = Column(String(42),    nullable=False)
    dst_to_address      = Column(String(42),    nullable=False)
    dst_fee             = Column(Numeric(30,0), nullable=False)
    dst_fee_usd         = Column(Float,         nullable=True)
    dst_timestamp       = Column(BigInteger,    nullable=False)
    src_contract_address= Column(String(42),    nullable=False)
    dst_contract_address= Column(String(42),    nullable=False)
    depositor           = Column(String(42),    nullable=True)
    recipient           = Column(String(42),    nullable=False)
    amount              = Column(Numeric(30,0), nullable=False)
    amount_usd          = Column(Float,         nullable=True)

    def __init__(
        self,
        src_blockchain,
        src_transaction_hash,
        src_from_address,
        src_to_address,
        src_fee,
        src_timestamp,
        verifier_fee,
        relayer_fee,
        dst_blockchain,
        dst_transaction_hash,
        dst_from_address,
        dst_to_address,
        dst_fee,
        dst_timestamp,
        src_contract_address,
        dst_contract_address,
        depositor,
        recipient,
        amount,
    ):
        self.src_blockchain = src_blockchain
        self.src_transaction_hash = src_transaction_hash
        self.src_from_address = src_from_address
        self.src_to_address = src_to_address
        self.src_fee = src_fee
        self.src_timestamp = src_timestamp
        self.verifier_fee = verifier_fee
        self.relayer_fee = relayer_fee
        self.dst_blockchain = dst_blockchain
        self.dst_transaction_hash = dst_transaction_hash
        self.dst_from_address = dst_from_address
        self.dst_to_address = dst_to_address
        self.dst_fee = dst_fee
        self.dst_timestamp = dst_timestamp
        self.src_contract_address = src_contract_address
        self.dst_contract_address = dst_contract_address
        self.depositor = depositor
        self.recipient = recipient
        self.amount = amount

    def __repr__(self):
        return f"<StargateCrossChainTokenTransfers(src_blockchain={self.src_blockchain}, src_transaction_hash={self.src_transaction_hash}, src_from_address={self.src_from_address}, src_to_address={self.src_to_address}, src_fee={self.src_fee}, src_timestamp={self.src_timestamp}, verifier_fee={self.verifier_fee}, relayer_fee={self.relayer_fee}, dst_blockchain={self.dst_blockchain}, dst_transaction_hash={self.dst_transaction_hash}, dst_from_address={self.dst_from_address}, dst_to_address={self.dst_to_address}, dst_fee={self.dst_fee}, dst_timestamp={self.dst_timestamp}, src_contract_address={self.src_contract_address}, dst_contract_address={self.dst_contract_address}, depositor={self.depositor}, recipient={self.recipient}, amount={self.amount})>"
