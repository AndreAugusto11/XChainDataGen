import threading
import time
from queue import Queue
from urllib.request import BaseHandler

from config.constants import Bridge
from extractor.decoder import BridgeDecoder
from utils.rpc_utils import RPCClient
from utils.utils import (
    CliColor,
    CustomException,
    build_log_message,
    load_module,
    log_error,
    log_to_cli,
)


class Extractor:
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

        divide_block_ranges(start_block: int, end_block: int, chunk_size: int = 1000):
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

        self.rpc_client = RPCClient(bridge)

        # fetch a random rpc to initialize the decoder for the bridge
        self.decoder = BridgeDecoder(bridge, self.rpc_client.get_random_rpc(blockchain))

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
    def divide_block_ranges(start_block: int, end_block: int, chunk_size: int = 1000):
        """Divide block range into smaller chunks."""
        ranges = []
        for block in range(start_block, end_block + 1, chunk_size):
            ranges.append((block, min(block + chunk_size - 1, end_block)))
        return ranges

    def work(
        self,
        contract: str,
        topics: list,
        start_block: int,
        end_block: int,
    ):
        log_to_cli(
            build_log_message(
                start_block,
                end_block,
                contract,
                self.bridge,
                self.blockchain,
                "Processing logs and transactions...",
            )
        )

        logs = self.rpc_client.get_logs_emitted_by_contract(
            self.blockchain, contract, topics, start_block, end_block
        )

        if len(logs) == 0:
            return

        decoded_logs = []
        txs = {}

        for log in logs:
            decoded_log = self.decoder.decode(contract, self.blockchain, log)

            # we take the decoded log and append more data to it, such that the handler can insert
            #  in the right DB table
            decoded_log["transaction_hash"] = log["transactionHash"]
            decoded_log["block_number"] = log["blockNumber"]
            decoded_log["contract_address"] = contract
            decoded_log["topic"] = log["topics"][0]
            decoded_logs.append(decoded_log)

        included_logs = self.handler.handle_events(
            self.blockchain, start_block, end_block, contract, topics, decoded_logs
        )

        for log in included_logs:
            tx_hash = log["transaction_hash"]

            # to avoid processing the same transaction multiple times we ignore if already in the
            #  repository
            try:
                if self.handler.does_transaction_exist_by_hash(tx_hash):
                    continue

                tx_receipt, block = self.rpc_client.process_transaction(
                    self.blockchain, log["transaction_hash"], log["block_number"]
                )

                if tx_receipt is None or block is None:
                    raise Exception(tx_hash)

                txs[tx_hash] = self.handler.create_transaction_object(
                    self.blockchain, tx_receipt, block
                )

            except CustomException as e:
                request_desc = (
                    f"Error processing request: {self.blockchain}, {start_block}, {end_block}, "
                    f"{contract}, {topics}. Error: {e}"
                )
                log_error(self.bridge, request_desc)

        if len(txs) > 0:
            self.handler.handle_transactions(txs.values())

    def worker(self):
        """Worker function for threads to process block ranges."""
        while not self.task_queue.empty():
            try:
                contract, topics, start_block, end_block = self.task_queue.get()

                self.work(
                    contract,
                    topics,
                    start_block,
                    end_block,
                )
            except CustomException as e:
                request_desc = (
                    f"Error processing request: {self.bridge}, {self.blockchain}, {start_block}, "
                    f"{end_block}, {contract}, {topics}. Error: {e}"
                )
                log_error(self.bridge, request_desc)
            finally:
                self.task_queue.task_done()

    def extract_data(self, start_block: int, end_block: int):
        """Main extraction logic."""

        # load the bridge contract addresses and topics from the configuration file
        bridge_blockchain_pairs = self.handler.get_bridge_contracts_and_topics(
            self.bridge, self.blockchain
        )

        for pair in bridge_blockchain_pairs:
            for contract in pair["contracts"]:
                start_time = time.time()
                topics = pair["topics"]

                num_threads = self.rpc_client.max_threads_per_blockchain(self.blockchain) * 2

                chunk_size = min((end_block - start_block) // num_threads, 1000)

                if chunk_size < 1:
                    block_ranges = self.divide_block_ranges(start_block, end_block)
                else:
                    # Divide block ranges into smaller chunks
                    block_ranges = self.divide_block_ranges(start_block, end_block, chunk_size)

                # Populate the task queue
                for start, end in block_ranges:
                    self.task_queue.put((contract, topics, start, end))

                # Create and start threads
                log_to_cli(
                    build_log_message(
                        start_block,
                        end_block,
                        contract,
                        self.bridge,
                        self.blockchain,
                        (
                            f"Launching {num_threads} threads to process {len(block_ranges)} block "
                            f"ranges...",
                        ),
                    )
                )
                for i in range(num_threads):
                    thread = threading.Thread(target=self.worker, name=f"thread_id_{i}")
                    thread.start()
                    self.threads.append(thread)

                # Wait for all threads to complete
                self.task_queue.join()
                for thread in self.threads:
                    thread.join()

                end_time = time.time()

                log_to_cli(
                    build_log_message(
                        start_block,
                        end_block,
                        contract,
                        self.bridge,
                        self.blockchain,
                        (
                            f"Finished processing logs and transactions. Time taken: "
                            f"{end_time - start_time} seconds.",
                        ),
                    ),
                    CliColor.SUCCESS,
                )
