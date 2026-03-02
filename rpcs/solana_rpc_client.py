import requests

from config.constants import (
    RPCS_CONFIG_FILE,
)
from rpcs.rpc_client import RPCClient
from utils.utils import (
    CliColor,
    CustomException,
    build_log_message_solana,
    load_solana_decoder_url,
    log_to_cli,
)


class SolanaRPCClient(RPCClient):
    CLASS_NAME = "SolanaRPCClient"

    def __init__(self, bridge, config_file: str = RPCS_CONFIG_FILE):
        super().__init__(bridge, config_file)
        self.SOLANA_DECODER_URL = load_solana_decoder_url()

    def get_all_signatures_for_address(
        self,
        account_address: str,
        start_signature: str,
        end_signature: str,
    ) -> list:
        all_signatures = []
        before = end_signature  # start from the newest tx
        stop_at = start_signature  # oldest signature to stop at
        seen = set()  # remove duplicates caused by RPC instability

        while True:
            params = [account_address, {"before": before, "limit": 1000}]
            fetched = self.req_get_signatures_for_address(params)

            if not fetched:
                # No more results from RPC
                break

            for tx in fetched:
                sig = tx["signature"]

                # Stop condition: reached or passed our lower bound
                if sig == stop_at:
                    return all_signatures

                if sig in seen:
                    continue  # deduplicate across unstable RPC responses
                seen.add(sig)

                all_signatures.append(tx)

            log_to_cli(
                build_log_message_solana(
                    start_signature,
                    end_signature,
                    self.bridge,
                    f"Fetched {len(all_signatures)} signatures for {account_address}...",
                ),
                CliColor.INFO,
            )

            # Pagination:
            # Move "before" to the OLDEST signature returned in this batch
            before = fetched[-1]["signature"]

            # Safety stop: If the API starts returning the same pages repeatedly
            if len(fetched) < 1000:
                break  # Reached end of available history

        log_to_cli(
            build_log_message_solana(
                start_signature,
                end_signature,
                self.bridge,
                (
                    f"Retrieved all signatures for {account_address}..."
                    f"({len(all_signatures)} signatures fetched)",
                ),
            ),
            CliColor.SUCCESS,
        )

        return all_signatures

    def req_get_signatures_for_address(
        self,
        params: list,
    ) -> list:
        method = "getSignaturesForAddress"

        rpc = self.get_next_rpc("solana")
        response = self.make_request(rpc, "solana", method, params)

        return response["result"] if response else []

    def process_transaction(self, blockchain: str, tx_signature: str) -> dict:
        import concurrent.futures

        rpc = self.get_next_rpc(blockchain)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_receipt = executor.submit(self.parseTransactionByHash, rpc, tx_signature)

            response_receipt = future_receipt.result()

        return response_receipt["result"] if response_receipt else {}

    def parseTransactionByHash(self, tx_signature: str) -> dict:
        func_name = "parseTransactionByHash"

        rpc = self.get_next_rpc("solana")

        response = requests.post(
            f"{self.SOLANA_DECODER_URL}/parseTransactionByHash",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            json={"rpcUrl": rpc, "signature": tx_signature},
        )

        if response.status_code != 200:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"RPC request failed with status code {response.status_code}",
            )

        return response.json()
