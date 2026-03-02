import time

from sqlalchemy import and_, insert, join, literal, null, select, text
from sqlalchemy.orm import aliased

from config.constants import Bridge
from generator.base_generator import BaseGenerator
from generator.common.price_generator import PriceGenerator
from repository.across.models import (
    AcrossBlockchainTransaction,
    AcrossCrossChainTransaction,
    AcrossFilledRelay,
    AcrossFundsDeposited,
)
from repository.across.repository import (
    AcrossBlockchainTransactionRepository,
    AcrossCrossChainTransactionRepository,
    AcrossFilledRelayRepository,
    AcrossFundsDepositedRepository,
    AcrossRelayerRefundRepository,
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


class AcrossGenerator(BaseGenerator):
    CLASS_NAME = "AcrossGenerator"

    def __init__(self) -> None:
        super().__init__()
        self.bridge = Bridge.ACROSS
        self.price_generator = PriceGenerator()

    def bind_db_to_repos(self):
        self.transactions_repo = AcrossBlockchainTransactionRepository(DBSession)
        self.across_relayer_refund_repo = AcrossRelayerRefundRepository(DBSession)
        self.across_filled_v3_relay_repo = AcrossFilledRelayRepository(DBSession)
        self.across_v3_funds_deposited_repo = AcrossFundsDepositedRepository(DBSession)
        self.across_blockchain_transactions_repo = AcrossBlockchainTransactionRepository(DBSession)
        self.across_cross_chain_token_transfers_repo = AcrossCrossChainTransactionRepository(
            DBSession
        )

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
            self.price_generator.populate_native_tokens(
                self.bridge,
                self.native_token_repo,
                self.token_metadata_repo,
                self.token_price_repo,
                start_ts,
                end_ts,
            )

            # The Unichain blockchain is not supported by the Alchemy API, so we need to make some
            # additions to the database manually
            self.fetch_unichain_data(start_ts, end_ts)

            cctxs = self.across_cross_chain_token_transfers_repo.get_unique_src_dst_contract_pairs()
            self.populate_token_info_tables(cctxs, start_ts, end_ts)

            PriceGenerator.calculate_cctx_usd_values(
                self.bridge,
                self.across_cross_chain_token_transfers_repo,
                "across_cross_chain_transactions",
                "input_amount",
                "src_blockchain",
                "src_contract_address",
                "src_timestamp",
                "input_amount_usd",
            )
            PriceGenerator.calculate_cctx_usd_values(
                self.bridge,
                self.across_cross_chain_token_transfers_repo,
                "across_cross_chain_transactions",
                "output_amount",
                "dst_blockchain",
                "dst_contract_address",
                "src_timestamp",
                "output_amount_usd",
            )
            PriceGenerator.calculate_cctx_native_usd_values(
                self.bridge,
                self.across_cross_chain_token_transfers_repo,
                "across_cross_chain_transactions",
                "src_timestamp",
                "src_blockchain",
                "src_fee",
                "src_fee_usd",
            )
            PriceGenerator.calculate_cctx_native_usd_values(
                self.bridge,
                self.across_cross_chain_token_transfers_repo,
                "across_cross_chain_transactions",
                "dst_timestamp",
                "dst_blockchain",
                "dst_fee",
                "dst_fee_usd",
            )

            self.fix_token_symbol_clashes()

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

        self.across_cross_chain_token_transfers_repo.empty_table()

        # Build the SELECT statement
        deposit = aliased(AcrossFundsDeposited)
        src_tx = aliased(AcrossBlockchainTransaction)
        fill = aliased(AcrossFilledRelay)
        dst_tx = aliased(AcrossBlockchainTransaction)

        # Join tables
        j1 = join(deposit, src_tx, deposit.transaction_hash == src_tx.transaction_hash)
        j2 = join(
            j1,
            fill,
            and_(
                fill.deposit_id == deposit.deposit_id, fill.output_amount == deposit.output_amount
            ),
        )
        j3 = join(j2, dst_tx, dst_tx.transaction_hash == fill.transaction_hash)

        # Build the SELECT columns
        select_stmt = (
            select(
                src_tx.blockchain.label("src_blockchain"),
                src_tx.transaction_hash.label("src_transaction_hash"),
                src_tx.from_address.label("src_from_address"),
                src_tx.to_address.label("src_to_address"),
                src_tx.fee.label("src_fee"),
                null().label("src_fee_usd"),
                src_tx.timestamp.label("src_timestamp"),
                dst_tx.blockchain.label("dst_blockchain"),
                dst_tx.transaction_hash.label("dst_transaction_hash"),
                dst_tx.from_address.label("dst_from_address"),
                dst_tx.to_address.label("dst_to_address"),
                dst_tx.fee.label("dst_fee"),
                null().label("dst_fee_usd"),
                dst_tx.timestamp.label("dst_timestamp"),
                null().label("refund_blockchain"),
                null().label("refund_transaction_hash"),
                null().label("refund_from_address"),
                null().label("refund_to_address"),
                null().label("refund_fee"),
                null().label("refund_value"),
                null().label("refund_fee_usd"),
                null().label("refund_timestamp"),
                deposit.deposit_id.label("intent_id"),
                deposit.depositor.label("depositor"),
                deposit.recipient.label("recipient"),
                deposit.input_token.label("src_contract_address"),
                fill.output_token.label("dst_contract_address"),
                deposit.input_amount.label("input_amount"),
                null().label("input_amount_usd"),
                null().label("middle_src_token"),
                null().label("middle_src_amount"),
                null().label("middle_src_amount_usd"),
                null().label("middle_dst_token"),
                null().label("middle_dst_amount"),
                null().label("middle_dst_amount_usd"),
                deposit.output_amount.label("output_amount"),
                null().label("output_amount_usd"),
                deposit.quote_timestamp.label("quote_timestamp"),
                deposit.fill_deadline.label("fill_deadline"),
                deposit.exclusivity_deadline.label("exclusivity_deadline"),
                deposit.exclusive_relayer.label("exclusive_relayer"),
                fill.fill_type.label("fill_type"),
                literal(0).label("native_fix_fee"),
                null().label("native_fix_fee_usd"),
                literal(0).label("percent_fee"),
                null().label("percent_fee_usd"),
            )
            .select_from(j3)
            .where(
                and_(
                    deposit.destination_chain == dst_tx.blockchain,
                    fill.src_chain == src_tx.blockchain,
                )
            )
        )

        # Build the INSERT statement
        insert_stmt = insert(AcrossCrossChainTransaction).from_select(
            [
                "src_blockchain",
                "src_transaction_hash",
                "src_from_address",
                "src_to_address",
                "src_fee",
                "src_fee_usd",
                "src_timestamp",
                "dst_blockchain",
                "dst_transaction_hash",
                "dst_from_address",
                "dst_to_address",
                "dst_fee",
                "dst_fee_usd",
                "dst_timestamp",
                "refund_blockchain",
                "refund_transaction_hash",
                "refund_from_address",
                "refund_to_address",
                "refund_fee",
                "refund_value",
                "refund_fee_usd",
                "refund_timestamp",
                "intent_id",
                "depositor",
                "recipient",
                "src_contract_address",
                "dst_contract_address",
                "input_amount",
                "input_amount_usd",
                "middle_src_token",
                "middle_src_amount",
                "middle_src_amount_usd",
                "middle_dst_token",
                "middle_dst_amount",
                "middle_dst_amount_usd",
                "output_amount",
                "output_amount_usd",
                "quote_timestamp",
                "fill_deadline",
                "exclusivity_deadline",
                "exclusive_relayer",
                "fill_type",
                "native_fix_fee",
                "native_fix_fee_usd",
                "percent_fee",
                "percent_fee_usd",
            ],
            select_stmt,
        )

        try:
            self.across_cross_chain_token_transfers_repo.execute(insert_stmt)

            size = self.across_cross_chain_token_transfers_repo.get_number_of_records()

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

    def fetch_unichain_data(self, start_ts, end_ts):
        if not self.native_token_repo.get_native_token_by_blockchain("unichain"):
            self.native_token_repo.create(
                {
                    "symbol": "WETH",
                    "blockchain": "unichain",
                }
            )

        if not self.token_metadata_repo.get_token_metadata_by_symbol_and_blockchain(
            "WETH", "unichain"
        ):
            self.token_metadata_repo.create(
                {
                    "symbol": "WETH",
                    "name": "Wrapped Ether",
                    "decimals": 18,
                    "blockchain": "unichain",
                    "address": "0x4200000000000000000000000000000000000006",
                }
            )

            self.token_metadata_repo.create(
                {
                    "symbol": "WETH",
                    "name": "Wrapped Ether",
                    "decimals": 18,
                    "blockchain": "unichain",
                    "address": "0x0000000000000000000000000000000000000000",
                }
            )

        if not self.token_metadata_repo.get_token_metadata_by_symbol_and_blockchain(
            "USDC", "unichain"
        ):
            self.token_metadata_repo.create(
                {
                    "symbol": "USDC",
                    "name": "USD Coin",
                    "decimals": 6,
                    "blockchain": "unichain",
                    "address": "0x078d782b760474a361dda0af3839290b0ef57ad6",
                }
            )

    def fix_token_symbol_clashes(self):
        """
        The calculate_cctx_usd_values function calculated the USD value of the input and output
        amounts, based on the symbol. The reason why we base it on the symbol only (and not
        symbol + name) is because in multiple blockchains, the same token can have different
        names. Therefore, asking for the price of the same token in multiple blockchains would
        return different prices (e.g., 500 token X worth of 1 USD in one blockchain, and 500
        token X worth of 2 USD in another blockchain, leading to fake token price disparities).
        However, this can cause problems when multiple tokens have the same symbol. This
        function serves to fix those problems. Unfortunately, the only way to fix this is by
        manually checking the generated cctxs, checking values that are completely disparate,
        retrieving token contracts and updating the query to fetch the correct token price.

        An example is PEPE and BasedPEPE. Both have the same symbol, but different names. The
        price of PEPE at the moment is X USD, and the price of BasedPEPE is X*10^-3 USD.
        """

        func_name = "fix_token_symbol_clashes"

        query = text(
            """
                UPDATE across_cross_chain_transactions cctx
                SET output_amount_usd = token_price.price_usd * cctx.output_amount / power(10, token_metadata.decimals)
                FROM token_metadata
                JOIN token_price
                    ON token_metadata.symbol = token_price.symbol
                    AND token_metadata.name = token_price.name
                WHERE lower(cctx.dst_contract_address) = lower(token_metadata.address)
                AND cctx.dst_blockchain = token_metadata.blockchain
                AND CAST(TO_TIMESTAMP(cctx.src_timestamp) AS DATE) = token_price.date
                AND dst_contract_address = '0x52b492a33E447Cdb854c7FC19F1e57E8BfA1777D';
            """  # noqa: E501
        )

        try:
            self.across_cross_chain_token_transfers_repo.execute(query)

        except Exception as e:
            raise CustomException(
                PriceGenerator.CLASS_NAME,
                func_name,
                (
                    f"Error processing USD values for BasedPEPE in across_cross_chain_transactions."
                    f"Error: {e}"
                ),
            ) from e
