import time

from sqlalchemy import text

from config.constants import Bridge
from generator.base_generator import BaseGenerator
from generator.common.price_generator import PriceGenerator
from repository.common.repository import *
from repository.database import DBSession
from repository.omnibridge.repository import *
from utils.utils import (CliColor, CustomException,
                         build_log_message_generator, log_error, log_to_cli)


class OmnibridgeGenerator(BaseGenerator):
    CLASS_NAME = "OmnibridgeGenerator"

    def __init__(self) -> None:
        super().__init__()
        self.bridge = Bridge.OMNIBRIDGE
        self.price_generator = PriceGenerator()

    def bind_db_to_repos(self):
        self.transactions_repo = OmnibridgeBlockchainTransactionRepository(DBSession)
        self.tokens_bridged_repo = OmnibridgeTokensBridgedRepository(DBSession)
        self.tokens_bridging_initiated_repo = OmnibridgeTokensBridgingInitiatedRepository(DBSession)
        self.relayed_message_repo = OmnibridgeRelayedMessageRepository(DBSession)
        self.signed_for_user_request_repo = OmnibridgeSignedForUserRequestRepository(DBSession)
        self.signed_for_affirmation_repo = OmnibridgeSignedForAffirmationRepository(DBSession)
        self.user_request_for_signature_repo = OmnibridgeUserRequestForSignatureRepository(DBSession)
        self.affirmation_completed_repo = OmnibridgeAffirmationCompletedRepository(DBSession)
        self.user_request_for_affirmation_repo = OmnibridgeUserRequestForAffirmationRepository(DBSession)

        self.xdai_cross_chain_transactions = OmnibridgeCrossChainTransactionsRepository(DBSession)
        self.operator_transactions = OmnibridgeOperatorTransactionsRepository(DBSession)

        self.token_metadata_repo = TokenMetadataRepository(DBSession)
        self.token_price_repo = TokenPriceRepository(DBSession)
        self.native_token_repo = NativeTokenRepository(DBSession)

    def generate_cross_chain_data(self):
        func_name = "create_cross_chain_transactions"

        try:
            self.match_xdai_cctxs()
            self.match_omnibridge_cctxs()
            self.match_operator_cctxs()

            start_ts = int(self.transactions_repo.get_min_timestamp()) - 86400
            end_ts = int(self.transactions_repo.get_max_timestamp()) + 86400

            ## POPULATE TOKEN TABLES WITH NATIVE TOKEN INFO
            PriceGenerator.populate_native_tokens(self.bridge, self.native_token_repo, self.token_metadata_repo, self.token_price_repo, start_ts, end_ts)

            cctxs = self.xdai_cross_chain_transactions.get_unique_src_dst_contract_pairs()
            self.populate_token_info_tables(cctxs, start_ts, end_ts)

            # a lot of token addresses in Gnosis are not being recognized by alchemy, so we fetch from both the src and dst blockchains, to make sure we use the Ethereum contracts
            PriceGenerator.calculate_cctx_usd_values(self.bridge, self.xdai_cross_chain_transactions, "omnibridge_cross_chain_transactions", "amount", "src_blockchain", "src_contract_address", "src_timestamp", "amount_usd")
            PriceGenerator.calculate_cctx_usd_values(self.bridge, self.xdai_cross_chain_transactions, "omnibridge_cross_chain_transactions", "amount", "dst_blockchain", "dst_contract_address", "dst_timestamp", "amount_usd")

            PriceGenerator.calculate_cctx_native_usd_values(self.bridge, self.xdai_cross_chain_transactions, "omnibridge_cross_chain_transactions", "src_timestamp", "src_blockchain", "src_fee",  "src_fee_usd")
            PriceGenerator.calculate_cctx_native_usd_values(self.bridge, self.xdai_cross_chain_transactions, "omnibridge_cross_chain_transactions", "dst_timestamp", "dst_blockchain", "dst_fee",  "dst_fee_usd")
            PriceGenerator.calculate_cctx_native_usd_values(self.bridge, self.operator_transactions, "omnibridge_operator_transactions", "timestamp", "blockchain", "fee",  "fee_usd")

        except Exception as e:
            exception = CustomException(
                self.CLASS_NAME,
                func_name,
                f"Error processing cross chain transactions. Error: {e}",
            )
            log_error(self.bridge, exception)


    def match_xdai_cctxs(self):
        func_name = "match_xdai_cctxs"

        start_time = time.time()
        log_to_cli(
            build_log_message_generator(self.bridge, "Matching xDAI token transfers...")
        )

        self.xdai_cross_chain_transactions.empty_table()

        query_gnosis_to_ethereum = text(
        """
            INSERT INTO omnibridge_cross_chain_transactions (
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
                NULL as message_id,
                src_tx.from_address,
                deposit.recipient,
                '0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d', -- we hardcode the xDAI address in Gnosis
                '0x6b175474e89094c44da98b954eedeac495271d0f', -- we hardcode the xDAI address in Ethereum
                deposit.value,
                NULL as amount_usd
            FROM omnibridge_user_request_for_signature deposit
            JOIN omnibridge_blockchain_transaction src_tx ON src_tx.transaction_hash = deposit.transaction_hash
            JOIN omnibridge_relayed_message fill ON fill.recipient = deposit.recipient AND fill.value = deposit.value AND fill.src_transaction_hash = src_tx.transaction_hash
            JOIN omnibridge_blockchain_transaction dst_tx ON dst_tx.transaction_hash = fill.transaction_hash
            WHERE deposit.value is not NULL AND deposit.recipient is not NULL;
        """
        )

        query_ethereum_to_gnosis = text(
        """
            INSERT INTO omnibridge_cross_chain_transactions (
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
                NULL as message_id,
                src_tx.from_address,
                deposit.recipient,
                '0x6b175474e89094c44da98b954eedeac495271d0f', -- we hardcode the xDAI address in Ethereum
                '0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d', -- we hardcode the xDAI address in Gnosis
                deposit.value,
                NULL as amount_usd
            FROM omnibridge_user_request_for_affirmation deposit
            JOIN omnibridge_blockchain_transaction src_tx ON src_tx.transaction_hash = deposit.transaction_hash
            JOIN omnibridge_affirmation_completed fill ON fill.recipient = deposit.recipient AND fill.value = deposit.value AND fill.src_transaction_hash = src_tx.transaction_hash
            JOIN omnibridge_blockchain_transaction dst_tx ON dst_tx.transaction_hash = fill.transaction_hash
            WHERE deposit.value is not NULL AND deposit.recipient is not NULL;
        """
        )

        try:
            self.xdai_cross_chain_transactions.populate_table(query_gnosis_to_ethereum)
            self.xdai_cross_chain_transactions.populate_table(query_ethereum_to_gnosis)

            size = self.xdai_cross_chain_transactions.get_number_of_records()

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


    def match_omnibridge_cctxs(self):
        func_name = "match_omnibridge_cctxs"

        start_time = time.time()
        log_to_cli(
            build_log_message_generator(self.bridge, "Matching Omnibridge token transfers...")
        )

        self.xdai_cross_chain_transactions.empty_table()

        query_gnosis_to_ethereum = text(
        """
            INSERT INTO omnibridge_cross_chain_transactions (
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
                deposit.message_id,
                deposit2.sender,
                fill.recipient,
                deposit2.token, -- we hardcode the xDAI address in Ethereum
                fill.token, -- we hardcode the xDAI address in Gnosis
                fill.value,
                NULL as amount_usd
            FROM omnibridge_user_request_for_signature deposit
            JOIN omnibridge_tokens_bridging_initiated deposit2 ON deposit2.message_id = deposit.message_id
            JOIN omnibridge_blockchain_transaction src_tx ON src_tx.transaction_hash = deposit.transaction_hash
            JOIN omnibridge_tokens_bridged fill ON fill.message_id = deposit2.message_id AND fill.value = deposit2.value
            JOIN omnibridge_blockchain_transaction dst_tx ON dst_tx.transaction_hash = fill.transaction_hash
            WHERE deposit.message_id is not NULL AND deposit.encoded_data is not NULL;
        """
        )

        query_ethereum_to_gnosis = text(
        """
            INSERT INTO omnibridge_cross_chain_transactions (
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
                deposit.message_id,
                deposit2.sender,
                fill.recipient,
                deposit2.token, -- we hardcode the xDAI address in Ethereum
                fill.token, -- we hardcode the xDAI address in Gnosis
                fill.value,
                NULL as amount_usd
            FROM omnibridge_user_request_for_affirmation deposit
            JOIN omnibridge_tokens_bridging_initiated deposit2 ON deposit2.message_id = deposit.message_id AND deposit2.blockchain = deposit.blockchain
            JOIN omnibridge_blockchain_transaction src_tx ON src_tx.transaction_hash = deposit.transaction_hash
            JOIN omnibridge_tokens_bridged fill ON fill.message_id = deposit2.message_id AND fill.value = deposit2.value
            JOIN omnibridge_blockchain_transaction dst_tx ON dst_tx.transaction_hash = fill.transaction_hash
            WHERE deposit.message_id is not NULL AND deposit.encoded_data is not NULL;
        """
        )

        try:
            self.xdai_cross_chain_transactions.populate_table(query_gnosis_to_ethereum)
            self.xdai_cross_chain_transactions.populate_table(query_ethereum_to_gnosis)

            size = self.xdai_cross_chain_transactions.get_number_of_records()

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
        
    def match_operator_cctxs(self):
        func_name = "match_operator_cctxs"

        start_time = time.time()

        log_to_cli(
            build_log_message_generator(self.bridge, "Matching Omnibridge token transfers...")
        )

        self.operator_transactions.empty_table()

        query = text(
        """
            INSERT INTO omnibridge_operator_transactions (
                blockchain,
                transaction_hash,
                from_address,
                to_address,
                signer,
                fee,
                fee_usd,
                timestamp,
                status
            )
            SELECT
                tx.blockchain,
                tx.transaction_hash,
                tx.from_address,
                tx.to_address,
                sig.signer,
                tx.fee,
                NULL as src_fee_usd,
                tx.timestamp,
                tx.status
            FROM omnibridge_signed_for_user_request sig
            JOIN omnibridge_blockchain_transaction tx ON tx.transaction_hash = sig.transaction_hash;
        """
        )

        try:
            self.operator_transactions.populate_table(query)

            size = self.operator_transactions.get_number_of_records()

            end_time = time.time()
            log_to_cli(
                build_log_message_generator(
                    self.bridge,
                    f"Operator transactions matched in {end_time - start_time} seconds. Total records inserted: {size}",
                ),
                CliColor.SUCCESS,
            )
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"Error processing token. Error: {e}",
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
