import time

from sqlalchemy import text

from config.constants import Bridge
from generator.base_generator import BaseGenerator
from generator.common.price_generator import PriceGenerator
from repository.cctp.repository import (
    CCTPBlockchainTransactionRepository,
    CctpCrossChainTransactionsRepository,
    CCTPDepositForBurnRepository,
    CCTPMessageReceivedRepository,
)
from repository.common.repository import (
    NativeTokenRepository,
    TokenMetadataRepository,
    TokenPriceRepository,
)
from repository.database import DBSession
from utils.utils import (
    CliColor,
    CustomException,
    build_log_message_generator,
    log_error,
    log_to_cli,
)


class CctpGenerator(BaseGenerator):
    CLASS_NAME = "CctpGenerator"

    def __init__(self) -> None:
        super().__init__()
        self.bridge = Bridge.CCTP
        self.price_generator = PriceGenerator()

    def bind_db_to_repos(self):
        self.transactions_repo = CCTPBlockchainTransactionRepository(DBSession)
        self.cctp_deposit_for_burn_repo = CCTPDepositForBurnRepository(DBSession)
        self.cctp_message_received_repo = CCTPMessageReceivedRepository(DBSession)

        self.cctp_cross_chain_token_transfers_repo = CctpCrossChainTransactionsRepository(DBSession)

        self.token_metadata_repo = TokenMetadataRepository(DBSession)
        self.token_price_repo = TokenPriceRepository(DBSession)
        self.native_token_repo = NativeTokenRepository(DBSession)

    def generate_cross_chain_data(self):
        func_name = "create_cross_chain_transactions"

        try:
            self.match_token_transfers()

            start_ts = int(self.transactions_repo.get_min_timestamp()) - 86400
            end_ts = int(self.transactions_repo.get_max_timestamp()) + 86400

            # POPULATE TOKEN TABLES WITH NATIVE TOKEN INFO
            PriceGenerator.populate_native_tokens(
                self.bridge,
                self.native_token_repo,
                self.token_metadata_repo,
                self.token_price_repo,
                start_ts,
                end_ts,
            )

            cctxs = self.cctp_cross_chain_token_transfers_repo.get_unique_src_dst_contract_pairs()
            self.populate_token_info_tables(cctxs, start_ts, end_ts)

            PriceGenerator.calculate_cctx_usd_values(
                self.bridge,
                self.cctp_cross_chain_token_transfers_repo,
                "cctp_cross_chain_transactions",
                "amount",
                "src_blockchain",
                "src_contract_address",
                "src_timestamp",
                "amount_usd",
            )
            PriceGenerator.calculate_cctx_native_usd_values(
                self.bridge,
                self.cctp_cross_chain_token_transfers_repo,
                "cctp_cross_chain_transactions",
                "src_timestamp",
                "src_blockchain",
                "src_fee",
                "src_fee_usd",
            )
            PriceGenerator.calculate_cctx_native_usd_values(
                self.bridge,
                self.cctp_cross_chain_token_transfers_repo,
                "cctp_cross_chain_transactions",
                "dst_timestamp",
                "dst_blockchain",
                "dst_fee",
                "dst_fee_usd",
            )

        except Exception as e:
            exception = CustomException(
                self.CLASS_NAME,
                func_name,
                f"Error processing cross chain transactions. Error: {e}",
            )
            log_error(self.bridge, exception)

    def match_token_transfers(self):
        func_name = "match_token_transfers"

        start_time = time.time()
        log_to_cli(build_log_message_generator(self.bridge, "Matching token transfers..."))

        self.cctp_cross_chain_token_transfers_repo.empty_table()

        query = text(
            """
            INSERT INTO cctp_cross_chain_transactions (
                src_blockchain,
                src_transaction_hash,
                src_from_address,
                src_to_address,
                src_fee,
                src_fee_usd,
                src_timestamp,
                dst_blockchain,
                dst_transaction_hash,
                dst_from_address,
                dst_to_address,
                dst_fee,
                dst_fee_usd,
                dst_timestamp,
                deposit_id,
                depositor,
                recipient,
                src_contract_address,
                amount,
                amount_usd
            )
            SELECT
                src_tx.blockchain,
                src_tx.transaction_hash,
                src_tx.from_address,
                src_tx.to_address,
                src_tx.fee,
                NULL as src_fee_usd,
                src_tx.timestamp,
                dst_tx.blockchain,
                dst_tx.transaction_hash,
                dst_tx.from_address,
                dst_tx.to_address,
                dst_tx.fee,
                NULL as dst_fee_usd,
                dst_tx.timestamp,
                deposit.nonce,
                deposit.depositor,
                deposit.recipient,
                deposit.burn_token,
                deposit.amount,
                NULL as amount_usd
            FROM cctp_deposit_for_burn deposit
            JOIN cctp_blockchain_transactions src_tx ON src_tx.transaction_hash = deposit.transaction_hash
            JOIN cctp_message_received fill ON fill.nonce = deposit.nonce AND deposit.dst_blockchain = fill.blockchain AND fill.src_blockchain = deposit.blockchain
            JOIN cctp_blockchain_transactions dst_tx ON dst_tx.transaction_hash = fill.transaction_hash
            WHERE deposit.amount = fill.amount
            AND deposit.burn_token = fill.input_token
            AND deposit.depositor = fill.depositor
            AND deposit.recipient = fill.recipient
            AND deposit.burn_token = fill.input_token;
        """  # noqa: E501
        )

        try:
            self.cctp_cross_chain_token_transfers_repo.execute(query)

            size = self.cctp_cross_chain_token_transfers_repo.get_number_of_records()

            end_time = time.time()
            log_to_cli(
                build_log_message_generator(
                    self.bridge,
                    (
                        f"Token transfers matched in {end_time - start_time} seconds. "
                        f"Total records inserted: {size}",
                    ),
                ),
                CliColor.SUCCESS,
            )
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"Error processing token transfers. Error: {e}",
            ) from e

    def populate_token_info_tables(self, cctxs, start_ts, end_ts):
        start_time = time.time()
        log_to_cli(build_log_message_generator(self.bridge, "Fetching token prices..."))

        for cctx in cctxs:
            self.price_generator.populate_token_info(
                self.bridge,
                self.token_metadata_repo,
                self.token_price_repo,
                cctx.src_blockchain if "src_blockchain" not in cctx else None,
                None,
                cctx.src_contract_address if "src_contract_address" not in cctx else None,
                None,
                start_ts,
                end_ts,
            )

        end_time = time.time()
        log_to_cli(
            build_log_message_generator(
                self.bridge,
                f"Token prices fetched in {end_time - start_time} seconds.",
            ),
            CliColor.SUCCESS,
        )
