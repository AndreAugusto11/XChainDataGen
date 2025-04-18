from abc import ABC, abstractmethod

from sqlalchemy.orm import scoped_session, sessionmaker

from generator.common.price_generator import PriceGenerator
from repository.database import engine


class BaseGenerator(ABC):

    def __init__(self) -> None:
        self.bind_db_to_repos()
        self.price_generator = PriceGenerator()

    @abstractmethod
    def bind_db_to_repos(self) -> None:
        pass

    @abstractmethod
    def generate_cross_chain_data(self) -> None:
        pass
