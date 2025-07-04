import threading
import time

from config.constants import Bridge
from extractor.decoder import BridgeDecoder
from extractor.extractor import Extractor
from rpcs.evm_rpc_client import EvmRPCClient
from utils.utils import (
    CliColor,
    CustomException,
    build_log_message,
    log_error,
    log_to_cli,
)


class EvmExtractor(Extractor):
    CLASS_NAME = "EvmExtractor"

    def __init__(self, bridge: Bridge, blockchain: str, blockchains: list):
        self.rpc_client = EvmRPCClient(bridge)
        # fetch a random rpc to initialize the decoder for the bridge
        self.decoder = BridgeDecoder(bridge, self.rpc_client.get_random_rpc(blockchain))

        super().__init__(bridge, blockchain, blockchains)

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

                tx, block = self.rpc_client.process_transaction(
                    self.blockchain, log["transaction_hash"], log["block_number"]
                )

                if tx is None or block is None:
                    raise Exception(tx_hash)

                txs[tx_hash] = self.handler.create_transaction_object(
                    self.blockchain, tx, block["timestamp"]
                )

            except CustomException as e:
                request_desc = (
                    f"Error processing request: {self.blockchain}, {start_block}, {end_block}, "
                    f"{contract}, {topics}. Error: {e}"
                )
                log_error(self.bridge, request_desc)

        if len(txs) > 0:
            try:
                self.handler.handle_transactions(txs.values())
            except CustomException:
                # if there is an error while handling transactions in batch, we handle them one
                # by one to avoid the entire batch failing
                for tx in txs.values():
                    try:
                        self.handler.handle_transaction(tx)
                    except CustomException as e:
                        request_desc = (
                            f"Error processing transaction: {self.blockchain}, "
                            f"{tx['transaction_hash']}. Error: {e}"
                        )
                        log_error(self.bridge, request_desc)

    def extract_data(self, start_block: int, end_block: int):
        """Main extraction logic."""

        # load the bridge contract addresses and topics from the configuration file
        bridge_blockchain_pairs = self.handler.get_bridge_contracts_and_topics(
            self.bridge, self.blockchain
        )

        for pair in bridge_blockchain_pairs:
            for contract in pair["contracts"]:
                threads = []

                start_time = time.time()
                topics = pair["topics"]

                num_threads = self.rpc_client.max_threads_per_blockchain(self.blockchain) * 2

                chunk_size = max(
                    1, min((end_block - start_block + num_threads - 1) // num_threads, 1000)
                )

                block_ranges = self.divide_range(start_block, end_block - 1, chunk_size)

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
                    threads.append(thread)

                # Wait for all threads to complete
                self.task_queue.join()
                for thread in threads:
                    thread.join()

                threads.clear()

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
