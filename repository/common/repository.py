from datetime import datetime

from sqlalchemy import Index, func
from sqlalchemy.orm import Session

from repository.base import BaseRepository

from .models import *


class TokenPriceRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(TokenPrice, session_factory)

    def get_token_price_by_symbol_and_date(self, symbol: str, date: str):
        with self.get_session() as session:
            return session.query(TokenPrice).filter(TokenPrice.symbol == symbol, TokenPrice.date == date).first()
    
    def exists_price_for_symbol(self, symbol: str):
        with self.get_session() as session:
            return session.query(func.count(TokenPrice.id)).filter(TokenPrice.symbol == symbol).scalar()

    def get_min_date_for_symbol_and_name(self, symbol: str, name: str):
        with self.get_session() as session:
            return session.query(func.min(TokenPrice.date)).filter(TokenPrice.symbol == symbol, TokenPrice.name == name).scalar()
    
    def get_max_date_for_symbol_and_name(self, symbol: str, name: str):
        with self.get_session() as session:
            return session.query(func.max(TokenPrice.date)).filter(TokenPrice.symbol == symbol, TokenPrice.name == name).scalar()

    def get_count_datapoints_for_symbol_and_name_between_dates(self, symbol: str, name: str, start_ts: str, end_ts: str):
        start_day = datetime.fromtimestamp(int(start_ts)).date()
        end_day = datetime.fromtimestamp(int(end_ts)).date()
        
        with self.get_session() as session:
            return session.query(func.count(TokenPrice.id)).filter(TokenPrice.symbol == symbol, TokenPrice.name == name, TokenPrice.date >= start_day, TokenPrice.date <= end_day).scalar()

class TokenMetadataRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(TokenMetadata, session_factory)

    def get_token_metadata_by_contract_and_blockchain(self, contract_address: str, blockchain: str):
        with self.get_session() as session:
            return session.query(TokenMetadata).filter(TokenMetadata.address == contract_address, TokenMetadata.blockchain == blockchain).first()

    def get_token_metadata_by_symbol(self, symbol: str):
        with self.get_session() as session:
            return session.query(TokenMetadata).filter(TokenMetadata.symbol == symbol).first()

class NativeTokenRepository(BaseRepository):

    def __init__(self, session_factory):
        super().__init__(NativeToken, session_factory)

    def get_native_token_by_blockchain(self, blockchain: str):
        with self.get_session() as session:
            return session.query(NativeToken).filter(NativeToken.blockchain == blockchain).first()


Index("ix_token_price_symbol", TokenPrice.symbol)
Index("ix_token_price_symbol_date", TokenPrice.symbol, TokenPrice.date)
Index("ix_token_metadata_symbol", TokenMetadata.symbol)
Index("ix_token_metadata_blockchain_address", TokenMetadata.address, TokenMetadata.blockchain)

Index("ix_native_token_blockchain", NativeToken.symbol, NativeToken.blockchain)