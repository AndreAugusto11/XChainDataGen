import time

from sqlalchemy import text

from config.constants import Bridge
from extractor.stargate.constants import (STARGATE_OFT_TOKEN_MAPPING,
                                          STARGATE_POOL_TOKEN_MAPPING)
from generator.base_generator import BaseGenerator
from generator.common.price_generator import PriceGenerator
from repository.common.repository import (NativeTokenRepository,
                                          TokenMetadataRepository,
                                          TokenPriceRepository)
from repository.database import DBSession
from repository.stargate.repository import *
from utils.utils import (CliColor, CustomException,
                         build_log_message_generator, log_error, log_to_cli)


class StargateGenerator(BaseGenerator):
    CLASS_NAME = "StargateGenerator"

    def __init__(self) -> None:
        super().__init__()
        self.bridge = Bridge.STARGATE
        self.price_generator = PriceGenerator()

    def bind_db_to_repos(self):
        self.transactions_repo = StargateBlockchainTransactionRepository(DBSession)
        self.bus_cross_chain_transactions_repo = StargateBusCrossChainTransactionRepository(DBSession)
        self.cross_chain_token_transfers_repo = StargateCrossChainTokenTransferRepository(DBSession)
        self.oft_cross_chain_transactions = StargateOFTCrossChainTransactionRepository(DBSession)
        self.cross_chain_swap_repo = StargateCrossChainSwapRepository(DBSession)

        self.token_metadata_repo = TokenMetadataRepository(DBSession)
        self.token_price_repo = TokenPriceRepository(DBSession)
        self.native_token_repo = NativeTokenRepository(DBSession)

    def generate_cross_chain_data(self):
        func_name = "create_cross_chain_transactions"

        try:
            ## CREATE CROSS CHAIN TRANSACTIONS
            self.match_bus_transactions()
            self.match_oft_transfers()
            self.match_token_transfers()
            self.match_swap_events()

            start_ts = int(self.transactions_repo.get_min_timestamp()) - 86400
            end_ts = int(self.transactions_repo.get_max_timestamp()) + 86400

            ## POPULATE TOKEN TABLES WITH NATIVE TOKEN INFO
            PriceGenerator.populate_native_tokens(self.bridge, self.native_token_repo, self.token_metadata_repo, self.token_price_repo, start_ts, end_ts)

            ## POPULATE TOKEN TABLES WITH CROSS CHAIN TRANSACTIONS INFO
            cctxs = self.bus_cross_chain_transactions_repo.get_unique_src_dst_contract_pairs()
            self.populate_token_info_liquidity_pools(cctxs, start_ts, end_ts)

            cctxs = self.oft_cross_chain_transactions.get_unique_src_dst_contract_pairs()
            self.populate_token_info_liquidity_pools(cctxs, start_ts, end_ts)

            cctxs = self.cross_chain_token_transfers_repo.get_unique_src_dst_contract_pairs()
            self.populate_token_info_cctxs(cctxs, start_ts, end_ts)

            cctxs = self.cross_chain_swap_repo.get_unique_src_dst_contract_pairs()
            self.populate_token_info_liquidity_pools(cctxs, start_ts, end_ts)

            ## CALCULATE USD VALUES (AND POPULATE CORRESPONDING COLUMNS) FOR CROSS CHAIN TRANSACTIONS (VALUE TRANSACTED AND FEES)
            PriceGenerator.calculate_cctx_usd_values(self.bridge, self.bus_cross_chain_transactions_repo, "stargate_bus_cross_chain_transactions", "amount_received_ld", "src_blockchain", "src_contract_address", "user_timestamp", "amount_received_ld_usd")
            PriceGenerator.calculate_cctx_usd_values(self.bridge, self.bus_cross_chain_transactions_repo, "stargate_bus_cross_chain_transactions", "amount_sent_ld", "src_blockchain", "src_contract_address", "user_timestamp", "amount_sent_ld_usd")
            PriceGenerator.calculate_cctx_native_usd_values(self.bridge, self.bus_cross_chain_transactions_repo, "stargate_bus_cross_chain_transactions", "user_timestamp", "src_blockchain", "user_fee",  "user_fee_usd")
            PriceGenerator.calculate_cctx_native_usd_values(self.bridge, self.bus_cross_chain_transactions_repo, "stargate_bus_cross_chain_transactions", "user_timestamp", "src_blockchain", "bus_fee",      "bus_fee_usd")
            PriceGenerator.calculate_cctx_native_usd_values(self.bridge, self.bus_cross_chain_transactions_repo, "stargate_bus_cross_chain_transactions", "user_timestamp", "src_blockchain", "bus_fare",     "bus_fare_usd")
            PriceGenerator.calculate_cctx_native_usd_values(self.bridge, self.bus_cross_chain_transactions_repo, "stargate_bus_cross_chain_transactions", "user_timestamp", "src_blockchain", "executor_fee", "executor_fee_usd")
            PriceGenerator.calculate_cctx_native_usd_values(self.bridge, self.bus_cross_chain_transactions_repo, "stargate_bus_cross_chain_transactions", "user_timestamp", "src_blockchain", "dvn_fee",      "dvn_fee_usd")
            PriceGenerator.calculate_cctx_native_usd_values(self.bridge, self.bus_cross_chain_transactions_repo, "stargate_bus_cross_chain_transactions", "dst_timestamp",  "dst_blockchain", "dst_fee",   "dst_fee_usd")

            PriceGenerator.calculate_cctx_usd_values(self.bridge, self.oft_cross_chain_transactions, "stargate_oft_cross_chain_transactions", "amount", "src_blockchain", "src_contract_address", "src_timestamp", "amount_usd")
            PriceGenerator.calculate_cctx_native_usd_values(self.bridge, self.oft_cross_chain_transactions, "stargate_oft_cross_chain_transactions", "src_timestamp", "src_blockchain", "src_fee",  "src_fee_usd")
            PriceGenerator.calculate_cctx_native_usd_values(self.bridge, self.oft_cross_chain_transactions, "stargate_oft_cross_chain_transactions", "src_timestamp", "src_blockchain", "executor_fee",  "executor_fee_usd")
            PriceGenerator.calculate_cctx_native_usd_values(self.bridge, self.oft_cross_chain_transactions, "stargate_oft_cross_chain_transactions", "src_timestamp", "src_blockchain", "dvn_fee",  "dvn_fee_usd")
            PriceGenerator.calculate_cctx_native_usd_values(self.bridge, self.oft_cross_chain_transactions, "stargate_oft_cross_chain_transactions", "dst_timestamp", "dst_blockchain", "dst_fee",  "dst_fee_usd")

            PriceGenerator.calculate_cctx_usd_values(self.bridge, self.cross_chain_token_transfers_repo, "stargate_cross_chain_token_transfers", "amount", "src_blockchain", "src_contract_address", "src_timestamp", "amount_usd")
            PriceGenerator.calculate_cctx_native_usd_values(self.bridge, self.oft_cross_chain_transactions, "stargate_cross_chain_token_transfers", "src_timestamp", "src_blockchain", "src_fee",  "src_fee_usd")
            PriceGenerator.calculate_cctx_native_usd_values(self.bridge, self.oft_cross_chain_transactions, "stargate_cross_chain_token_transfers", "src_timestamp", "src_blockchain", "verifier_fee",  "verifier_fee_usd")
            PriceGenerator.calculate_cctx_native_usd_values(self.bridge, self.oft_cross_chain_transactions, "stargate_cross_chain_token_transfers", "src_timestamp", "src_blockchain", "relayer_fee",  "relayer_fee_usd")
            PriceGenerator.calculate_cctx_native_usd_values(self.bridge, self.oft_cross_chain_transactions, "stargate_cross_chain_token_transfers", "dst_timestamp", "dst_blockchain", "dst_fee",  "dst_fee_usd")

            PriceGenerator.calculate_cctx_usd_values(self.bridge, self.cross_chain_swap_repo, "stargate_cross_chain_swaps", "amount_sd", "src_blockchain", "src_contract_address", "src_timestamp", "amount_usd")
            PriceGenerator.calculate_cctx_native_usd_values(self.bridge, self.cross_chain_swap_repo, "stargate_cross_chain_swaps", "src_timestamp", "src_blockchain", "src_fee",   "src_fee_usd")
            PriceGenerator.calculate_cctx_native_usd_values(self.bridge, self.cross_chain_swap_repo, "stargate_cross_chain_swaps", "dst_timestamp", "dst_blockchain", "dst_fee",   "dst_fee_usd")
            PriceGenerator.calculate_cctx_native_usd_values(self.bridge, self.cross_chain_swap_repo, "stargate_cross_chain_swaps", "src_timestamp", "src_blockchain", "verifier_fee", "verifier_fee_usd")
            PriceGenerator.calculate_cctx_native_usd_values(self.bridge, self.cross_chain_swap_repo, "stargate_cross_chain_swaps", "src_timestamp", "src_blockchain", "relayer_fee",  "relayer_fee_usd")
            PriceGenerator.calculate_cctx_native_usd_values(self.bridge, self.cross_chain_swap_repo, "stargate_cross_chain_swaps", "src_timestamp", "src_blockchain", "protocol_fee", "protocol_fee_usd")
            PriceGenerator.calculate_cctx_native_usd_values(self.bridge, self.cross_chain_swap_repo, "stargate_cross_chain_swaps", "src_timestamp", "src_blockchain", "eq_fee",       "eq_fee_usd")
            PriceGenerator.calculate_cctx_native_usd_values(self.bridge, self.cross_chain_swap_repo, "stargate_cross_chain_swaps", "src_timestamp", "src_blockchain", "lp_fee",       "lp_fee_usd")

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
        log_to_cli(
            build_log_message_generator(self.bridge, "Matching token transfers...")
        )

        self.cross_chain_token_transfers_repo.empty_table()

        query = text(
            """
            INSERT INTO stargate_cross_chain_token_transfers (
                src_blockchain,
                src_transaction_hash,
                src_from_address,
                src_to_address,
                src_fee,
                src_fee_usd,
                src_timestamp,
                verifier_fee,
                verifier_fee_usd,
                relayer_fee,
                relayer_fee_usd,
                dst_blockchain,
                dst_transaction_hash,
                dst_from_address,
                dst_to_address,
                dst_fee,
                dst_fee_usd,
                dst_timestamp,
                src_contract_address,
                dst_contract_address,
                depositor,
                recipient,
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
                verifier_fee.fee,
                NULL as verifier_fee_usd,
                relayer_fee.fee,
                NULL as relayer_fee_usd,
                dst_tx.blockchain,
                dst_tx.transaction_hash,
                dst_tx.from_address,
                dst_tx.to_address,
                dst_tx.fee,
                NULL as dst_fee_usd,
                dst_tx.timestamp,
                oft_send_to_chain.contract_address,
                oft_receive_from_chain.contract_address,
                oft_send_to_chain.from_address,
                oft_send_to_chain.to_address,
                oft_send_to_chain.amount,
                NUlL as amount_usd
            FROM stargate_oft_send_to_chain oft_send_to_chain
            JOIN stargate_blockchain_transactions src_tx ON src_tx.transaction_hash = oft_send_to_chain.transaction_hash
            JOIN stargate_verifier_fee verifier_fee ON verifier_fee.transaction_hash = oft_send_to_chain.transaction_hash
            JOIN stargate_relayer_fee relayer_fee ON relayer_fee.transaction_hash = oft_send_to_chain.transaction_hash
            JOIN stargate_packet packet ON packet.transaction_hash = oft_send_to_chain.transaction_hash
            JOIN stargate_packet_received packet_received ON packet_received.nonce = packet.nonce AND packet_received.blockchain = packet.dst_blockchain AND packet_received.src_blockchain = packet.blockchain
            JOIN stargate_blockchain_transactions dst_tx ON dst_tx.transaction_hash = packet_received.transaction_hash
            JOIN stargate_oft_receive_from_chain oft_receive_from_chain ON oft_receive_from_chain.transaction_hash = packet_received.transaction_hash
            WHERE oft_receive_from_chain.amount = oft_send_to_chain.amount
            AND oft_send_to_chain.dst_blockchain = oft_receive_from_chain.blockchain
            AND oft_send_to_chain.blockchain = src_tx.blockchain;
        """
        )

        try:
            self.cross_chain_token_transfers_repo.populate_table(query)

            size = self.cross_chain_token_transfers_repo.get_number_of_records()

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

    def match_swap_events(self):
        func_name = "match_swap_events"

        start_time = time.time()
        log_to_cli(
            build_log_message_generator(self.bridge, "Matching cross-chain swaps...")
        )

        self.cross_chain_swap_repo.empty_table()

        query = text(
            """
            INSERT INTO stargate_cross_chain_swap (
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
                verifier_fee,
                verifier_fee_usd,
                relayer_fee,
                relayer_fee_usd,
                src_contract_address,
                dst_contract_address,
                dst_pool_id,
                depositor,
                recipient,
                amount_sd,
                protocol_fee,
                protocol_fee_usd,
                eq_fee,
                eq_fee_usd,
                eq_reward,
                lp_fee,
                lp_fee_usd,
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
                verifier_fee.fee,
                NULL as verifier_fee_usd,
                relayer_fee.fee,
                NULL as relayer_fee_usd,
                swap.contract_address,
                swap_remote.contract_address,
                swap.dst_pool_id,
                swap.from_address,
                swap_remote.to_address,
                swap_remote.amount_sd,
                swap_remote.protocol_fee,
                NULL as protocol_fee_usd,
                swap.eq_fee,
                NULL as eq_fee_usd,
                swap.eq_reward,
                swap.lp_fee,
                NULL as lp_fee_usd,
                NUlL as amount_usd
            FROM stargate_swap swap
            JOIN stargate_blockchain_transactions src_tx ON src_tx.transaction_hash = swap.transaction_hash
            JOIN stargate_verifier_fee verifier_fee ON verifier_fee.transaction_hash = swap.transaction_hash
            JOIN stargate_relayer_fee relayer_fee ON relayer_fee.transaction_hash = swap.transaction_hash
            JOIN stargate_packet packet ON packet.transaction_hash = swap.transaction_hash
            JOIN stargate_packet_received packet_received ON packet_received.nonce = packet.nonce
            JOIN stargate_blockchain_transactions dst_tx ON dst_tx.transaction_hash = packet_received.transaction_hash
            JOIN stargate_swap_remote swap_remote ON swap_remote.transaction_hash = packet_received.transaction_hash
            WHERE swap_remote.amount_sd = swap.amount_sd
            AND swap.protocol_fee = swap_remote.protocol_fee
            AND swap.eq_fee = swap_remote.dst_fee;
        """
        )

        try:
            self.cross_chain_swap_repo.populate_table(query)

            size = self.cross_chain_swap_repo.get_number_of_records()

            end_time = time.time()
            log_to_cli(
                build_log_message_generator(
                    self.bridge,
                    f"Cross-chain swaps matched in {end_time - start_time} seconds. Total records inserted: {size}",
                ),
                CliColor.SUCCESS,
            )
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"Error processing swap events. Error: {e}",
            )

    def match_oft_transfers(self):
        func_name = "match_oft_transfers"

        start_time = time.time()
        log_to_cli(
            build_log_message_generator(self.bridge, "Matching OFT token transfers...")
        )

        self.oft_cross_chain_transactions.empty_table()

        query = text(
            """
            INSERT INTO stargate_oft_cross_chain_transactions (
                src_blockchain,
                src_transaction_hash,
                src_from_address,
                src_to_address,
                src_fee,
                src_fee_usd,
                src_timestamp,
                executor_fee,
                executor_fee_usd,
                dvn_fee,
                dvn_fee_usd,
                dst_blockchain,
                dst_transaction_hash,
                dst_from_address,
                dst_to_address,
                dst_fee,
                dst_fee_usd,
                dst_timestamp,
                src_contract_address,
                dst_contract_address,
                depositor,
                recipient,
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
                executor_fee_paid.fee,
                NULL as executor_fee_usd,
                dvn_fee_paid.fee,
                NULL as dvn_fee_usd,
                dst_tx.blockchain,
                dst_tx.transaction_hash,
                dst_tx.from_address,
                dst_tx.to_address,
                dst_tx.fee,
                NULL as dst_fee_usd,
                dst_tx.timestamp,
                oft_sent.contract_address,
                oft_received.contract_address,
                oft_sent.from_address,
                oft_received.to_address,
                oft_sent.amount_received_ld,
                NUlL as amount_usd
            FROM stargate_oft_sent oft_sent
            JOIN stargate_blockchain_transactions src_tx ON src_tx.transaction_hash = oft_sent.transaction_hash
            JOIN stargate_executor_fee_paid executor_fee_paid ON executor_fee_paid.transaction_hash = oft_sent.transaction_hash
            JOIN stargate_dvn_fee_paid dvn_fee_paid ON dvn_fee_paid.transaction_hash = oft_sent.transaction_hash
            JOIN stargate_oft_received oft_received ON oft_received.guid = oft_sent.guid
            JOIN stargate_blockchain_transactions dst_tx ON dst_tx.transaction_hash = oft_received.transaction_hash
            WHERE oft_sent.dst_blockchain = oft_received.blockchain
            AND oft_sent.blockchain = oft_received.src_blockchain;
        """
        )

        try:
            self.oft_cross_chain_transactions.populate_table(query)

            size = self.oft_cross_chain_transactions.get_number_of_records()

            end_time = time.time()
            log_to_cli(
                build_log_message_generator(
                    self.bridge,
                    f"OFT token transfers matched in {end_time - start_time} seconds. Total records inserted: {size}",
                ),
                CliColor.SUCCESS,
            )
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"Error processing oft transfers. Error: {e}",
            )

    def match_bus_transactions(self):
        func_name = "match_bus_transactions"

        start_time = time.time()
        log_to_cli(
            build_log_message_generator(
                self.bridge, "Matching bus cross-chain transfers..."
            )
        )

        self.bus_cross_chain_transactions_repo.empty_table()

        query = text(
            """
            WITH bus_rode AS (
                SELECT *, ROW_NUMBER() OVER (PARTITION BY transaction_hash) AS event_index
                FROM stargate_bus_rode
            ),
            oft_sent AS (
                SELECT *, ROW_NUMBER() OVER (PARTITION BY transaction_hash) AS event_index
                FROM stargate_oft_sent
            ),
            oft_received AS (
                SELECT DISTINCT blockchain, transaction_hash, guid, amount_received_ld, to_address, contract_address
                FROM stargate_oft_received
            )
            INSERT INTO stargate_bus_cross_chain_transactions (
                src_blockchain,
                user_transaction_hash,
                user_from_address,
                user_to_address,
                user_fee,
                user_fee_usd,
                user_timestamp,
                bus_transaction_hash,
                bus_from_address,
                bus_to_address,
                bus_fee,
                bus_fee_usd,
                bus_timestamp,
                bus_ticket_id,
                bus_fare,
                bus_fare_usd,
                bus_guid,
                passenger,
                dst_blockchain,
                executor_fee,
                executor_fee_usd,
                dvn_fee,
                dvn_fee_usd,
                src_contract_address,
                dst_contract_address,
                amount_sent_ld,
                amount_sent_ld_usd,
                amount_received_ld,
                amount_received_ld_usd,
                dst_transaction_hash,
                dst_from_address,
                dst_to_address,
                dst_fee,
                dst_fee_usd,
                dst_timestamp
            )
            SELECT
                oft_sent.blockchain,
                oft_sent.transaction_hash,
                user_tx.from_address,
                user_tx.to_address,
                user_tx.fee,
                NULL as user_fee_usd,
                user_tx.timestamp,
                bus_tx.transaction_hash,
                bus_tx.from_address,
                bus_tx.to_address,
                bus_tx.fee,
                NULL as bus_tx_fee_usd,
                bus_tx.timestamp,
                bus_rode.ticket_id,
                bus_rode.fare,
                NULL as bus_rode_fare_usd,
                bus_driven.guid,
                oft_received.to_address,
                oft_received.blockchain,
                executor_fee_paid.fee,
                NULL as executor_fee_paid_fee_usd,
                dvn_fee_paid.fee,
                NULL as dvn_fee_paid_fee_usd,
                oft_sent.contract_address,
                oft_received.contract_address,
                oft_sent.amount_sent_ld,
                NULL as amount_sent_ld_usd,
                oft_sent.amount_received_ld,
                NULL as amount_received_ld_usd,
                dst_tx.transaction_hash,
                dst_tx.from_address,
                dst_tx.to_address,
                dst_tx.fee,
                NULL as dst_fee_usd,
                dst_tx.timestamp
            FROM stargate_bus_driven bus_driven
            JOIN bus_rode ON bus_rode.dst_blockchain = bus_driven.dst_blockchain AND bus_driven.blockchain = bus_rode.blockchain AND bus_rode.ticket_id BETWEEN bus_driven.start_ticket_id AND (bus_driven.start_ticket_id + bus_driven.num_passengers - 1)
            JOIN oft_sent ON oft_sent.transaction_hash = bus_rode.transaction_hash AND bus_rode.event_index = oft_sent.event_index
            JOIN stargate_blockchain_transactions user_tx ON user_tx.transaction_hash = oft_sent.transaction_hash
            JOIN stargate_blockchain_transactions bus_tx ON bus_tx.transaction_hash = bus_driven.transaction_hash
            JOIN oft_received ON oft_received.guid = bus_driven.guid AND lower(oft_received.to_address) = bus_rode.passenger AND (
                oft_sent.amount_received_ld = oft_received.amount_received_ld OR
                oft_sent.amount_received_ld = oft_received.amount_received_ld * 1e12 OR
                oft_sent.amount_received_ld * 1e12 = oft_received.amount_received_ld
            )
            JOIN stargate_executor_fee_paid executor_fee_paid ON executor_fee_paid.transaction_hash = bus_driven.transaction_hash
            JOIN stargate_dvn_fee_paid dvn_fee_paid ON dvn_fee_paid.transaction_hash = bus_driven.transaction_hash
            JOIN stargate_blockchain_transactions dst_tx ON dst_tx.transaction_hash = oft_received.transaction_hash
            WHERE bus_rode.blockchain = oft_sent.blockchain
            AND bus_rode.blockchain = bus_driven.blockchain
            AND oft_sent.blockchain = bus_driven.blockchain;
        """
        )

        try:
            self.bus_cross_chain_transactions_repo.populate_table(query)

            size = self.bus_cross_chain_transactions_repo.get_number_of_records()

            end_time = time.time()
            log_to_cli(
                build_log_message_generator(
                    self.bridge,
                    f"Bus cross-chain transfers matched in {end_time - start_time} seconds. Total records inserted: {size}",
                ),
                CliColor.SUCCESS,
            )
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"Error processing bus transactions. Error: {e}",
            )
        

    def populate_token_info_liquidity_pools(self, cctxs, start_ts, end_ts):
        for cctx in cctxs:
            try:
                input_token = STARGATE_POOL_TOKEN_MAPPING[cctx.src_blockchain][cctx.src_contract_address]
                output_token = STARGATE_POOL_TOKEN_MAPPING[cctx.dst_blockchain][cctx.dst_contract_address]

                self.price_generator.populate_token_info(
                    self.bridge,
                    self.token_metadata_repo,
                    self.token_price_repo,
                    cctx.src_blockchain,
                    cctx.dst_blockchain,
                    input_token,
                    output_token,
                    start_ts,
                    end_ts,
                    cctx.src_contract_address,
                    cctx.dst_contract_address,
                )
            except Exception as e:
                log_error(
                    self.bridge,
                    CustomException(
                        self.CLASS_NAME,
                        "populate_token_info_liquidity_pools",
                        f"Error populating token info for bus cross chain transactions. CCTX: {cctx} Error: {e}",
                    ),
                )


    def populate_token_info_cctxs(self, cctxs, start_ts, end_ts):
        for cctx in cctxs:
            try:
                input_token = STARGATE_OFT_TOKEN_MAPPING[cctx.src_blockchain][cctx.src_contract_address]
                output_token = STARGATE_OFT_TOKEN_MAPPING[cctx.dst_blockchain][cctx.dst_contract_address]

                self.price_generator.populate_token_info(
                    self.bridge,
                    self.token_metadata_repo,
                    self.token_price_repo,
                    cctx.src_blockchain,
                    cctx.dst_blockchain,
                    input_token,
                    output_token,
                    start_ts,
                    end_ts,
                    cctx.src_contract_address if input_token != cctx.src_contract_address else input_token,
                    cctx.dst_contract_address if output_token != cctx.dst_contract_address else output_token,
                )
            except Exception as e:
                log_error(
                    self.bridge,
                    CustomException(
                        self.CLASS_NAME,
                        "populate_token_info_cctxs",
                        f"Error populating token info for cross chain token transfers. CCTX: {cctx} Error: {e}",
                    ),
                )
