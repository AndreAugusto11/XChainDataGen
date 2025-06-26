from abc import ABC, abstractmethod
from queue import Queue
from urllib.request import BaseHandler

from config.constants import Bridge
from utils.utils import (
    CustomException,
    load_module,
)


class Extractor(ABC):
    """
    Extractor is a class responsible for orchestrating the extraction of blockchain logs and
    transactions for a specified bridge and blockchain. It manages the division of block ranges,
    multi-threaded processing, dynamic handler loading, and the decoding and handling of logs
    and transactions.

    Attributes:
        CLASS_NAME (str): The name of the class.
        task_queue (Queue): Queue to manage block range tasks for worker threads.
        threads (list): List of active worker threads.
        blockchain (str): The blockchain network to extract data from.
        bridge (Bridge): The bridge instance specifying the protocol/bridge.
        rpc_client (RPCClient): Client for interacting with blockchain RPC endpoints.
        decoder (BridgeDecoder): Decoder for parsing logs specific to the bridge.
        handler (BaseHandler): Handler for processing and storing extracted data.

    Methods:
        __init__(self, bridge: Bridge, blockchain: str):
            Initializes the Extractor with the specified bridge and blockchain, sets up the RPC
            client, decoder, and handler.

        load_handler(self) -> BaseHandler:
            Dynamically loads and returns the handler for the specified bridge.

        divide_range(start_block: int, end_block: int, chunk_size: int = 1000):
            Divides a block range into smaller chunks for parallel processing.

        work(self, contract: str, topics: list, start_block: int, end_block: int):
            Processes logs and transactions for a given contract and block range, decodes logs, and
            invokes the bridge handler.

        worker(self):
            Worker function for threads to process block ranges from the task queue.

        extract_data(self, start_block: int, end_block: int, blockchains: list):
            Main extraction logic that validates contracts, divides block ranges, launches worker
            threads, and coordinates the extraction process.
    """

    CLASS_NAME = "Extractor"

    def __init__(self, bridge: Bridge, blockchain: str, blockchains: list):
        self.task_queue = Queue()
        self.threads = []
        self.blockchain = blockchain
        self.bridge = bridge

        # load the bridge handler and initiate a DB session
        self.handler = self.load_handler(blockchains)

    def load_handler(self, blockchains: list) -> BaseHandler:
        """Dynamically loads the handler for the specified bridge."""
        func_name = "load_handler"
        bridge_name = self.bridge.value

        try:
            module = load_module(f"extractor.{bridge_name}.handler")
            handler_class_name = f"{bridge_name.capitalize()}Handler"
            handler_class = getattr(module, handler_class_name)

            return handler_class(self.rpc_client, blockchains)
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME, func_name, f"Bridge {bridge_name} not supported. {e}"
            ) from e

    @staticmethod
    def divide_range(start_index: int, end_index: int, chunk_size: int = 1000):
        """Divide an index range into chunks of at most `chunk_size`."""
        ranges = []
        for i in range(start_index, end_index + 1, chunk_size):
            ranges.append((i, min(i + chunk_size, end_index + 1)))
        return ranges

    @abstractmethod
    def worker(self):
        pass

    @abstractmethod
    def work(self, start_block: int, end_block: int):
        """Logic for each launched thread."""
        pass

    @abstractmethod
    def extract_data(self, start_block: int, end_block: int):
        """Main extraction logic."""
        pass
