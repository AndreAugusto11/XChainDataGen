from sqlalchemy import BigInteger, Column, Date, Float, Integer, Numeric, String

from repository.database import Base


class TokenPrice(Base):
    __tablename__ = "token_price"

    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    symbol = Column(String(50), nullable=False)
    name = Column(String(50), nullable=False)
    date = Column(Date, nullable=True)
    price_usd = Column(Float, nullable=False)

    def __init__(self, symbol, name, date, price_usd):
        self.symbol = symbol
        self.name = name
        self.date = date
        self.price_usd = price_usd

    def __repr__(self):
        return f"<TokenPrice(symbol={self.symbol}, date={self.date}, price_usd={self.price_usd})>"


class TokenMetadata(Base):
    __tablename__ = "token_metadata"

    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    symbol = Column(String(50), nullable=False)
    name = Column(String(50), nullable=False)
    decimals = Column(Integer, nullable=False)
    blockchain = Column(String(10), nullable=False)
    address = Column(String(44), nullable=True)

    def __init__(self, symbol, name, decimals, blockchain, address):
        self.symbol = symbol
        self.name = name
        self.decimals = decimals
        self.blockchain = blockchain
        self.address = address

    def __repr__(self):
        return (
            f"<Token(symbol={self.symbol}, "
            f"name={self.name}, "
            f"decimals={self.decimals}, "
            f"blockchain={self.blockchain}, "
            f"address={self.address})>"
        )


class NativeToken(Base):
    __tablename__ = "native_token"

    blockchain = Column(String(10), nullable=False, primary_key=True)
    symbol = Column(String(50), nullable=False)

    def __init__(self, symbol, blockchain):
        self.symbol = symbol
        self.blockchain = blockchain

    def __repr__(self):
        return f"<Token(symbol={self.symbol}, blockchain={self.blockchain})>"


class BlockchainTransaction(Base):
    __abstract__ = True

    blockchain = Column(String(10), nullable=False)
    transaction_hash = Column(String(88), nullable=False, primary_key=True)
    block_number = Column(Integer, nullable=False)
    timestamp = Column(BigInteger, nullable=False)
    from_address = Column(String(44), nullable=True)
    to_address = Column(String(44), nullable=True)
    status = Column(Integer, nullable=False)
    value = Column(Numeric(30, 0), nullable=True)
    input_data = Column(String(35000), nullable=True)
    fee = Column(Numeric(30, 0), nullable=False)

    def __init__(
        self,
        blockchain,
        transaction_hash,
        block_number,
        timestamp,
        from_address,
        to_address,
        status,
        value,
        input_data,
        fee,
    ):
        self.blockchain = blockchain
        self.transaction_hash = transaction_hash
        self.block_number = block_number
        self.timestamp = timestamp
        self.from_address = from_address
        self.to_address = to_address
        self.status = status
        self.value = value
        self.input_data = input_data
        self.fee = fee
