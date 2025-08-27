import time

from sqlalchemy import case, literal, text, update
from sqlalchemy.orm import aliased

from config.constants import Bridge
from generator.base_generator import BaseGenerator
from generator.common.price_generator import PriceGenerator
from repository.common.models import TokenMetadata
from repository.common.repository import (
    NativeTokenRepository,
    TokenMetadataRepository,
    TokenPriceRepository,
)
from repository.database import DBSession
from repository.debridge.models import (
    DeBridgeBlockchainTransaction,
    DeBridgeClaimedUnlock,
    DeBridgeCreatedOrder,
    DeBridgeFulfilledOrder,
)
from repository.debridge.repository import (
    DeBridgeBlockchainTransactionRepository,
    DeBridgeClaimedUnlockRepository,
    DeBridgeCreatedOrderRepository,
    DeBridgeCrossChainTransactionsRepository,
    DeBridgeFulfilledOrderRepository,
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

        self.debridge_cross_chain_transactions_repo = DeBridgeCrossChainTransactionsRepository(
            DBSession
        )

        self.token_metadata_repo = TokenMetadataRepository(DBSession)
        self.token_price_repo = TokenPriceRepository(DBSession)
        self.native_token_repo = NativeTokenRepository(DBSession)

    def generate_cross_chain_data(self):
        func_name = "create_cross_chain_transactions"

        try:
            self.match_evm_to_all_cctxs()
            self.match_sol_to_evm_cctxs()

            start_ts = int(self.transactions_repo.get_min_timestamp()) - 86400
            end_ts = int(self.transactions_repo.get_max_timestamp()) + 86400

            ## POPULATE TOKEN TABLES WITH NATIVE TOKEN INFO
            self.price_generator.populate_native_tokens(
                self.bridge,
                self.native_token_repo,
                self.token_metadata_repo,
                self.token_price_repo,
                start_ts,
                end_ts,
            )

            self.fetch_solana_data(start_ts, end_ts)

            cctxs = self.debridge_cross_chain_transactions_repo.get_unique_src_dst_contract_pairs()
            self.populate_token_info_tables(cctxs, start_ts, end_ts)

            self.fill_null_address_tokens()

            # a lot of token addresses in Gnosis are not being recognized by alchemy, so we fetch
            # from both the src and dst blockchains, to make sure we use the Ethereum contracts
            PriceGenerator.calculate_cctx_usd_values(
                self.bridge,
                self.debridge_cross_chain_transactions_repo,
                "debridge_cross_chain_transactions",
                "input_amount",
                "src_blockchain",
                "src_contract_address",
                "src_timestamp",
                "input_amount_usd",
            )
            PriceGenerator.calculate_cctx_usd_values(
                self.bridge,
                self.debridge_cross_chain_transactions_repo,
                "debridge_cross_chain_transactions",
                "output_amount",
                "dst_blockchain",
                "dst_contract_address",
                "dst_timestamp",
                "output_amount_usd",
            )
            PriceGenerator.calculate_cctx_usd_values(
                self.bridge,
                self.debridge_cross_chain_transactions_repo,
                "debridge_cross_chain_transactions",
                "refund_amount",
                "src_blockchain",
                "src_contract_address",
                "src_timestamp",
                "refund_amount_usd",
            )
            PriceGenerator.calculate_cctx_usd_values(
                self.bridge,
                self.debridge_cross_chain_transactions_repo,
                "debridge_cross_chain_transactions",
                "middle_src_amount",
                "src_blockchain",
                "middle_src_token",
                "src_timestamp",
                "middle_src_amount_usd",
            )
            PriceGenerator.calculate_cctx_usd_values(
                self.bridge,
                self.debridge_cross_chain_transactions_repo,
                "debridge_cross_chain_transactions",
                "middle_dst_amount",
                "dst_blockchain",
                "middle_dst_token",
                "dst_timestamp",
                "middle_dst_amount_usd",
            )
            PriceGenerator.calculate_cctx_usd_values(
                self.bridge,
                self.debridge_cross_chain_transactions_repo,
                "debridge_cross_chain_transactions",
                "percent_fee",
                "src_blockchain",
                "middle_src_token",
                "src_timestamp",
                "percent_fee_usd",
            )

            PriceGenerator.calculate_cctx_native_usd_values(
                self.bridge,
                self.debridge_cross_chain_transactions_repo,
                "debridge_cross_chain_transactions",
                "src_timestamp",
                "src_blockchain",
                "src_fee",
                "src_fee_usd",
            )
            PriceGenerator.calculate_cctx_native_usd_values(
                self.bridge,
                self.debridge_cross_chain_transactions_repo,
                "debridge_cross_chain_transactions",
                "dst_timestamp",
                "dst_blockchain",
                "dst_fee",
                "dst_fee_usd",
            )
            PriceGenerator.calculate_cctx_native_usd_values(
                self.bridge,
                self.debridge_cross_chain_transactions_repo,
                "debridge_cross_chain_transactions",
                "refund_timestamp",
                "refund_blockchain",
                "refund_fee",
                "refund_fee_usd",
            )
            PriceGenerator.calculate_cctx_native_usd_values(
                self.bridge,
                self.debridge_cross_chain_transactions_repo,
                "debridge_cross_chain_transactions",
                "src_timestamp",
                "src_blockchain",
                "native_fix_fee",
                "native_fix_fee_usd",
            )

        except Exception as e:
            exception = CustomException(
                self.CLASS_NAME,
                func_name,
                f"Error processing cross chain transactions. Error: {e}",
            )
            log_error(self.bridge, exception)

    def match_evm_to_all_cctxs(self):
        func_name = "match_evm_to_all_cctxs"

        start_time = time.time()
        log_to_cli(
            build_log_message_generator(
                self.bridge, "Matching deBridge EVM -> ALL token transfers..."
            )
        )

        self.debridge_cross_chain_transactions_repo.empty_table()

        try:
            results = []

            SrcTx = aliased(DeBridgeBlockchainTransaction)
            DstTx = aliased(DeBridgeBlockchainTransaction)
            RefundTx = aliased(DeBridgeBlockchainTransaction)

            with self.debridge_cross_chain_transactions_repo.get_session() as session:
                # Merge CreatedOrder with BlockchainTransaction by transaction_hash
                results = (
                    session.query(
                        SrcTx.blockchain.label("src_blockchain"),
                        SrcTx.transaction_hash.label("src_transaction_hash"),
                        SrcTx.from_address.label("src_from_address"),
                        SrcTx.to_address.label("src_to_address"),
                        SrcTx.fee.label("src_fee"),
                        literal(None).label("src_fee_usd"),
                        SrcTx.value.label("src_value"),
                        SrcTx.timestamp.label("src_timestamp"),
                        DstTx.blockchain.label("dst_blockchain"),
                        DstTx.transaction_hash.label("dst_transaction_hash"),
                        case(
                            (DstTx.blockchain == "solana", DeBridgeFulfilledOrder.taker),  # noqa: E711 DO NOT REPLACE != WITH 'IS NOT'
                            else_=DstTx.from_address,
                        ).label("dst_from_address"),
                        case(
                            (
                                DstTx.blockchain == "solana",
                                "dst5MGcFPoBeREFAA5E3tU5ij8m5uVYwkzkSAbsLbNo",
                            ),  # noqa: E711 DO NOT REPLACE != WITH 'IS NOT'
                            else_=DstTx.to_address,
                        ).label("dst_to_address"),
                        DstTx.fee.label("dst_fee"),
                        literal(None).label("dst_fee_usd"),
                        DstTx.value.label("dst_value"),
                        DstTx.timestamp.label("dst_timestamp"),
                        RefundTx.blockchain.label("refund_blockchain"),
                        RefundTx.transaction_hash.label("refund_transaction_hash"),
                        RefundTx.from_address.label("refund_from_address"),
                        RefundTx.to_address.label("refund_to_address"),
                        RefundTx.fee.label("refund_fee"),
                        literal(None).label("refund_fee_usd"),
                        RefundTx.value.label("refund_value"),
                        RefundTx.timestamp.label("refund_timestamp"),
                        DeBridgeCreatedOrder.order_id.label("intent_id"),
                        DeBridgeCreatedOrder.maker_src.label("depositor"),
                        DeBridgeFulfilledOrder.receiver_dst.label("recipient"),
                        DeBridgeFulfilledOrder.give_token_address.label("src_contract_address"),
                        DeBridgeFulfilledOrder.take_token_address.label("dst_contract_address"),
                        DeBridgeCreatedOrder.original_amount.label("input_amount"),
                        literal(None).label("input_amount_usd"),
                        DeBridgeCreatedOrder.give_token_address.label("middle_src_token"),
                        DeBridgeCreatedOrder.give_amount.label("middle_src_amount"),
                        literal(None).label("middle_src_amount_usd"),
                        DeBridgeFulfilledOrder.middle_dst_token.label("middle_dst_token"),
                        DeBridgeFulfilledOrder.middle_dst_amount.label("middle_dst_amount"),
                        literal(None).label("middle_dst_amount_usd"),
                        DeBridgeFulfilledOrder.take_amount.label("output_amount"),
                        literal(None).label("output_amount_usd"),
                        DeBridgeClaimedUnlock.give_amount.label("refund_amount"),
                        literal(None).label("refund_amount_usd"),
                        DeBridgeClaimedUnlock.give_token_address.label("refund_token"),
                        DeBridgeCreatedOrder.native_fix_fee.label("native_fix_fee"),
                        literal(None).label("native_fix_fee_usd"),
                        DeBridgeCreatedOrder.percent_fee.label("percent_fee"),
                        literal(None).label("percent_fee_usd"),
                    )
                    .join(SrcTx, DeBridgeCreatedOrder.transaction_hash == SrcTx.transaction_hash)
                    .join(
                        DeBridgeFulfilledOrder,
                        DeBridgeCreatedOrder.order_id == DeBridgeFulfilledOrder.order_id,
                    )
                    .join(DstTx, DeBridgeFulfilledOrder.transaction_hash == DstTx.transaction_hash)
                    .outerjoin(
                        DeBridgeClaimedUnlock,
                        DeBridgeCreatedOrder.order_id == DeBridgeClaimedUnlock.order_id,
                    )
                    .outerjoin(
                        RefundTx,
                        DeBridgeClaimedUnlock.transaction_hash == RefundTx.transaction_hash,
                    )
                    .filter(SrcTx.blockchain != "solana")
                    .all()
                )

                cctxs = []

                for row in results:
                    cctxs.append(row._asdict())

                self.debridge_cross_chain_transactions_repo.create_all(cctxs)

            size = self.debridge_cross_chain_transactions_repo.get_number_of_records()

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

    def match_sol_to_evm_cctxs(self):
        func_name = "match_sol_to_evm_cctxs"

        start_time = time.time()
        log_to_cli(
            build_log_message_generator(
                self.bridge, "Matching deBridge SOL -> EVM token transfers..."
            )
        )

        try:
            results = []

            SrcTx = aliased(DeBridgeBlockchainTransaction)
            DstTx = aliased(DeBridgeBlockchainTransaction)
            RefundTx = aliased(DeBridgeBlockchainTransaction)

            with self.debridge_cross_chain_transactions_repo.get_session() as session:
                results = (
                    session.query(
                        SrcTx.blockchain.label("src_blockchain"),
                        SrcTx.transaction_hash.label("src_transaction_hash"),
                        DeBridgeCreatedOrder.maker_src.label("src_from_address"),
                        literal("src5qyZHqTqecJV4aY6Cb6zDZLMDzrDKKezs22MPHr4").label(
                            "src_to_address"
                        ),
                        SrcTx.fee.label("src_fee"),
                        literal(None).label("src_fee_usd"),
                        SrcTx.value.label("src_value"),
                        SrcTx.timestamp.label("src_timestamp"),
                        DstTx.blockchain.label("dst_blockchain"),
                        DstTx.transaction_hash.label("dst_transaction_hash"),
                        DstTx.from_address.label("dst_from_address"),
                        DstTx.to_address.label("dst_to_address"),
                        DstTx.fee.label("dst_fee"),
                        literal(None).label("dst_fee_usd"),
                        DstTx.value.label("dst_value"),
                        DstTx.timestamp.label("dst_timestamp"),
                        RefundTx.blockchain.label("refund_blockchain"),
                        RefundTx.transaction_hash.label("refund_transaction_hash"),
                        RefundTx.from_address.label("refund_from_address"),
                        RefundTx.to_address.label("refund_to_address"),
                        RefundTx.fee.label("refund_fee"),
                        literal(None).label("refund_fee_usd"),
                        RefundTx.value.label("refund_value"),
                        RefundTx.timestamp.label("refund_timestamp"),
                        DeBridgeFulfilledOrder.order_id.label("intent_id"),
                        DeBridgeCreatedOrder.maker_src.label("depositor"),
                        DeBridgeCreatedOrder.receiver_dst.label("recipient"),
                        DeBridgeCreatedOrder.give_token_address.label("src_contract_address"),
                        DeBridgeCreatedOrder.take_token_address.label("dst_contract_address"),
                        DeBridgeCreatedOrder.original_amount.label("input_amount"),
                        literal(None).label("input_amount_usd"),
                        DeBridgeCreatedOrder.give_token_address.label("middle_src_token"),
                        DeBridgeCreatedOrder.give_amount.label("middle_src_amount"),
                        literal(None).label("middle_src_amount_usd"),
                        DeBridgeFulfilledOrder.middle_dst_token.label("middle_dst_token"),
                        DeBridgeFulfilledOrder.middle_dst_amount.label("middle_dst_amount"),
                        literal(None).label("middle_dst_amount_usd"),
                        DeBridgeFulfilledOrder.take_amount.label("output_amount"),
                        literal(None).label("output_amount_usd"),
                        DeBridgeClaimedUnlock.give_amount.label("refund_amount"),
                        literal(None).label("refund_amount_usd"),
                        DeBridgeClaimedUnlock.give_token_address.label("refund_token"),
                        DeBridgeCreatedOrder.native_fix_fee.label("native_fix_fee"),
                        literal(None).label("native_fix_fee_usd"),
                        case(
                            (
                                SrcTx.blockchain == "solana",
                                literal(0),
                            ),
                            else_=DeBridgeCreatedOrder.percent_fee,
                        ).label("percent_fee"),
                        literal(None).label("percent_fee_usd"),
                    )
                    .join(SrcTx, DeBridgeCreatedOrder.transaction_hash == SrcTx.transaction_hash)
                    .join(
                        DeBridgeFulfilledOrder,
                        DeBridgeCreatedOrder.maker_order_nonce
                        == DeBridgeFulfilledOrder.maker_order_nonce,
                    )
                    .join(DstTx, DeBridgeFulfilledOrder.transaction_hash == DstTx.transaction_hash)
                    .outerjoin(
                        DeBridgeClaimedUnlock,
                        DeBridgeFulfilledOrder.order_id == DeBridgeClaimedUnlock.order_id,
                    )
                    .outerjoin(
                        RefundTx,
                        DeBridgeClaimedUnlock.transaction_hash == RefundTx.transaction_hash,
                    )
                    .filter(SrcTx.blockchain == "solana")
                    .all()
                )

                cctxs = []

                for row in results:
                    cctxs.append(row._asdict())

                self.debridge_cross_chain_transactions_repo.create_all(cctxs)

            size = self.debridge_cross_chain_transactions_repo.get_number_of_records()

            end_time = time.time()
            log_to_cli(
                build_log_message_generator(
                    self.bridge,
                    (
                        f"SOL -> EVM token transfers matched in {end_time - start_time} seconds. "
                        f"Total records inserted: {size}",
                    ),
                ),
                CliColor.SUCCESS,
            )
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"Error processing SOL -> EVM token transfers. Error: {e}",
            ) from e

    def fill_null_address_tokens(self):
        """
        DeBridge uses the null address (0x0000000000000000000000000000000000000000) when
        transferring the native tokens in give_token_address and take_token_address.
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

    def fetch_solana_data(self, start_ts, end_ts):
        if not self.native_token_repo.get_native_token_by_blockchain("solana"):
            self.native_token_repo.create(
                {
                    "symbol": "SOL",
                    "blockchain": "solana",
                }
            )

        if not self.token_metadata_repo.get_token_metadata_by_symbol("SOL"):
            self.token_metadata_repo.create(
                {
                    "symbol": "SOL",
                    "name": "Wrapped Solana",
                    "decimals": 9,
                    "blockchain": "solana",
                    "address": "11111111111111111111111111111111",
                }
            )

            self.token_metadata_repo.create(
                {
                    "symbol": "SOL",
                    "name": "Wrapped Solana",
                    "decimals": 9,
                    "blockchain": "solana",
                    "address": "0x0000000000000000000000000000000000000000",
                }
            )

        # When the native token is used in the destination blockchain,
        # the address is set to 0x0000000000000000000000000000000000000000
        # however, if we fetch info from Alchemy, we will not get the
        # token metadata for the native token, so we need to fill it manually
        # with the data we have in the NativeToken table and the TokenMetadata table

        if not self.token_metadata_repo.get_token_metadata_by_symbol_and_blockchain(
            "WETH", "solana"
        ):
            self.token_metadata_repo.create(
                {
                    "symbol": "WETH",
                    "name": "Wrapped Ether",
                    "decimals": 8,
                    "blockchain": "solana",
                    "address": "7vfCXTUXx5WJV5JADk17DUJ4ksgau7utNKj4b963voxs",
                }
            )

        if not self.token_metadata_repo.get_token_metadata_by_symbol_and_blockchain(
            "USDC", "solana"
        ):
            self.token_metadata_repo.create(
                {
                    "symbol": "USDC",
                    "name": "USDC",
                    "decimals": 6,
                    "blockchain": "solana",
                    "address": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
                }
            )

        if not PriceGenerator.is_token_price_complete(
            self.token_price_repo,
            start_ts,
            end_ts,
            "SOL",
            "solana",
        ):
            PriceGenerator.fetch_and_store_token_prices(
                self.bridge,
                self.token_price_repo,
                start_ts,
                end_ts,
                "Solana",
                "SOL",
            )

        # We found an erros in the Alchemy API where it returns the wrong
        # decimals for the DONKEY token in BNB, so we need to fix it manually
        with self.token_metadata_repo.get_session() as session:
            stmt = (
                update(TokenMetadata)
                .values(decimals=18)
                .where(
                    TokenMetadata.blockchain == "bnb",
                    TokenMetadata.symbol == "DONKEY",
                    TokenMetadata.address == "0xA49fA5E8106E2d6d6a69E78df9B6A20AaB9c4444",
                )
                .execution_options(synchronize_session=False)
            )
            session.execute(stmt)
