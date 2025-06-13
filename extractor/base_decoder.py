from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseDecoder(ABC):
    @abstractmethod
    def decode_event(
        self,
        log: Dict[str, Any],
    ) -> None:
        pass
