import time

from sqlalchemy import text

from config.constants import Bridge
from generator.base_generator import BaseGenerator
from generator.common.price_generator import PriceGenerator
from repository.common.repository import (
    NativeTokenRepository,
    TokenMetadataRepository,
    TokenPriceRepository,
)
from repository.database import DBSession
from repository.debridge.repository import (
    DeBridgeBlockchainTransactionRepository,
    DeBridgeClaimedUnlockRepository,
    DeBridgeCreatedOrderRepository,
    DeBridgeCrossChainTransactionsRepository,
    DeBridgeFulfilledOrderRepository,
    DeBridgeSentOrderUnlockRepository,
)
from utils.utils import (
    CliColor,
    CustomException,
    build_log_message_generator,
    log_error,
    log_to_cli,
)


class DebridgeGenerator(BaseGenerator):
    CLASS_NAME = "DebridgeGenerator"

    def __init__(self) -> None:
        super().__init__()
        self.bridge = Bridge.DEBRIDGE
        self.price_generator = PriceGenerator()

    def bind_db_to_repos(self):
        self.transactions_repo = DeBridgeBlockchainTransactionRepository(DBSession)
        self.created_orders_repo = DeBridgeCreatedOrderRepository(DBSession)
        self.fulfilled_orders_repo = DeBridgeFulfilledOrderRepository(DBSession)
        self.claimed_unlock_repo = DeBridgeClaimedUnlockRepository(DBSession)
        self.sent_order_unlock_repo = DeBridgeSentOrderUnlockRepository(DBSession)

        self.debridge_cross_chain_transactions = DeBridgeCrossChainTransactionsRepository(DBSession)

        self.token_metadata_repo = TokenMetadataRepository(DBSession)
        self.token_price_repo = TokenPriceRepository(DBSession)
        self.native_token_repo = NativeTokenRepository(DBSession)

    def generate_cross_chain_data(self):
        func_name = "create_cross_chain_transactions"

        try:
            self.match_cctxs()

            start_ts = int(self.transactions_repo.get_min_timestamp()) - 86400
            end_ts = int(self.transactions_repo.get_max_timestamp()) + 86400

            ## POPULATE TOKEN TABLES WITH NATIVE TOKEN INFO
            PriceGenerator.populate_native_tokens(
                self.bridge,
                self.native_token_repo,
                self.token_metadata_repo,
                self.token_price_repo,
                start_ts,
                end_ts,
            )

            cctxs = self.debridge_cross_chain_transactions.get_unique_src_dst_contract_pairs()
            self.populate_token_info_tables(cctxs, start_ts, end_ts)

            self.fill_null_address_tokens()

            # a lot of token addresses in Gnosis are not being recognized by alchemy, so we fetch
            # from both the src and dst blockchains, to make sure we use the Ethereum contracts
            PriceGenerator.calculate_cctx_usd_values(
                self.bridge,
                self.debridge_cross_chain_transactions,
                "debridge_cross_chain_transactions",
                "input_amount",
                "src_blockchain",
                "src_contract_address",
                "src_timestamp",
                "input_amount_usd",
            )
            PriceGenerator.calculate_cctx_usd_values(
                self.bridge,
                self.debridge_cross_chain_transactions,
                "debridge_cross_chain_transactions",
                "output_amount",
                "dst_blockchain",
                "dst_contract_address",
                "dst_timestamp",
                "output_amount_usd",
            )

            PriceGenerator.calculate_cctx_native_usd_values(
                self.bridge,
                self.debridge_cross_chain_transactions,
                "debridge_cross_chain_transactions",
                "src_timestamp",
                "src_blockchain",
                "src_fee",
                "src_fee_usd",
            )
            PriceGenerator.calculate_cctx_native_usd_values(
                self.bridge,
                self.debridge_cross_chain_transactions,
                "debridge_cross_chain_transactions",
                "dst_timestamp",
                "dst_blockchain",
                "dst_fee",
                "dst_fee_usd",
            )
            PriceGenerator.calculate_cctx_native_usd_values(
                self.bridge,
                self.debridge_cross_chain_transactions,
                "debridge_cross_chain_transactions",
                "dst_timestamp",
                "dst_blockchain",
                "native_fix_fee",
                "native_fix_fee_usd",
            )
            PriceGenerator.calculate_cctx_native_usd_values(
                self.bridge,
                self.debridge_cross_chain_transactions,
                "debridge_cross_chain_transactions",
                "dst_timestamp",
                "dst_blockchain",
                "percent_fee",
                "percent_fee_usd",
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
        log_to_cli(build_log_message_generator(self.bridge, "Matching deBridge token transfers..."))

        self.debridge_cross_chain_transactions.empty_table()

        query = text(
            """
            INSERT INTO debridge_cross_chain_transactions (
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
                message_id,
                depositor,
                recipient,
                src_contract_address,
                dst_contract_address,
                input_amount,
                input_amount_usd,
                output_amount,
                output_amount_usd,
                native_fix_fee,
                native_fix_fee_usd,
                percent_fee,
                percent_fee_usd
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
                NULL as message_id,
                src_tx.from_address,
                deposit.receiver_dst,
                deposit.give_token_address,
                deposit.take_token_address,
                deposit.give_amount,
                NULL as input_amount_usd,
                deposit.take_amount,
                NULL as output_amount_usd,
                deposit.native_fix_fee,
                NULL as native_fix_fee_usd,
                deposit.percent_fee,
                NULL as percent_fee_usd
            FROM debridge_created_order deposit
            JOIN debridge_blockchain_transaction src_tx ON src_tx.transaction_hash = deposit.transaction_hash
            JOIN debridge_fulfilled_order fill ON fill.order_id = deposit.order_id
            JOIN debridge_blockchain_transaction dst_tx ON dst_tx.transaction_hash = fill.transaction_hash;
        """  # noqa: E501
        )

        try:
            self.debridge_cross_chain_transactions.execute(query)

            size = self.debridge_cross_chain_transactions.get_number_of_records()

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

    def fill_null_address_tokens(self):
        """
        DeBridge uses the null address (0x0000000000000000000000000000000000000000) when
        transferringthe native tokens in give_token_address and take_token_address.
        We need to match them in the database to the native token address of the src and
        dst blockchains.
        """

        func_name = "fill_null_address_tokens"

        start_time = time.time()
        log_to_cli(build_log_message_generator(self.bridge, "Filling null address tokens..."))

        try:
            query = text(
                """
                with null_addresses as (
                    select id, symbol, name, decimals, blockchain, address
                    from token_metadata
                    where address = '0x0000000000000000000000000000000000000000'
                )
                update token_metadata
                set symbol = native_token.symbol, decimals = 18
                from null_addresses
                join native_token on native_token.blockchain = null_addresses.blockchain
                where token_metadata.address = '0x0000000000000000000000000000000000000000';
                """
            )

            self.token_metadata_repo.execute(query)

            end_time = time.time()
            log_to_cli(
                build_log_message_generator(
                    self.bridge,
                    f"Null address tokens filled in {end_time - start_time} seconds.",
                ),
                CliColor.SUCCESS,
            )
        except Exception as e:
            exception = CustomException(
                self.CLASS_NAME,
                func_name,
                f"Error filling null address tokens. Error: {e}",
            )
            log_error(self.bridge, exception)
            raise exception from e

    def populate_token_info_tables(self, cctxs, start_ts, end_ts):
        start_time = time.time()
        log_to_cli(build_log_message_generator(self.bridge, "Fetching token prices..."))

        for cctx in cctxs:
            self.price_generator.populate_token_info(
                self.bridge,
                self.token_metadata_repo,
                self.token_price_repo,
                cctx.src_blockchain,
                cctx.dst_blockchain,
                cctx.src_contract_address,
                cctx.dst_contract_address,
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
