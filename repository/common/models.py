from sqlalchemy import Column, Date, Float, Integer, String

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
    address = Column(String(42), nullable=True)

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
