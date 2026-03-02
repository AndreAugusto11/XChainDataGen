# import json
import threading
import time

from config.constants import Bridge
from extractor.extractor import Extractor
from rpcs.solana_rpc_client import SolanaRPCClient
from utils.utils import (
    CliColor,
    CustomException,
    build_log_message_solana,
    log_error,
    log_to_cli,
)


class SolanaExtractor(Extractor):
    CLASS_NAME = "SolanaExtractor"

    def __init__(self, bridge: Bridge, blockchain: str, blockchains: list):
        self.rpc_client = SolanaRPCClient(bridge)

        super().__init__(bridge, blockchain, blockchains)

        self.solana_program_ids = self.handler.get_solana_bridge_program_ids()

    def worker(self):
        """Worker function for threads to process block ranges."""
        while not self.task_queue.empty():
            try:
                program_id, signatures = self.task_queue.get()

                self.work(signatures)
            except CustomException as e:
                request_desc = (
                    f"Error processing request: {self.bridge}, {self.blockchain}, {program_id}, "
                    f"{signatures[0]}, {signatures[-1]}, {program_id}. Error: {e}"
                )
                log_error(self.bridge, request_desc)
            finally:
                self.task_queue.task_done()

    def work(
        self,
        signatures: list,
    ):
        start_signature = signatures[0]
        end_signature = signatures[-1]

        log_to_cli(
            build_log_message_solana(
                start_signature,
                end_signature,
                self.bridge,
                "Processing logs and transactions...",
            )
        )

        decoded_instructions = []
        for signature in signatures:
            try:
                exists = self.handler.does_transaction_exist_by_hash(signature)

                if exists:
                    continue

                decoded_tx = self.rpc_client.parseTransactionByHash(signature)

                decoded_instructions.append(decoded_tx)

            except CustomException as e:
                request_desc = (
                    f"Error processing transaction: {self.bridge}, {self.blockchain}, "
                    f"{signature}. Error: {e}"
                )
                log_error(self.bridge, request_desc)

        included_txs = self.handler.handle_solana_events(
            self.blockchain, start_signature, end_signature, decoded_instructions
        )

        transactions = []

        for decoded_tx in included_txs:
            if self.handler.does_transaction_exist_by_hash(
                decoded_tx["transaction"]["transaction"]["signatures"][0]
            ):
                continue

            transactions.append(
                self.handler.create_transaction_object(
                    self.blockchain,
                    decoded_tx["transaction"],
                    decoded_tx["transaction"]["blockTime"],
                )
            )

        if len(transactions) > 0:
            self.handler.handle_transactions(transactions)

    def extract_data(self, signature_ranges: dict):
        """Main extraction logic."""

        for idx, program_id in enumerate(self.solana_program_ids):
            start_signature = signature_ranges[program_id]["start_signature"]
            end_signature = signature_ranges[program_id]["end_signature"]

            log_to_cli(
                build_log_message_solana(
                    start_signature,
                    end_signature,
                    self.bridge,
                    (
                        f"Retrieving all signatures for program {program_id} ",
                        f"({idx + 1}/{len(self.solana_program_ids)}).",
                    ),
                )
            )

            # if we already have signatures fetched, we can skip fetching them again
            # and we can load them from a file

            all_signatures = self.rpc_client.get_all_signatures_for_address(
                program_id, start_signature, end_signature
            )

            all_signatures = list(map(lambda x: x["signature"], all_signatures))

            # store all signatures to a file for future reference
            with open(f"extractor/solana_{program_id}_signatures.txt", "w") as f:
                for signature in all_signatures:
                    f.write(f"{signature}\n")

            # if we want to load signatures from a file instead of fetching them again, we can
            # uncomment the following code

            # all_signatures = []
            # with open(f"extractor/solana_{program_id}_signatures.txt", "r") as f:
            #     # each line is a tx_hash / signature
            #     for line in f:
            #         tx_hash = line.strip()
            #         if tx_hash:
            #             all_signatures.append(tx_hash)

            # ensure no duplicates
            all_signatures = list(set(all_signatures))

            if not all_signatures:
                log_to_cli(
                    build_log_message_solana(
                        start_signature,
                        end_signature,
                        program_id,
                        self.blockchain,
                        "No transaction signatures found in the specified range.",
                    ),
                    CliColor.ERROR,
                )
                return None

            start_time = time.time()

            # num_threads = self.rpc_client.max_threads_per_blockchain(self.blockchain) * 2

            num_threads = 15

            # Ensure at least 1 per chunk, capped at 1000
            chunk_size = max(1, min((len(all_signatures) + num_threads - 1) // num_threads, 1000))

            block_ranges = self.divide_range(0, len(all_signatures) - 1, chunk_size)

            # Populate the task queue
            for start, end in block_ranges:
                self.task_queue.put((program_id, all_signatures[start:end]))

            log_to_cli(
                build_log_message_solana(
                    start_signature,
                    end_signature,
                    self.bridge,
                    (
                        f"Launching {num_threads} threads to process {len(block_ranges)} signature "
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
                build_log_message_solana(
                    start_signature,
                    end_signature,
                    self.bridge,
                    (
                        f"Finished processing logs and transactions. Time taken: "
                        f"{end_time - start_time} seconds.",
                    ),
                ),
                CliColor.SUCCESS,
            )
