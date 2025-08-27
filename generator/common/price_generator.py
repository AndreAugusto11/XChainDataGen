import time
from datetime import datetime, timedelta

from sqlalchemy import text

from config.constants import BLOCKCHAIN_IDS
from repository.common.repository import (
    NativeTokenRepository,
    TokenMetadataRepository,
    TokenPriceRepository,
)
from rpcs.alchemy_client import AlchemyClient
from utils.utils import (
    CliColor,
    CustomException,
    build_log_message_generator,
    get_blockchain_native_token_symbol,
    log_error,
    log_to_cli,
)


class PriceGenerator:
    CLASS_NAME = "PriceGenerator"

    def __init__(self):
        self.pairs_tried_price = {}  # {blockchain: [token_contracts, ...]}
        self.pairs_tried_metadata = {}  # {blockchain: [token_contracts, ...]}

    def populate_native_tokens(
        self,
        bridge: str,
        native_token_repo: NativeTokenRepository,
        token_metadata_repo: TokenMetadataRepository,
        token_price_repo: TokenPriceRepository,
        start_ts: str,
        end_ts: str,
    ):
        log_to_cli(
            build_log_message_generator(
                bridge,
                "Fetching prices for native tokens...",
            ),
            CliColor.INFO,
        )

        PriceGenerator.create_null_token_prices(token_price_repo, start_ts, end_ts)

        try:
            rows = []
            for blockchain_id in BLOCKCHAIN_IDS.keys():
                metadata = BLOCKCHAIN_IDS[blockchain_id]
                blockchain = metadata["name"]

                if "native_token_contract" not in metadata:
                    continue

                record = native_token_repo.get_native_token_by_blockchain(blockchain)

                symbol = get_blockchain_native_token_symbol(blockchain)

                if record is None:
                    rows.append(
                        {
                            "symbol": symbol,
                            "blockchain": blockchain,
                        }
                    )

                token_metadata = token_metadata_repo.get_token_metadata_by_symbol_and_blockchain(
                    symbol, blockchain
                )
                name = token_metadata.name if token_metadata is not None else None

                if token_metadata is None:
                    token_metadata = self.fetch_and_store_token_metadata(
                        bridge,
                        token_metadata_repo,
                        blockchain,
                        metadata["native_token_contract"],
                        None,
                    )

                    name = token_metadata["name"]

                completed, dates = PriceGenerator.is_token_price_complete(
                    token_price_repo, start_ts, end_ts, symbol, name
                )

                if not completed:
                    if dates is None:
                        PriceGenerator.fetch_and_store_token_prices(
                            bridge, token_price_repo, start_ts, end_ts, name=name, symbol=symbol
                        )
                    else:
                        for [_start_ts, _end_ts] in dates:
                            PriceGenerator.fetch_and_store_token_prices(
                                bridge,
                                token_price_repo,
                                _start_ts,
                                _end_ts,
                                name=name,
                                symbol=symbol,
                            )

                # Sometimes when the native token is used, the address is set to
                # 0x0000000000000000000000000000000000000000
                # however, if we fetch info from Alchemy, we will not get the
                # token metadata for the native token, so we need to fill it manually
                # with the data we have in the NativeToken table and the TokenMetadata table
                if not token_metadata_repo.get_token_metadata_by_contract_and_blockchain(
                    "0x0000000000000000000000000000000000000000",
                    blockchain,
                ):
                    token_metadata_repo.create(
                        {
                            "symbol": metadata["native_token"],
                            "name": name,
                            "decimals": token_metadata["decimals"]
                            if isinstance(token_metadata, dict)
                            else token_metadata.decimals,
                            "blockchain": blockchain,
                            "address": "0x0000000000000000000000000000000000000000",  # native token
                        }
                    )

            if len(rows) > 0:
                native_token_repo.create_all(rows)

        except Exception as e:
            raise CustomException(
                PriceGenerator.CLASS_NAME,
                "populate_native_tokens",
                f"Error while populating native tokens: {str(e)}",
            ) from e

    def populate_token_info(
        self,
        bridge: str,
        token_metadata_repo: TokenMetadataRepository,
        token_price_repo: TokenPriceRepository,
        src_blockchain: str,
        dst_blockchain: str,
        input_token: str,
        output_token: str,
        start_ts: str,
        end_ts: str,
        # src_contract_address and dst_contract_address exist to store the contract being used in
        # the bridge that is not the token itself (e.g. a liquidity pool based on the token)
        src_contract_address: str = None,
        dst_contract_address: str = None,
    ):
        try:
            token_symbol = None
            token_name = None

            src_token_metadata = token_metadata_repo.get_token_metadata_by_contract_and_blockchain(
                src_contract_address if src_contract_address is not None else input_token,
                src_blockchain,
            )
            dst_token_metadata = token_metadata_repo.get_token_metadata_by_contract_and_blockchain(
                dst_contract_address if dst_contract_address is not None else output_token,
                dst_blockchain,
            )

            if input_token is None:
                # in this case, there is no token recorded in the cctx, therefore we cannot fetch
                # the token metadata
                pass
            else:
                if src_token_metadata is None:
                    metadata = self.fetch_and_store_token_metadata(
                        bridge,
                        token_metadata_repo,
                        src_blockchain,
                        input_token,
                        src_contract_address,
                    )

                    if not (metadata is None or "symbol" not in metadata or "name" not in metadata):
                        token_symbol = metadata["symbol"]
                        token_name = metadata["name"]

                elif dst_token_metadata is not None:
                    token_symbol = src_token_metadata.symbol
                    token_name = src_token_metadata.name

                # check if we have already fetched the token prices for this symbol
                if token_symbol is not None and token_name is not None:
                    completed, dates = PriceGenerator.is_token_price_complete(
                        token_price_repo, start_ts, end_ts, token_symbol, token_name
                    )

                    if not completed and not self.has_tried_price_fetching_for_contract(
                        src_blockchain, input_token
                    ):
                        if dates is None:
                            PriceGenerator.fetch_and_store_token_prices(
                                bridge,
                                token_price_repo,
                                start_ts,
                                end_ts,
                                name=token_name,
                                symbol=token_symbol,
                                blockchain=src_blockchain,
                                token_address=input_token,
                            )
                        else:
                            for [_start_ts, _end_ts] in dates:
                                PriceGenerator.fetch_and_store_token_prices(
                                    bridge,
                                    token_price_repo,
                                    _start_ts,
                                    _end_ts,
                                    name=token_name,
                                    symbol=token_symbol,
                                    blockchain=src_blockchain,
                                    token_address=input_token,
                                )

                        self.update_pairs_tried_price_fetching(src_blockchain, input_token)

            if output_token is None:
                # in this case, there is no token recorded in the cctx, therefore we cannot fetch
                # the token metadata
                pass
            else:
                if dst_token_metadata is None:
                    metadata = self.fetch_and_store_token_metadata(
                        bridge,
                        token_metadata_repo,
                        dst_blockchain,
                        output_token,
                        dst_contract_address,
                    )
                    if metadata is None or "symbol" not in metadata or "name" not in metadata:
                        return

                    token_symbol = metadata["symbol"]
                    token_name = metadata["name"]
                else:
                    metadata = token_metadata_repo.get_token_metadata_by_contract_and_blockchain(
                        output_token,
                        dst_blockchain,
                    )

                    if metadata is None or not metadata.symbol or not metadata.name:
                        return

                    token_symbol = metadata.symbol
                    token_name = metadata.name

                if token_symbol is None or token_name is None:
                    # if the token symbol or name is None, we cannot fetch the prices
                    # for this token

                    log_to_cli(
                        build_log_message_generator(
                            bridge,
                            f"Token metadata for {input_token} ({src_blockchain}) or "
                            f"{output_token} ({dst_blockchain}) is missing. "
                            "Skipping price fetching.",
                        ),
                        CliColor.INFO,
                    )
                    return

                # check if we have already fetched the token prices for this symbol
                completed, dates = PriceGenerator.is_token_price_complete(
                    token_price_repo, start_ts, end_ts, token_symbol, token_name
                )

                if not completed and not self.has_tried_price_fetching_for_contract(
                    dst_blockchain, output_token
                ):
                    if dates is None:
                        PriceGenerator.fetch_and_store_token_prices(
                            bridge,
                            token_price_repo,
                            start_ts,
                            end_ts,
                            name=token_name,
                            symbol=token_symbol,
                            blockchain=dst_blockchain,
                            token_address=output_token,
                        )
                    else:
                        for [_start_ts, _end_ts] in dates:
                            PriceGenerator.fetch_and_store_token_prices(
                                bridge,
                                token_price_repo,
                                _start_ts,
                                _end_ts,
                                name=token_name,
                                symbol=token_symbol,
                                blockchain=dst_blockchain,
                                token_address=output_token,
                            )

                    self.update_pairs_tried_price_fetching(dst_blockchain, output_token)
        except Exception as e:
            exception = CustomException(
                self.CLASS_NAME,
                "populate_token_info",
                (
                    f"Error while populating token info for {input_token} ({src_blockchain}) and "
                    f"{output_token} ({dst_blockchain}): {str(e)}",
                ),
            )

            log_error(bridge, exception)

    def fetch_and_store_token_metadata(
        self,
        bridge: str,
        token_metadata_repo: TokenMetadataRepository,
        blockchain: str,
        token_contract: str,
        # contract_address exists to store the contract being used in
        # the bridge that is not the token itself (e.g. a liquidity pool based on the token)
        contract_address: str,
    ):
        try:
            if blockchain == "solana":
                return None  # Alchemy does not support Solana

            if self.has_tried_metadata_fetching_for_contract(blockchain, token_contract):
                return None

            log_to_cli(
                build_log_message_generator(
                    bridge,
                    f"Fetching metadata for {token_contract} in {blockchain}...",
                ),
                CliColor.INFO,
            )

            metadata = AlchemyClient.get_token_metadata(blockchain, token_contract)

            if metadata is None or "symbol" not in metadata or "name" not in metadata:
                return None

            metadata["symbol"] = metadata["symbol"].upper()

            token_metadata_repo.create(
                {
                    "symbol": metadata["symbol"],
                    "name": metadata["name"],
                    "decimals": metadata["decimals"] if metadata["decimals"] else 1,
                    "blockchain": blockchain,
                    "address": token_contract if contract_address is None else contract_address,
                }
            )

            return metadata
        except Exception:
            return None
        finally:
            self.update_pairs_tried_metadata_fetching(blockchain, token_contract)

    def fetch_and_store_token_prices(
        bridge: str,
        token_price_repo: TokenPriceRepository,
        start_ts: int,
        end_ts: int,
        name: str,
        symbol: str = None,
        blockchain: str = None,
        token_address: str = None,
    ):
        if blockchain == "solana":
            return None  # Alchemy does not support Solana

        if symbol is None or name is None:
            return

        log_to_cli(
            build_log_message_generator(
                bridge,
                f"Fetching historical price of {symbol}...",
            ),
            CliColor.INFO,
        )

        if "usd" in symbol.lower() or "dai" in symbol.lower() or "frax" in symbol.lower():
            rows = []
            current_ts = start_ts
            one_day = 86400  # seconds in a day
            while current_ts <= end_ts:
                date = datetime.fromtimestamp(current_ts)
                rows.append(
                    {
                        "symbol": symbol,
                        "name": name,
                        "date": date,
                        "price_usd": 1.0,
                    }
                )
                current_ts += one_day

            token_price_repo.create_all(rows)
            return

        if blockchain is None and token_address is None:
            token_prices = AlchemyClient.get_token_prices_by_symbol_or_address(
                bridge, start_ts, end_ts, symbol=symbol
            )
        else:
            token_prices = AlchemyClient.get_token_prices_by_symbol_or_address(
                bridge, start_ts, end_ts, blockchain=blockchain, token_address=token_address
            )

        if token_prices is None or "data" not in token_prices:
            return

        rows = []
        for pair in token_prices["data"]:
            date_struct = time.strptime(pair["timestamp"], "%Y-%m-%dT%H:%M:%SZ")
            date = datetime.fromtimestamp(time.mktime(date_struct))

            rows.append(
                {
                    "symbol": symbol,
                    "name": name,
                    "date": date,
                    "price_usd": pair["value"],
                }
            )

        token_price_repo.create_all(rows)

    def is_token_price_complete(
        token_price_repo: TokenPriceRepository, start_ts: str, end_ts: str, symbol: str, name: str
    ):
        days_diff = (
            datetime.fromtimestamp(end_ts).date() - datetime.fromtimestamp(start_ts).date()
        ).days + 1  # inclusive of start and end dates
        db_data = token_price_repo.get_count_datapoints_for_symbol_and_name_between_dates(
            symbol, name, start_ts, end_ts
        )

        if db_data == 0 or db_data is None:
            return False, None
        elif db_data == days_diff:
            return True, None
        else:
            dates = []
            min_date_stored = token_price_repo.get_min_date_for_symbol_and_name(symbol, name)
            max_date_stored = token_price_repo.get_max_date_for_symbol_and_name(symbol, name)

            # calculate difference between the start_ts (unix) and the min_date_stored (sql date)
            start_ts_diff = min_date_stored - datetime.fromtimestamp(start_ts).date()
            start_ts_diff = start_ts_diff.days

            if start_ts_diff > 0:
                dates.append([start_ts, int(time.mktime((min_date_stored).timetuple()))])

            # calculate difference between the end_ts (unix) and the max_date_stored (sql date)
            end_ts_diff = datetime.fromtimestamp(end_ts).date() - max_date_stored
            end_ts_diff = end_ts_diff.days

            if end_ts_diff > 0:
                dates.append([int(time.mktime((max_date_stored).timetuple())), end_ts])

            if dates == []:
                return True, None

        return False, dates

    def update_pairs_tried_metadata_fetching(self, blockchain, contract):
        if blockchain in self.pairs_tried_metadata:
            self.pairs_tried_metadata[blockchain].append(contract)
        else:
            self.pairs_tried_metadata[blockchain] = [contract]

    def has_tried_metadata_fetching_for_contract(self, blockchain, contract):
        if blockchain not in self.pairs_tried_metadata:
            return False
        return contract in self.pairs_tried_metadata[blockchain]

    def update_pairs_tried_price_fetching(self, blockchain, contract):
        if blockchain in self.pairs_tried_price:
            self.pairs_tried_price[blockchain].append(contract)
        else:
            self.pairs_tried_price[blockchain] = [contract]

    def has_tried_price_fetching_for_contract(self, blockchain, contract):
        if blockchain not in self.pairs_tried_price:
            return False
        return contract in self.pairs_tried_price[blockchain]

    def create_null_token_prices(token_price_repo, start_ts, end_ts):
        """used to populate token prices for unmapped tokens with invalid symbols"""

        completed, _ = PriceGenerator.is_token_price_complete(
            token_price_repo, start_ts, end_ts, "", ""
        )

        if completed:
            return

        start_date = datetime.fromtimestamp(start_ts).date()
        end_date = datetime.fromtimestamp(end_ts).date()

        rows = []
        while start_date <= end_date:
            rows.append(
                {
                    "symbol": "",
                    "name": "",
                    "date": start_date,
                    "price_usd": 0,
                }
            )
            start_date += timedelta(days=1)

        token_price_repo.create_all(rows)

    def calculate_cctx_usd_values(
        bridge: str,
        cctx_repo,
        table_name: str,
        amount_field_name: str,
        blockchain_field_name: str,
        contract_address_field_name: str,
        timestamp_field_name: str,
        usd_value_field_name: str,
    ):
        func_name = "calculate_cctx_usd_values"

        start_time = time.time()
        log_to_cli(
            build_log_message_generator(
                bridge,
                f"Calculating USD values for {amount_field_name} in {table_name}...",
            ),
            CliColor.INFO,
        )

        query = text(
            f"""
                UPDATE {table_name} cctx
                SET {usd_value_field_name} = token_price.price_usd * cctx.{amount_field_name} / power(10, token_metadata.decimals)
                FROM token_metadata
                JOIN token_price
                    ON token_metadata.symbol = token_price.symbol
                WHERE lower(cctx.{contract_address_field_name}) = lower(token_metadata.address)
                AND cctx.{blockchain_field_name} = token_metadata.blockchain
                AND CAST(TO_TIMESTAMP(cctx.{timestamp_field_name}) AS DATE) = token_price.date;
            """  # noqa: E501
        )

        try:
            cctx_repo.execute(query)

            total_value = cctx_repo.get_total_amount_usd_transacted()

            formatted_total_value = "${:,.2f}".format(total_value) if total_value else "$0.00"

            end_time = time.time()
            log_to_cli(
                build_log_message_generator(
                    bridge,
                    (
                        f"Calculated USD values for {table_name} in {end_time - start_time} seconds"
                        f". Total value: {formatted_total_value}",
                    ),
                ),
                CliColor.SUCCESS,
            )
        except Exception as e:
            raise CustomException(
                PriceGenerator.CLASS_NAME,
                func_name,
                f"Error processing USD values for {amount_field_name} in {table_name}. Error: {e}",
            ) from e

    def calculate_cctx_native_usd_values(
        bridge: str,
        cctx_repo,
        table_name: str,
        timestamp_field_name: str,
        blockchain_field_name: str,
        fee_field_name: str,
        usd_fee_field_name: str,
    ):
        func_name = "calculate_cctx_native_usd_values"

        start_time = time.time()
        log_to_cli(
            build_log_message_generator(
                bridge,
                f"Calculating USD values for {fee_field_name} in {table_name}...",
            ),
            CliColor.INFO,
        )

        query = text(
            f"""
            UPDATE {table_name} cctx
            SET {usd_fee_field_name} = token_price.price_usd * cctx.{fee_field_name} / power(10, token_metadata.decimals)
            FROM token_metadata
            JOIN token_price
                ON token_metadata.symbol = token_price.symbol 
                AND token_metadata.name = token_price.name
            WHERE
                token_metadata.address = '0x0000000000000000000000000000000000000000'
                AND cctx.{blockchain_field_name} = token_metadata.blockchain
                AND CAST(TO_TIMESTAMP(cctx.{timestamp_field_name}) AS DATE) = token_price.date;
        """  # noqa: E501
        )

        try:
            cctx_repo.execute(query)

            end_time = time.time()
            log_to_cli(
                build_log_message_generator(
                    bridge,
                    (
                        f"Calculating USD values for {fee_field_name} in {table_name}... "
                        f"Completed in {end_time - start_time} seconds.",
                    ),
                ),
                CliColor.SUCCESS,
            )
        except Exception as e:
            raise CustomException(
                PriceGenerator.CLASS_NAME,
                func_name,
                f"Error processing USD values for {table_name}. Error: {e}",
            ) from e
