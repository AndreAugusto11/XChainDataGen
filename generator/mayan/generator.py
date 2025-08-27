import time

from sqlalchemy import case, func, literal, literal_column, update
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
from repository.mayan.models import (
    MayanAuctionBid,
    MayanBlockchainTransaction,
    MayanCrossChainTransaction,
    MayanForwarded,
    MayanFulfillOrder,
    MayanInitOrder,
    MayanOrderCreated,
    MayanOrderFulfilled,
    MayanOrderUnlocked,
    MayanRegisterOrder,
    MayanSwapAndForwarded,
    MayanUnlock,
)
from repository.mayan.repository import (
    MayanBlockchainTransactionRepository,
    MayanCrossChainTransactionRepository,
)
from utils.utils import (
    CliColor,
    CustomException,
    build_log_message_generator,
    log_error,
    log_to_cli,
)


class MayanGenerator(BaseGenerator):
    CLASS_NAME = "MayanGenerator"

    def __init__(self) -> None:
        super().__init__()
        self.bridge = Bridge.MAYAN
        self.price_generator = PriceGenerator()

    def bind_db_to_repos(self):
        self.transactions_repo = MayanBlockchainTransactionRepository(DBSession)

        self.cross_chain_transactions_repo = MayanCrossChainTransactionRepository(DBSession)

        self.token_metadata_repo = TokenMetadataRepository(DBSession)
        self.token_price_repo = TokenPriceRepository(DBSession)
        self.native_token_repo = NativeTokenRepository(DBSession)

    def generate_cross_chain_data(self):
        func_name = "create_cross_chain_transactions"

        try:
            self.match_sol_to_evm()
            self.match_evm_to_sol()
            self.match_evm_to_evm()

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

            # The Solana blockchain is not supported by the Alchemy API, so we need to make some
            # additions to the database manually
            self.fetch_solana_data(start_ts, end_ts)

            cctxs = self.cross_chain_transactions_repo.get_unique_src_dst_contract_pairs()
            self.populate_token_info_tables(cctxs, start_ts, end_ts)

            PriceGenerator.calculate_cctx_usd_values(
                self.bridge,
                self.cross_chain_transactions_repo,
                "mayan_cross_chain_transactions",
                "input_amount",
                "src_blockchain",
                "src_contract_address",
                "src_timestamp",
                "input_amount_usd",
            )
            PriceGenerator.calculate_cctx_usd_values(
                self.bridge,
                self.cross_chain_transactions_repo,
                "mayan_cross_chain_transactions",
                "output_amount",
                "dst_blockchain",
                "dst_contract_address",
                "dst_timestamp",
                "output_amount_usd",
            )
            PriceGenerator.calculate_cctx_usd_values(
                self.bridge,
                self.cross_chain_transactions_repo,
                "mayan_cross_chain_transactions",
                "refund_amount",
                "src_blockchain",
                "src_contract_address",
                "src_timestamp",
                "refund_amount_usd",
            )
            PriceGenerator.calculate_cctx_usd_values(
                self.bridge,
                self.cross_chain_transactions_repo,
                "mayan_cross_chain_transactions",
                "middle_src_amount",
                "src_blockchain",
                "middle_src_token",
                "src_timestamp",
                "middle_src_amount_usd",
            )
            PriceGenerator.calculate_cctx_usd_values(
                self.bridge,
                self.cross_chain_transactions_repo,
                "mayan_cross_chain_transactions",
                "middle_dst_amount",
                "dst_blockchain",
                "middle_dst_token",
                "dst_timestamp",
                "middle_dst_amount_usd",
            )
            PriceGenerator.calculate_cctx_usd_values(
                self.bridge,
                self.cross_chain_transactions_repo,
                "mayan_cross_chain_transactions",
                "percent_fee",
                "dst_blockchain",
                "dst_contract_address",
                "dst_timestamp",
                "percent_fee_usd",
            )

            PriceGenerator.calculate_cctx_native_usd_values(
                self.bridge,
                self.cross_chain_transactions_repo,
                "mayan_cross_chain_transactions",
                "src_timestamp",
                "src_blockchain",
                "src_fee",
                "src_fee_usd",
            )
            PriceGenerator.calculate_cctx_native_usd_values(
                self.bridge,
                self.cross_chain_transactions_repo,
                "mayan_cross_chain_transactions",
                "dst_timestamp",
                "dst_blockchain",
                "dst_fee",
                "dst_fee_usd",
            )
            PriceGenerator.calculate_cctx_native_usd_values(
                self.bridge,
                self.cross_chain_transactions_repo,
                "mayan_cross_chain_transactions",
                "refund_timestamp",
                "refund_blockchain",
                "refund_fee",
                "refund_fee_usd",
            )

            self.fix_token_symbol_clashes()

        except Exception as e:
            exception = CustomException(
                self.CLASS_NAME,
                func_name,
                f"Error processing cross chain transactions. Error: {e}",
            )
            log_error(self.bridge, exception)

    def match_sol_to_evm(self):
        func_name = "match_sol_to_evm"

        start_time = time.time()
        log_to_cli(
            build_log_message_generator(self.bridge, "Matching cross-chain SOL -> EVM transfers...")
        )

        self.cross_chain_transactions_repo.empty_table()

        try:
            results = []

            auction_data = self.get_auction_data()

            SrcTx = aliased(MayanBlockchainTransaction)
            DstTx = aliased(MayanBlockchainTransaction)
            RefundTx = aliased(MayanBlockchainTransaction)

            with self.cross_chain_transactions_repo.get_session() as session:
                results = (
                    session.query(
                        MayanInitOrder.trader.label("src_from_address"),
                        MayanInitOrder.trader.label("depositor"),
                        MayanInitOrder.addr_dest.label("recipient"),
                        MayanInitOrder.order_hash.label("order_hash"),
                        MayanInitOrder.token_out.label("token_out"),
                        MayanInitOrder.original_src_token.label("original_src_token"),
                        MayanInitOrder.original_src_amount.label("original_src_amount"),
                        MayanInitOrder.middle_src_token.label("middle_src_token"),
                        MayanInitOrder.middle_src_amount.label("middle_src_amount"),
                        MayanOrderFulfilled.net_amount.label("output_amount"),
                        MayanOrderFulfilled.middle_dst_token.label("middle_dst_token"),
                        MayanOrderFulfilled.middle_dst_amount.label("middle_dst_amount"),
                        MayanUnlock.signature.label("refund_transaction_hash"),
                        MayanUnlock.driver_acc.label("refund_from_address"),
                        MayanUnlock.amount.label("refund_amount"),
                        MayanUnlock.mint_from.label("refund_token"),
                        SrcTx.blockchain.label("src_blockchain"),
                        SrcTx.transaction_hash.label("src_transaction_hash"),
                        SrcTx.fee.label("src_fee"),
                        SrcTx.value.label("src_value"),
                        SrcTx.timestamp.label("src_timestamp"),
                        DstTx.transaction_hash.label("dst_transaction_hash"),
                        DstTx.blockchain.label("dst_blockchain"),
                        DstTx.from_address.label("dst_from_address"),
                        DstTx.to_address.label("dst_to_address"),
                        DstTx.fee.label("dst_fee"),
                        DstTx.value.label("dst_value"),
                        DstTx.timestamp.label("dst_timestamp"),
                        RefundTx.blockchain.label("refund_blockchain"),
                        RefundTx.fee.label("refund_fee"),
                        RefundTx.value.label("refund_value"),
                        RefundTx.timestamp.label("refund_timestamp"),
                        auction_data.c.auction_id.label("auction_id"),
                        auction_data.c.auction_first_bid_timestamp.label(
                            "auction_first_bid_timestamp"
                        ),
                        auction_data.c.auction_last_bid_timestamp.label(
                            "auction_last_bid_timestamp"
                        ),
                        auction_data.c.auction_number_of_bids.label("auction_number_of_bids"),
                        literal(0).label("native_fix_fee"),
                        (
                            MayanOrderFulfilled.net_amount * 0.000300090027 / (1 - 0.000300090027)
                        ).label("percent_fee"),
                    )
                    .join(MayanOrderFulfilled, MayanInitOrder.order_hash == MayanOrderFulfilled.key)
                    .join(SrcTx, SrcTx.transaction_hash == MayanInitOrder.signature)
                    .join(DstTx, DstTx.transaction_hash == MayanOrderFulfilled.transaction_hash)
                    .outerjoin(MayanUnlock, MayanInitOrder.state == MayanUnlock.state)
                    .outerjoin(RefundTx, RefundTx.transaction_hash == MayanUnlock.signature)
                    .outerjoin(
                        auction_data,
                        auction_data.c.order_hash == MayanInitOrder.order_hash,
                    )
                    .all()
                )

            cctxs = []

            for row in results:
                cctxs.append(
                    MayanCrossChainTransaction(
                        src_blockchain=row.src_blockchain,
                        src_transaction_hash=row.src_transaction_hash,
                        src_from_address=row.src_from_address,
                        src_to_address="BLZRi6frs4X4DNLw56V4EXai1b6QVESN1BhHBTYM9VcY",
                        src_fee=row.src_fee,
                        src_value=row.src_value,
                        src_fee_usd=None,
                        src_timestamp=row.src_timestamp,
                        dst_blockchain=row.dst_blockchain,
                        dst_transaction_hash=row.dst_transaction_hash,
                        dst_from_address=row.dst_from_address,
                        dst_to_address=row.dst_to_address,
                        dst_fee=row.dst_fee,
                        dst_value=row.dst_value,
                        dst_fee_usd=None,
                        dst_timestamp=row.dst_timestamp,
                        refund_blockchain=row.refund_blockchain,
                        refund_transaction_hash=row.refund_transaction_hash,
                        refund_from_address=row.refund_from_address,
                        refund_to_address="9w1D9okTM8xNE7Ntb7LpaAaoLc6LfU9nHFs2h2KTpX1H",
                        refund_fee=row.refund_fee,
                        refund_value=row.refund_value,
                        refund_fee_usd=None,
                        refund_timestamp=row.refund_timestamp,
                        intent_id=row.order_hash,
                        depositor=row.depositor,
                        recipient=row.recipient,
                        src_contract_address=row.original_src_token,
                        dst_contract_address=row.token_out,
                        input_amount=row.original_src_amount,
                        input_amount_usd=None,
                        middle_src_token=row.middle_src_token,
                        middle_src_amount=row.middle_src_amount,
                        middle_src_amount_usd=None,
                        middle_dst_token=row.middle_dst_token,
                        middle_dst_amount=row.middle_dst_amount,
                        middle_dst_amount_usd=None,
                        output_amount=row.output_amount,
                        output_amount_usd=None,
                        refund_amount=row.refund_amount,
                        refund_amount_usd=None,
                        refund_token=row.refund_token,
                        auction_id=row.auction_id,
                        auction_first_bid_timestamp=row.auction_first_bid_timestamp,
                        auction_last_bid_timestamp=row.auction_last_bid_timestamp,
                        auction_number_of_bids=row.auction_number_of_bids,
                        native_fix_fee=row.native_fix_fee,
                        native_fix_fee_usd=None,
                        percent_fee=row.percent_fee,
                        percent_fee_usd=None,
                    )
                )

            self.cross_chain_transactions_repo.create_all(cctxs)

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

    def match_evm_to_sol(self):
        func_name = "match_evm_to_sol"

        start_time = time.time()
        log_to_cli(
            build_log_message_generator(self.bridge, "Matching cross-chain EVM -> SOL transfers...")
        )

        try:
            results = []

            auction_data = self.get_auction_data()

            SrcTx = aliased(MayanBlockchainTransaction)
            DstTx = aliased(MayanBlockchainTransaction)
            RefundTx = aliased(MayanBlockchainTransaction)

            with self.cross_chain_transactions_repo.get_session() as session:
                forwarded_query = session.query(
                    MayanForwarded.blockchain.label("blockchain"),
                    MayanForwarded.transaction_hash.label("transaction_hash"),
                    MayanForwarded.trader.label("trader"),
                    MayanForwarded.token.label("token"),
                    MayanForwarded.token_out.label("token_out"),
                    MayanForwarded.dst_addr.label("dst_addr"),
                    MayanForwarded.amount.label("amount"),
                    literal(None).label("middle_src_token"),
                    literal(None).label("middle_src_amount"),
                    literal_column("'forwarded'").label("entry_type"),
                )

                # Select swap_and_forwarded entries
                swap_and_forwarded_query = session.query(
                    MayanSwapAndForwarded.blockchain.label("blockchain"),
                    MayanSwapAndForwarded.transaction_hash.label("transaction_hash"),
                    MayanSwapAndForwarded.trader.label("trader"),
                    MayanSwapAndForwarded.token_in.label("token"),
                    MayanSwapAndForwarded.token_out.label("token_out"),
                    MayanSwapAndForwarded.dst_addr.label("dst_addr"),
                    MayanSwapAndForwarded.amount_in.label("amount"),
                    MayanSwapAndForwarded.middle_token.label("middle_src_token"),
                    MayanSwapAndForwarded.middle_amount.label("middle_src_amount"),
                    literal_column("'swap_and_forwarded'").label("entry_type"),
                )

                # Create a union of both
                forward_union = forwarded_query.union_all(swap_and_forwarded_query).subquery()
                Fwd = aliased(forward_union)

                results = (
                    session.query(
                        Fwd.c.blockchain.label("src_blockchain"),
                        Fwd.c.transaction_hash.label("src_transaction_hash"),
                        SrcTx.from_address.label("src_from_address"),
                        SrcTx.to_address.label("src_to_address"),
                        SrcTx.fee.label("src_fee"),
                        SrcTx.value.label("src_value"),
                        SrcTx.timestamp.label("src_timestamp"),
                        MayanFulfillOrder.signature.label("dst_transaction_hash"),
                        MayanFulfillOrder.driver.label("dst_from_address"),
                        MayanFulfillOrder.dest.label("dst_to_address"),
                        MayanFulfillOrder.middle_dst_token.label("middle_dst_token"),
                        MayanFulfillOrder.middle_dst_amount.label("middle_dst_amount"),
                        DstTx.fee.label("dst_fee"),
                        DstTx.value.label("dst_value"),
                        DstTx.timestamp.label("dst_timestamp"),
                        RefundTx.blockchain.label("refund_blockchain"),
                        RefundTx.transaction_hash.label("refund_transaction_hash"),
                        RefundTx.from_address.label("refund_from_address"),
                        RefundTx.to_address.label("refund_to_address"),
                        RefundTx.fee.label("refund_fee"),
                        RefundTx.value.label("refund_value"),
                        RefundTx.timestamp.label("refund_timestamp"),
                        MayanOrderCreated.key.label("intent_id"),
                        Fwd.c.trader.label("depositor"),
                        MayanRegisterOrder.addr_dest.label("recipient"),
                        Fwd.c.token.label("src_contract_address"),
                        MayanRegisterOrder.token_out.label("dst_contract_address"),
                        case(
                            (Fwd.c.amount != None, Fwd.c.amount),  # noqa: E711 DO NOT REPLACE != WITH 'IS NOT'
                            else_=SrcTx.value,
                        ).label("input_amount"),
                        MayanFulfillOrder.amount.label("output_amount"),
                        auction_data.c.auction_id.label("auction_id"),
                        auction_data.c.auction_first_bid_timestamp.label(
                            "auction_first_bid_timestamp"
                        ),
                        auction_data.c.auction_last_bid_timestamp.label(
                            "auction_last_bid_timestamp"
                        ),
                        auction_data.c.auction_number_of_bids.label("auction_number_of_bids"),
                        Fwd.c.middle_src_token.label("middle_src_token"),
                        Fwd.c.middle_src_amount.label("middle_src_amount"),
                        literal(0).label("native_fix_fee"),
                        literal(0).label("percent_fee"),
                    )
                    .join(
                        MayanOrderCreated,
                        MayanOrderCreated.transaction_hash == Fwd.c.transaction_hash,
                    )
                    .join(
                        MayanRegisterOrder, MayanRegisterOrder.order_hash == MayanOrderCreated.key
                    )
                    .join(MayanFulfillOrder, MayanFulfillOrder.state == MayanRegisterOrder.state)
                    .join(SrcTx, SrcTx.transaction_hash == Fwd.c.transaction_hash)
                    .join(DstTx, DstTx.transaction_hash == MayanFulfillOrder.signature)
                    .outerjoin(MayanOrderUnlocked, MayanOrderUnlocked.key == MayanOrderCreated.key)
                    .outerjoin(
                        RefundTx, RefundTx.transaction_hash == MayanOrderUnlocked.transaction_hash
                    )
                    .outerjoin(
                        auction_data,
                        auction_data.c.order_hash == MayanRegisterOrder.order_hash,
                    )
                )

            cctxs = []

            for row in results:
                cctxs.append(
                    MayanCrossChainTransaction(
                        src_blockchain=row.src_blockchain,
                        src_transaction_hash=row.src_transaction_hash,
                        src_from_address=row.src_from_address,
                        src_to_address=row.src_to_address,
                        src_fee=row.src_fee,
                        src_value=row.src_value,
                        src_fee_usd=None,
                        src_timestamp=row.src_timestamp,
                        dst_blockchain="solana",
                        dst_transaction_hash=row.dst_transaction_hash,
                        dst_from_address=row.dst_from_address,
                        dst_to_address=row.dst_to_address,
                        dst_fee=row.dst_fee,
                        dst_value=row.dst_value,
                        dst_fee_usd=None,
                        dst_timestamp=row.dst_timestamp,
                        refund_blockchain=row.refund_blockchain,
                        refund_transaction_hash=row.refund_transaction_hash,
                        refund_from_address=row.refund_from_address,
                        refund_to_address=row.refund_to_address,
                        refund_fee=row.refund_fee,
                        refund_value=row.refund_value,
                        refund_fee_usd=None,
                        refund_timestamp=row.refund_timestamp,
                        intent_id=row.intent_id,
                        depositor=row.depositor,
                        recipient=row.recipient,
                        src_contract_address=row.src_contract_address,
                        dst_contract_address=row.dst_contract_address,
                        input_amount=row.input_amount,
                        input_amount_usd=None,
                        middle_src_token=row.middle_src_token,
                        middle_src_amount=row.middle_src_amount,
                        middle_src_amount_usd=None,
                        middle_dst_token=row.middle_dst_token,
                        middle_dst_amount=row.middle_dst_amount,
                        middle_dst_amount_usd=None,
                        output_amount=row.output_amount,
                        output_amount_usd=None,
                        refund_amount=row.input_amount,  # in the case of usage of intermediary
                        # protocols, the refund amount is a bit less than the input amount (because
                        # of fees), but there is not way to get the exact refund amount unless we
                        # parse internal transactions and match to the unlock events.
                        refund_amount_usd=None,
                        refund_token="0x0000000000000000000000000000000000000000",
                        auction_id=row.auction_id,
                        auction_first_bid_timestamp=row.auction_first_bid_timestamp,
                        auction_last_bid_timestamp=row.auction_last_bid_timestamp,
                        auction_number_of_bids=row.auction_number_of_bids,
                        native_fix_fee=row.native_fix_fee,
                        native_fix_fee_usd=None,
                        percent_fee=row.percent_fee,
                        percent_fee_usd=None,
                    )
                )

            self.cross_chain_transactions_repo.create_all(cctxs)

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

    def match_evm_to_evm(self):
        func_name = "match_evm_to_evm"

        start_time = time.time()
        log_to_cli(
            build_log_message_generator(self.bridge, "Matching cross-chain EVM -> EVM transfers...")
        )

        try:
            results = []

            auction_data = self.get_auction_data()

            SrcTx = aliased(MayanBlockchainTransaction)
            DstTx = aliased(MayanBlockchainTransaction)
            RefundTx = aliased(MayanBlockchainTransaction)

            with self.cross_chain_transactions_repo.get_session() as session:
                forwarded_query = session.query(
                    MayanForwarded.blockchain.label("blockchain"),
                    MayanForwarded.transaction_hash.label("transaction_hash"),
                    MayanForwarded.trader.label("trader"),
                    MayanForwarded.token.label("token"),
                    MayanForwarded.token_out.label("token_out"),
                    MayanForwarded.dst_addr.label("dst_addr"),
                    MayanForwarded.amount.label("amount"),
                    literal(None).label("middle_src_token"),
                    literal(None).label("middle_src_amount"),
                    literal_column("'forwarded'").label("entry_type"),
                )

                swap_and_forwarded_query = session.query(
                    MayanSwapAndForwarded.blockchain.label("blockchain"),
                    MayanSwapAndForwarded.transaction_hash.label("transaction_hash"),
                    MayanSwapAndForwarded.trader.label("trader"),
                    MayanSwapAndForwarded.token_in.label("token"),
                    MayanSwapAndForwarded.token_out.label("token_out"),
                    MayanSwapAndForwarded.dst_addr.label("dst_addr"),
                    MayanSwapAndForwarded.amount_in.label("amount"),
                    MayanSwapAndForwarded.middle_token.label("middle_src_token"),
                    MayanSwapAndForwarded.middle_amount.label("middle_src_amount"),
                    literal_column("'swap_and_forwarded'").label("entry_type"),
                )

                forward_union = forwarded_query.union_all(swap_and_forwarded_query).subquery()
                Fwd = aliased(forward_union)

                SrcTx = aliased(MayanBlockchainTransaction)
                DstTx = aliased(MayanBlockchainTransaction)
                RefundTx = aliased(MayanBlockchainTransaction)

                results = (
                    session.query(
                        Fwd.c.blockchain.label("src_blockchain"),
                        Fwd.c.transaction_hash.label("src_transaction_hash"),
                        SrcTx.from_address.label("src_from_address"),
                        SrcTx.to_address.label("src_to_address"),
                        SrcTx.fee.label("src_fee"),
                        SrcTx.value.label("src_value"),
                        SrcTx.timestamp.label("src_timestamp"),
                        MayanOrderFulfilled.transaction_hash.label("dst_transaction_hash"),
                        MayanOrderFulfilled.blockchain.label("dst_blockchain"),
                        MayanOrderFulfilled.net_amount.label("output_amount"),
                        MayanOrderFulfilled.middle_dst_token.label("middle_dst_token"),
                        MayanOrderFulfilled.middle_dst_amount.label("middle_dst_amount"),
                        DstTx.from_address.label("dst_from_address"),
                        DstTx.to_address.label("dst_to_address"),
                        DstTx.fee.label("dst_fee"),
                        DstTx.value.label("dst_value"),
                        DstTx.timestamp.label("dst_timestamp"),
                        MayanOrderUnlocked.blockchain.label("refund_blockchain"),
                        MayanOrderUnlocked.transaction_hash.label("refund_transaction_hash"),
                        RefundTx.from_address.label("refund_from_address"),
                        RefundTx.to_address.label("refund_to_address"),
                        RefundTx.fee.label("refund_fee"),
                        RefundTx.value.label("refund_value"),
                        RefundTx.timestamp.label("refund_timestamp"),
                        MayanOrderCreated.key.label("intent_id"),
                        Fwd.c.trader.label("depositor"),
                        Fwd.c.dst_addr.label("recipient"),
                        Fwd.c.token.label("src_contract_address"),
                        Fwd.c.token_out.label("dst_contract_address"),
                        Fwd.c.middle_src_token.label("middle_src_token"),
                        Fwd.c.middle_src_amount.label("middle_src_amount"),
                        case(
                            (Fwd.c.amount != None, Fwd.c.amount),  # noqa: E711 DO NOT REPLACE != WITH 'IS NOT'
                            else_=SrcTx.value,
                        ).label("input_amount"),
                        auction_data.c.auction_id.label("auction_id"),
                        auction_data.c.auction_first_bid_timestamp.label(
                            "auction_first_bid_timestamp"
                        ),
                        auction_data.c.auction_last_bid_timestamp.label(
                            "auction_last_bid_timestamp"
                        ),
                        auction_data.c.auction_number_of_bids.label("auction_number_of_bids"),
                        literal(0).label("native_fix_fee"),
                        (
                            MayanOrderFulfilled.net_amount * 0.000300090027 / (1 - 0.000300090027)
                        ).label("percent_fee"),
                    )
                    .join(
                        MayanOrderCreated,
                        MayanOrderCreated.transaction_hash == Fwd.c.transaction_hash,
                    )
                    .join(MayanOrderFulfilled, MayanOrderFulfilled.key == MayanOrderCreated.key)
                    .join(SrcTx, SrcTx.transaction_hash == Fwd.c.transaction_hash)
                    .join(DstTx, DstTx.transaction_hash == MayanOrderFulfilled.transaction_hash)
                    .outerjoin(MayanOrderUnlocked, MayanOrderCreated.key == MayanOrderUnlocked.key)
                    .outerjoin(
                        RefundTx, RefundTx.transaction_hash == MayanOrderUnlocked.transaction_hash
                    )
                    .outerjoin(
                        auction_data,
                        auction_data.c.order_hash == MayanOrderFulfilled.key,
                    )
                    .all()
                )

            cctxs = []

            for row in results:
                cctxs.append(
                    MayanCrossChainTransaction(
                        src_blockchain=row.src_blockchain,
                        src_transaction_hash=row.src_transaction_hash,
                        src_from_address=row.src_from_address,
                        src_to_address=row.src_to_address,
                        src_fee=row.src_fee,
                        src_value=row.src_value,
                        src_fee_usd=None,
                        src_timestamp=row.src_timestamp,
                        dst_blockchain=row.dst_blockchain,
                        dst_transaction_hash=row.dst_transaction_hash,
                        dst_from_address=row.dst_from_address,
                        dst_to_address=row.dst_to_address,
                        dst_fee=row.dst_fee,
                        dst_value=row.dst_value,
                        dst_fee_usd=None,
                        dst_timestamp=row.dst_timestamp,
                        refund_blockchain=row.refund_blockchain,
                        refund_transaction_hash=row.refund_transaction_hash,
                        refund_from_address=row.refund_from_address,
                        refund_to_address=row.refund_to_address,
                        refund_fee=row.refund_fee,
                        refund_value=row.refund_value,
                        refund_fee_usd=None,
                        refund_timestamp=row.refund_timestamp,
                        intent_id=row.intent_id,
                        depositor=row.depositor,
                        recipient=row.recipient,
                        src_contract_address=row.src_contract_address,
                        dst_contract_address=row.dst_contract_address,
                        input_amount=row.input_amount,
                        input_amount_usd=None,
                        middle_src_token=row.middle_src_token,
                        middle_src_amount=row.middle_src_amount,
                        middle_src_amount_usd=None,
                        middle_dst_token=row.middle_dst_token,
                        middle_dst_amount=row.middle_dst_amount,
                        middle_dst_amount_usd=None,
                        output_amount=row.output_amount,
                        output_amount_usd=None,
                        refund_amount=row.input_amount,
                        refund_amount_usd=None,
                        refund_token="0x0000000000000000000000000000000000000000",
                        auction_id=row.auction_id,
                        auction_first_bid_timestamp=row.auction_first_bid_timestamp,
                        auction_last_bid_timestamp=row.auction_last_bid_timestamp,
                        auction_number_of_bids=row.auction_number_of_bids,
                        native_fix_fee=row.native_fix_fee,
                        native_fix_fee_usd=None,
                        percent_fee=row.percent_fee,
                        percent_fee_usd=None,
                    )
                )

            self.cross_chain_transactions_repo.create_all(cctxs)

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

    def get_auction_data(self):
        """
        Returns a subquery to gather the auction data (id, open timestamp and number of bids)
        """
        func_name = "get_auction_data"

        try:
            results = []

            with self.cross_chain_transactions_repo.get_session() as session:
                bid_tx = aliased(MayanBlockchainTransaction)

                return (
                    session.query(
                        MayanAuctionBid.auction_state.label("auction_id"),
                        MayanAuctionBid.order_hash.label("order_hash"),
                        func.min(bid_tx.timestamp).label("auction_first_bid_timestamp"),
                        func.max(bid_tx.timestamp).label("auction_last_bid_timestamp"),
                        func.count(bid_tx.transaction_hash).label("auction_number_of_bids"),
                    )
                    .join(bid_tx, MayanAuctionBid.signature == bid_tx.transaction_hash)
                    .group_by(MayanAuctionBid.auction_state, MayanAuctionBid.order_hash)
                    .subquery()
                )

            return results

        except Exception as e:
            raise CustomException(
                self.CLASS_NAME, func_name, f"Error fetching auction data. Error: {e}"
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
                    "name": "Solana",
                    "decimals": 9,
                    "blockchain": "solana",
                    "address": "11111111111111111111111111111111",
                }
            )

        # In Mayan, when the native token is used in the destination blockchain,
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

    def fix_token_symbol_clashes(self):
        log_to_cli(
            build_log_message_generator(
                self.bridge, "Fixing token symbol clashes in Mayan cross-chain transactions..."
            )
        )

        # Also, we need to fix the decimals for the PEPE token on BNB with address
        # 0xb46584e0efdE3092e04010A13f2eAe62aDb3b9F0. The Alchemy API returns
        # the "real" PEPE token with a valuation much higher than the one
        # actually used in the BNB chain, so we need to fix it manually
        # fetched by the Alchemy API: https://coinmarketcap.com/currencies/pepe/
        # used in the BNB chain: https://coinmarketcap.com/currencies/pepe-coin-bsc2/

        # since we have very few transactions with this token, we can just delete the
        # usd valuation
        with self.cross_chain_transactions_repo.get_session() as session:
            stmt = (
                update(MayanCrossChainTransaction)
                .where(
                    MayanCrossChainTransaction.src_blockchain == "bnb",
                    MayanCrossChainTransaction.src_contract_address
                    == "0xb46584e0efdE3092e04010A13f2eAe62aDb3b9F0",
                )
                .values(input_amount_usd=None, refund_fee_usd=None)
            )
            session.execute(stmt)

        # Also, we need to fix the USD values of the 'Bitcoin on Base' token
        # because it is not worth the same as BTC
        with self.cross_chain_transactions_repo.get_session() as session:
            stmt = (
                update(MayanCrossChainTransaction)
                .where(
                    MayanCrossChainTransaction.src_blockchain == "base",
                    MayanCrossChainTransaction.src_contract_address
                    == "0x0c41f1fc9022feb69af6dc666abfe73c9ffda7ce",
                )
                .values(input_amount_usd=None, refund_fee_usd=None)
            )
            session.execute(stmt)
