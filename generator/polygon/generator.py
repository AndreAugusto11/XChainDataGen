import time

from sqlalchemy import text

from config.constants import Bridge
from generator.base_generator import BaseGenerator
from generator.common.price_generator import PriceGenerator
from repository.common.repository import *
from repository.database import DBSession
from repository.polygon.repository import *
from utils.utils import (CliColor, CustomException,
                         build_log_message_generator, log_error, log_to_cli)


class PolygonGenerator(BaseGenerator):
    CLASS_NAME = "PolygonGenerator"

    def __init__(self) -> None:
        super().__init__()
        self.bridge = Bridge.POLYGON
        self.price_generator = PriceGenerator()

    def bind_db_to_repos(self):
        self.transactions_repo = PolygonBlockchainTransactionRepository(DBSession)
        self.token_deposited_repo = PolygonTokenDepositedRepository(DBSession)

        self.pos_bridge_cross_chain_transactions_repo = PolygonCrossChainTransactionsRepository(DBSession)
        self.plasma_bridge_cross_chain_transactions_repo = PolygonPlasmaCrossChainTransactionsRepository(DBSession)

        self.token_metadata_repo = TokenMetadataRepository(DBSession)
        self.token_price_repo = TokenPriceRepository(DBSession)
        self.native_token_repo = NativeTokenRepository(DBSession)

    def generate_cross_chain_data(self):
        func_name = "generate_cross_chain_data"

        try:
            self.pos_bridge_match_deposits()
            self.plasma_bridge_match_deposits()

            start_ts = int(self.transactions_repo.get_min_timestamp()) - 86400
            end_ts = int(self.transactions_repo.get_max_timestamp()) + 86400

            # POPULATE TOKEN TABLES WITH NATIVE TOKEN INFO
            PriceGenerator.populate_native_tokens(self.bridge, self.native_token_repo, self.token_metadata_repo, self.token_price_repo, start_ts, end_ts)

            cctxs = self.pos_bridge_cross_chain_transactions_repo.get_unique_src_dst_contract_pairs()
            self.populate_token_info_tables(cctxs, start_ts, end_ts)

            PriceGenerator.calculate_cctx_usd_values(self.bridge, self.pos_bridge_cross_chain_transactions_repo, "polygon_cross_chain_transactions", "amount", "src_blockchain", "src_contract_address", "src_timestamp", "amount_usd")
            PriceGenerator.calculate_cctx_native_usd_values(self.bridge, self.pos_bridge_cross_chain_transactions_repo, "polygon_cross_chain_transactions", "src_timestamp", "src_blockchain", "src_fee", "src_fee_usd")
            PriceGenerator.calculate_cctx_native_usd_values(self.bridge, self.pos_bridge_cross_chain_transactions_repo, "polygon_cross_chain_transactions", "dst_timestamp", "dst_blockchain", "dst_fee", "dst_fee_usd")

            PriceGenerator.calculate_cctx_usd_values(self.bridge, self.plasma_bridge_cross_chain_transactions_repo, "polygon_plasma_cross_chain_transactions", "amount", "src_blockchain", "src_contract_address", "src_timestamp", "amount_usd")
            PriceGenerator.calculate_cctx_native_usd_values(self.bridge, self.plasma_bridge_cross_chain_transactions_repo, "polygon_plasma_cross_chain_transactions", "src_timestamp", "src_blockchain", "src_fee", "src_fee_usd")
            PriceGenerator.calculate_cctx_native_usd_values(self.bridge, self.plasma_bridge_cross_chain_transactions_repo, "polygon_plasma_cross_chain_transactions", "dst_timestamp", "dst_blockchain", "dst_fee", "dst_fee_usd")
        except Exception as e:
            exception = CustomException(
                self.CLASS_NAME,
                func_name,
                f"Error processing cross chain transactions. Error: {e}",
            )
            log_error(self.bridge, exception)


    def pos_bridge_match_deposits(self):
        func_name = "pos_bridge_match_deposits"

        start_time = time.time()
        log_to_cli(
            build_log_message_generator(self.bridge, "Matching PoS Bridge cross-chain token transfers...")
        )

        self.pos_bridge_cross_chain_transactions_repo.empty_table()

        query = text(
            """
            INSERT INTO polygon_cross_chain_transactions (
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
                deposit.depositor AS depositor,
                deposit.deposit_receiver AS recipient,
                deposit.root_token AS src_contract_address,
                deposit.amount AS src_amount,
                NULL AS src_amount_usd
            FROM polygon_locked_token deposit
            JOIN polygon_state_synced deposit_state ON deposit_state.transaction_hash = deposit.transaction_hash
            JOIN polygon_blockchain_transactions src_tx ON deposit.transaction_hash = src_tx.transaction_hash
            JOIN polygon_state_comitted fill ON fill.state_id = deposit_state.state_id
            JOIN polygon_blockchain_transactions dst_tx ON dst_tx.transaction_hash = fill.transaction_hash;
        """
        )

        try:
            self.pos_bridge_cross_chain_transactions_repo.populate_table(query)

            size = self.pos_bridge_cross_chain_transactions_repo.get_number_of_records()

            end_time = time.time()
            log_to_cli(
                build_log_message_generator(
                    self.bridge,
                    f"Token transfers matched in {end_time - start_time} seconds. Total records inserted: {size}",
                ),
                CliColor.SUCCESS,
            )
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"Error processing token transfers. Error: {e}",
            )



    def plasma_bridge_match_deposits(self):
        func_name = "plasma_bridge_match_deposits"

        start_time = time.time()
        log_to_cli(
            build_log_message_generator(self.bridge, "Matching Plasma Bridge cross-chain token transfers...")
        )

        self.plasma_bridge_cross_chain_transactions_repo.empty_table()

        query = text(
            """
            INSERT INTO polygon_plasma_cross_chain_transactions (
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
            (SELECT
                src_tx.blockchain AS src_blockchain,
                src_tx.transaction_hash AS src_tx_hash,
                src_tx.from_address AS src_from_address,
                src_tx.to_address AS src_to_address,
                src_tx.fee AS src_fee,
                NULL::double precision as src_fee_usd,
                src_tx.timestamp AS src_timestamp,
                dst_tx.blockchain AS dst_blockchain,
                dst_tx.transaction_hash AS dst_tx_hash,
                dst_tx.from_address AS dst_from_address,
                dst_tx.to_address AS dst_to_address,
                dst_tx.fee AS dst_fee,
                NULL::double precision as dst_fee_usd,
                dst_tx.timestamp AS dst_timestamp,
                deposit.deposit_block_id::VARCHAR AS deposit_id,
                deposit.owner AS depositor,
                fill.user AS recipient,
                fill.root_token AS src_contract_address,
                deposit.amount AS src_amount,
                NULL::double precision as src_amount_usd
            FROM polygon_new_deposit_block deposit
            JOIN polygon_state_synced deposit_state ON deposit_state.transaction_hash = deposit.transaction_hash
            JOIN polygon_blockchain_transactions src_tx ON deposit.transaction_hash = src_tx.transaction_hash
            JOIN polygon_state_comitted fill_state ON fill_state.state_id = deposit_state.state_id
            JOIN polygon_token_deposited fill ON fill.transaction_hash = fill_state.transaction_hash
            JOIN polygon_blockchain_transactions dst_tx ON dst_tx.transaction_hash = fill_state.transaction_hash
            WHERE deposit_state.data LIKE '%' || SUBSTRING(deposit.token FROM 3) || '%'
            AND deposit.amount = fill.amount
            AND fill.deposit_count = deposit.deposit_block_id
            AND deposit.token = fill.root_token
            UNION
            SELECT
                src_tx.blockchain AS src_blockchain,
                src_tx.transaction_hash AS src_tx_hash,
                src_tx.from_address AS src_from_address,
                src_tx.to_address AS src_to_address,
                src_tx.fee AS src_fee,
                NULL::double precision as dst_fee_usd,
                src_tx.timestamp AS src_timestamp,
                dst_tx.blockchain AS dst_blockchain,
                dst_tx.transaction_hash AS dst_tx_hash,
                dst_tx.from_address AS dst_from_address,
                dst_tx.to_address AS dst_to_address,
                dst_tx.fee AS dst_fee,
                NULL::double precision as dst_fee_usd,
                dst_tx.timestamp AS dst_timestamp,
                fill.exit_id AS exit_id,
                deposit.from_address AS depositor,
                fill.user AS recipient,
                fill.token AS src_contract_address,
                deposit.amount AS src_amount,
                NULL::double precision as dst_fee_usd
            FROM polygon_pol_withdraw deposit
            JOIN polygon_blockchain_transactions src_tx ON deposit.transaction_hash = src_tx.transaction_hash
            JOIN polygon_bridge_withdraw fill ON fill.token = deposit.token AND deposit.from_address = fill.user AND deposit.amount = fill.amount
            JOIN polygon_blockchain_transactions dst_tx ON dst_tx.transaction_hash = fill.transaction_hash
            );
        """
        )

        try:
            self.plasma_bridge_cross_chain_transactions_repo.populate_table(query)

            size = self.plasma_bridge_cross_chain_transactions_repo.get_number_of_records()

            end_time = time.time()
            log_to_cli(
                build_log_message_generator(
                    self.bridge,
                    f"Token transfers matched in {end_time - start_time} seconds. Total records inserted: {size}",
                ),
                CliColor.SUCCESS,
            )
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"Error processing token transfers. Error: {e}",
            )


    def populate_token_info_tables(self, cctxs, start_ts, end_ts):
        start_time = time.time()
        log_to_cli(
            build_log_message_generator(self.bridge, "Fetching token prices...")
        )

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
