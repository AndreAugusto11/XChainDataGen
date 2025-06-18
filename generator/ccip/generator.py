import time

from sqlalchemy import text

from config.constants import Bridge
from generator.base_generator import BaseGenerator
from generator.common.price_generator import PriceGenerator
from repository.ccip.repository import (
    CCIPBlockchainTransactionRepository,
    CCIPCrossChainTransactionsRepository,
    CCIPExecutionStateChangedRepository,
    CCIPSendRequestedRepository,
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


class CcipGenerator(BaseGenerator):
    CLASS_NAME = "CcipGenerator"

    def __init__(self) -> None:
        super().__init__()
        self.bridge = Bridge.CCIP
        self.price_generator = PriceGenerator()

    def bind_db_to_repos(self):
        self.transactions_repo = CCIPBlockchainTransactionRepository(DBSession)
        self.send_requested_repo = CCIPSendRequestedRepository(DBSession)
        self.execution_state_changed_repo = CCIPExecutionStateChangedRepository(DBSession)
        self.cross_chain_transactions_repo = CCIPCrossChainTransactionsRepository(DBSession)

        self.token_metadata_repo = TokenMetadataRepository(DBSession)
        self.token_price_repo = TokenPriceRepository(DBSession)
        self.native_token_repo = NativeTokenRepository(DBSession)

    def generate_cross_chain_data(self):
        func_name = "generate_cross_chain_data"

        try:
            self.match_cctxs()

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

            cctxs = self.cross_chain_transactions_repo.get_unique_src_dst_contract_pairs()
            self.populate_token_info_tables(cctxs, start_ts, end_ts)

            PriceGenerator.calculate_cctx_usd_values(
                self.bridge,
                self.cross_chain_transactions_repo,
                "ccip_cross_chain_transactions",
                "amount",
                "src_blockchain",
                "src_contract_address",
                "src_timestamp",
                "amount_usd",
            )
            PriceGenerator.calculate_cctx_usd_values(
                self.bridge,
                self.cross_chain_transactions_repo,
                "ccip_cross_chain_transactions",
                "fee_token_amount",
                "src_blockchain",
                "fee_token",
                "src_timestamp",
                "fee_token_amount_usd",
            )
            PriceGenerator.calculate_cctx_native_usd_values(
                self.bridge,
                self.cross_chain_transactions_repo,
                "ccip_cross_chain_transactions",
                "src_timestamp",
                "src_blockchain",
                "src_fee",
                "src_fee_usd",
            )
            PriceGenerator.calculate_cctx_native_usd_values(
                self.bridge,
                self.cross_chain_transactions_repo,
                "ccip_cross_chain_transactions",
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

    def match_cctxs(self):
        func_name = "match_cctxs"

        start_time = time.time()
        log_to_cli(
            build_log_message_generator(self.bridge, "Matching cross-chain token transfers...")
        )

        self.cross_chain_transactions_repo.empty_table()

        query = text(
            """
            INSERT INTO ccip_cross_chain_transactions (
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
                fee_token,
                fee_token_amount,
                fee_token_amount_usd,
                amount,
                amount_usd
            )
            SELECT
                src_tx.blockchain AS src_blockchain,
                src_tx.transaction_hash AS src_tx_hash,
                src_tx.from_address AS src_from_address,
                src_tx.to_address AS src_to_address,
                src_tx.fee AS src_fee,
                NULL AS src_fee_usd,
                src_tx.timestamp AS src_timestamp,
                dst_tx.blockchain AS dst_blockchain,
                dst_tx.transaction_hash AS dst_tx_hash,
                dst_tx.from_address AS dst_from_address,
                dst_tx.to_address AS dst_to_address,
                dst_tx.fee AS dst_fee,
                NULL AS dst_fee_usd,
                dst_tx.timestamp AS dst_timestamp,
                deposit.id AS deposit_id,
                deposit.sender AS depositor,
                deposit.receiver AS recipient,
                deposit.input_token AS src_contract_address,
                deposit.fee_token AS fee_token,
                deposit.fee_token_amount AS fee_token_amount,
                NULL AS fee_token_amount_usd,
                deposit.amount AS src_amount,
                NULL AS src_amount_usd
            FROM ccip_send_requested deposit
            JOIN ccip_blockchain_transactions src_tx ON deposit.transaction_hash = src_tx.transaction_hash
            JOIN ccip_execution_state_changed fill ON fill.message_id = deposit.message_id AND fill.sequence_number = deposit.sequence_number
            JOIN ccip_blockchain_transactions dst_tx ON dst_tx.transaction_hash = fill.transaction_hash
            WHERE deposit.input_token is not NULL;
        """  # noqa: E501
        )

        try:
            self.cross_chain_transactions_repo.execute(query)

            size = self.cross_chain_transactions_repo.get_number_of_records()

            end_time = time.time()
            log_to_cli(
                build_log_message_generator(
                    self.bridge,
                    (
                        f"Token transfers matched in {end_time - start_time} seconds. "
                        f"Total records inserted: {size}"
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
                cctx.src_blockchain,
                None,
                cctx.src_contract_address,
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
