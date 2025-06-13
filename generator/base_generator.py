from abc import ABC, abstractmethod

from generator.common.price_generator import PriceGenerator


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
