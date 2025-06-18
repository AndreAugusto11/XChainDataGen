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
from repository.ronin.repository import (
    RoninBlockchainTransactionRepository,
    RoninCrossChainTransactionRepository,
    RoninDepositRequestedRepository,
    RoninTokenDepositedRepository,
    RoninTokenWithdrewRepository,
    RoninWithdrawalRequestedRepository,
)
from utils.utils import (
    CliColor,
    CustomException,
    build_log_message_generator,
    log_error,
    log_to_cli,
)


class RoninGenerator(BaseGenerator):
    CLASS_NAME = "RoninGenerator"

    def __init__(self) -> None:
        super().__init__()
        self.bridge = Bridge.RONIN
        self.price_generator = PriceGenerator()

    def bind_db_to_repos(self):
        self.transactions_repo = RoninBlockchainTransactionRepository(DBSession)
        self.deposit_requested_repo = RoninDepositRequestedRepository(DBSession)
        self.token_deposited_repo = RoninTokenDepositedRepository(DBSession)
        self.withdrawal_requested_repo = RoninWithdrawalRequestedRepository(DBSession)
        self.token_withdrew_repo = RoninTokenWithdrewRepository(DBSession)

        self.cross_chain_transactions_repo = RoninCrossChainTransactionRepository(DBSession)

        self.token_metadata_repo = TokenMetadataRepository(DBSession)
        self.token_price_repo = TokenPriceRepository(DBSession)
        self.native_token_repo = NativeTokenRepository(DBSession)

    def generate_cross_chain_data(self):
        func_name = "create_cross_chain_transactions"

        try:
            self.match_deposits()

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

            # The Ronin blockchain is not supported by the Alchemy API, so we need to make some
            # additions to the database manually
            self.fetch_ronin_data()

            cctxs = self.cross_chain_transactions_repo.get_unique_src_dst_contract_pairs()
            self.populate_token_info_tables(cctxs, start_ts, end_ts)

            PriceGenerator.calculate_cctx_usd_values(
                self.bridge,
                self.cross_chain_transactions_repo,
                "ronin_cross_chain_transactions",
                "amount",
                "src_blockchain",
                "src_contract_address",
                "src_timestamp",
                "amount_usd",
            )
            PriceGenerator.calculate_cctx_usd_values(
                self.bridge,
                self.cross_chain_transactions_repo,
                "ronin_cross_chain_transactions",
                "amount",
                "dst_blockchain",
                "dst_contract_address",
                "dst_timestamp",
                "amount_usd",
            )
            PriceGenerator.calculate_cctx_native_usd_values(
                self.bridge,
                self.cross_chain_transactions_repo,
                "ronin_cross_chain_transactions",
                "src_timestamp",
                "src_blockchain",
                "src_fee",
                "src_fee_usd",
            )
            PriceGenerator.calculate_cctx_native_usd_values(
                self.bridge,
                self.cross_chain_transactions_repo,
                "ronin_cross_chain_transactions",
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

    def match_deposits(self):
        func_name = "match_deposits"

        start_time = time.time()
        log_to_cli(
            build_log_message_generator(self.bridge, "Matching cross-chain token transfers...")
        )

        self.cross_chain_transactions_repo.empty_table()

        query = text(
            """
            INSERT INTO ronin_cross_chain_transactions (
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
                dst_contract_address,
                amount,
                amount_usd
            )
            (SELECT
                src_tx.blockchain,
                src_tx.transaction_hash,
                src_tx.from_address,
                src_tx.to_address,
                src_tx.fee,
                NULL::double precision as src_fee_usd,
                src_tx.timestamp,
                dst_tx.blockchain,
                dst_tx.transaction_hash,
                dst_tx.from_address,
                dst_tx.to_address,
                dst_tx.fee,
                NULL::double precision as dst_fee_usd,
                dst_tx.timestamp,
                deposit.deposit_id,
                deposit.depositor,
                deposit.recipient,
                deposit.input_token,
                deposit.output_token,
                deposit.amount,
                NULL::double precision as amount_usd
            FROM ronin_deposit_requested deposit
            JOIN ronin_blockchain_transactions src_tx ON src_tx.transaction_hash = deposit.transaction_hash
            JOIN ronin_token_deposited fill ON fill.deposit_id = deposit.deposit_id
            JOIN ronin_blockchain_transactions dst_tx ON dst_tx.transaction_hash = fill.transaction_hash
            WHERE deposit.amount = fill.amount
            AND deposit.depositor = fill.depositor
            AND deposit.recipient = fill.recipient
            AND deposit.input_token = fill.input_token
            AND deposit.output_token = fill.output_token
            UNION
            SELECT
                src_tx.blockchain,
                src_tx.transaction_hash,
                src_tx.from_address,
                src_tx.to_address,
                src_tx.fee,
                NULL::double precision as src_fee_usd,
                src_tx.timestamp,
                dst_tx.blockchain,
                dst_tx.transaction_hash,
                dst_tx.from_address,
                dst_tx.to_address,
                dst_tx.fee,
                NULL::double precision as dst_fee_usd,
                dst_tx.timestamp,
                withdrawal.withdrawal_id,
                withdrawal.withdrawer,
                withdrawal.recipient,
                withdrawal.input_token,
                withdrawal.output_token,
                withdrawal.amount,
                NULL::double precision as amount_usd
            FROM ronin_withdrawal_requested withdrawal
            JOIN ronin_blockchain_transactions src_tx ON src_tx.transaction_hash = withdrawal.transaction_hash
            JOIN ronin_token_withdrew fill ON fill.withdrawal_id = withdrawal.withdrawal_id
            JOIN ronin_blockchain_transactions dst_tx ON dst_tx.transaction_hash = fill.transaction_hash
            WHERE withdrawal.amount = fill.amount
            AND withdrawal.withdrawer = fill.withdrawer
            AND withdrawal.recipient = fill.recipient
            AND withdrawal.recipient = fill.recipient
            AND withdrawal.input_token = fill.input_token
            AND withdrawal.output_token = fill.output_token);
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

    def fetch_ronin_data(self):
        if not self.native_token_repo.get_native_token_by_blockchain("ronin"):
            self.native_token_repo.create(
                {
                    "symbol": "AXS",
                    "blockchain": "ronin",
                }
            )

        if not self.token_metadata_repo.get_token_metadata_by_symbol("AXS"):
            self.token_metadata_repo.create(
                {
                    "symbol": "AXS",
                    "name": "Axie Infinity",
                    "decimals": 18,
                    "blockchain": "ronin",
                    "address": None,
                }
            )

            # we don't fetch the price of AXS because it will be fetched
            # through Alchemy using the AXS token on Ethereum later on
