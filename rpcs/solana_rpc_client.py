import requests

from config.constants import (
    RPCS_CONFIG_FILE,
)
from rpcs.rpc_client import RPCClient
from utils.utils import CustomException, load_solana_decoder_url


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
        lastSignature = end_signature  # the endpoint works by fetching in reverse order

        while True:
            fetchedTransactions = self.req_get_signatures_for_address(
                [
                    account_address,
                    {"before": lastSignature, "until": start_signature, "limit": 1000},
                ]
            )
            all_signatures.extend(fetchedTransactions)

            lastSignature = fetchedTransactions[len(fetchedTransactions) - 1]["signature"]

            if len(fetchedTransactions) != 1000:
                break

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
