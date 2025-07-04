from typing import Any, Dict, List

from config.constants import Bridge
from extractor.base_handler import BaseHandler
from extractor.mayan.constants import (
    BLOCKCHAIN_IDS,
    BRIDGE_CONFIG,
    SOLANA_PROGRAM_ADDRESSES,
)
from extractor.mayan.utils.OrderHash import reconstruct_order_hash_from_params
from repository.database import DBSession
from repository.mayan.repository import (
    MayanAuctionBidRepository,
    MayanAuctionCloseRepository,
    MayanBlockchainTransactionRepository,
    MayanForwardedRepository,
    MayanFulfillOrderRepository,
    MayanInitOrderRepository,
    MayanOrderCreatedRepository,
    MayanOrderFulfilledRepository,
    MayanOrderUnlockedRepository,
    MayanRegisterOrderRepository,
    MayanSetAuctionWinnerRepository,
    MayanSettleRepository,
    MayanSwapAndForwardedRepository,
    MayanUnlockRepository,
)
from rpcs.evm_rpc_client import EvmRPCClient
from utils.utils import (
    CustomException,
    convert_32_byte_array_to_evm_address,
    convert_32_byte_array_to_solana_address,
    log_error,
)


class MayanHandler(BaseHandler):
    CLASS_NAME = "MayanHandler"

    def __init__(self, rpc_client: EvmRPCClient, blockchains: list) -> None:
        super().__init__(rpc_client, blockchains)
        self.bridge = Bridge.MAYAN

    def get_solana_bridge_program_ids(self) -> str:
        """
        Returns the Solana bridge program ID for Mayan.
        """
        return SOLANA_PROGRAM_ADDRESSES

    def get_bridge_contracts_and_topics(self, bridge: str, blockchain: List[str]) -> None:
        return super().get_bridge_contracts_and_topics(
            config=BRIDGE_CONFIG,
            bridge=bridge,
            blockchain=blockchain,
        )

    def bind_db_to_repos(self):
        self.blockchain_transaction_repo = MayanBlockchainTransactionRepository(DBSession)
        self.order_created_repo = MayanOrderCreatedRepository(DBSession)
        self.order_fulfilled_repo = MayanOrderFulfilledRepository(DBSession)
        self.order_unlocked_repo = MayanOrderUnlockedRepository(DBSession)
        self.swap_and_forwarded_repo = MayanSwapAndForwardedRepository(DBSession)
        self.forwarded_repo = MayanForwardedRepository(DBSession)
        self.init_order_repo = MayanInitOrderRepository(DBSession)
        self.unlock_repo = MayanUnlockRepository(DBSession)
        self.fulfill_repo = MayanFulfillOrderRepository(DBSession)
        self.settle_repo = MayanSettleRepository(DBSession)
        self.set_auction_winner_repo = MayanSetAuctionWinnerRepository(DBSession)
        self.register_order_repo = MayanRegisterOrderRepository(DBSession)
        self.auction_bid_repo = MayanAuctionBidRepository(DBSession)
        self.auction_close_repo = MayanAuctionCloseRepository(DBSession)

    def does_transaction_exist_by_hash(self, transaction_hash: str) -> Any:
        func_name = "does_transaction_exist_by_hash"
        """
        Retrieves a transaction by its hash from the database.

        Args:
            transaction_hash: The hash of the transaction to retrieve.

        Returns:
            The transaction with the given hash.
        """
        try:
            return self.blockchain_transaction_repo.get_transaction_by_hash(transaction_hash)
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"Error reading transaction from database: {e}",
            ) from e

    def handle_events(
        self,
        blockchain: str,
        start_block: int,
        end_block: int,
        contract: str,
        topics: List[str],
        events: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        included_events = []
        for event in events:
            try:
                if (
                    event["topic"]
                    == "0x7cbff921ae1f3ea71284120d2aabde13587df067f2bb5c831ea6e35d7a9242ac"
                ):  # SwapAndForwardedEth
                    event = self.handle_swap_and_forwarded_eth(blockchain, event)
                elif (
                    event["topic"]
                    == "0x23278f58875126c795a4072b98b5851fe9b21cea19895b02a6224fefbb1e3298"
                ):  # SwapAndForwardedERC20
                    event = self.handle_swap_and_forwarded_erc20(blockchain, event)
                elif (
                    event["topic"]
                    == "0xb8543d214cab9591941648db8d40126a163bfd0db4a865678320b921e1398043"
                ):  # ForwardedEth
                    event = self.handle_forwarded_eth(blockchain, event)
                elif (
                    event["topic"]
                    == "0xbf150db6b4a14b084f7346b4bc300f552ce867afe55be27bce2d6b37e3307cda"
                ):  # ForwardedERC20
                    event = self.handle_forwarded_erc20(blockchain, event)
                elif (
                    event["topic"]
                    == "0x918554b6bd6e2895ce6553de5de0e1a69db5289aa0e4fe193a0dcd1f14347477"
                ):  # OrderCreated
                    event = self.handle_order_created(blockchain, event)
                elif (
                    event["topic"]
                    == "0x6ec9b1b5a9f54d929394f18dac4ba1b1cc79823f2266c2d09cab8a3b4700b40b"
                ):  # OrderFulfilled
                    event = self.handle_order_fulfilled(blockchain, event)
                elif (
                    event["topic"]
                    == "0x4bdcff348c4d11383c487afb95f732f243d93fbfc478aa736a4981cf6a640911"
                ):  # OrderUnlocked
                    event = self.handle_order_unlocked(blockchain, event)

                if event:
                    included_events.append(event)

            except CustomException as e:
                request_desc = (
                    f"Error processing request: {blockchain}, {start_block}, "
                    f"{end_block}, {contract}, {topics}.\n{e}"
                )
                log_error(self.bridge, request_desc)

        return included_events

    def handle_swap_and_forwarded_eth(self, blockchain, event):
        func_name = "handle_swap_and_forwarded_eth"

        event["tokenIn"] = self.populate_weth_token()

        try:
            return self.handle_swap_and_forwarded(blockchain, event)
        except CustomException as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e

    def handle_swap_and_forwarded_erc20(self, blockchain, event):
        func_name = "handle_swap_and_forwarded_erc20"

        try:
            return self.handle_swap_and_forwarded(blockchain, event)
        except CustomException as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e

    def handle_swap_and_forwarded(self, blockchain, event):
        func_name = "handle_swap_and_forwarded"

        try:
            if self.swap_and_forwarded_repo.event_exists(event["transaction_hash"]):
                return None

            # Only interested in events from the Mayan Swift protocol (other alternatives
            # are WH Swap Bridge and Mayan MCTP, currently not supported)
            if event["mayanProtocol"] != "0xC38e4e6A15593f908255214653d3D947CA1c2338":
                return None

            decoded_payload = None

            # function signature for createOrderWithEth
            if event["mayanData"][:8] == "b866e173":
                from extractor.mayan.utils.MayanOrderParamsDecoder import MayanOrderParamsDecoder

                decoded_payload = MayanOrderParamsDecoder.decode(event["mayanData"][8:])

            # function signature for createOrderWithToken
            elif event["mayanData"][:8] == "8e8d142b":
                from extractor.mayan.utils.MayanOrderParamsDecoder import MayanOrderParamsDecoder

                decoded_payload = MayanOrderParamsDecoder.decode(event["mayanData"][136:])

            dst_chain = self.convert_id_to_blockchain_name(
                id=decoded_payload["destChainId"],
                blockchain_ids=BLOCKCHAIN_IDS,
            )

            if not dst_chain:
                return None

            self.swap_and_forwarded_repo.create(
                {
                    "blockchain": blockchain,
                    "transaction_hash": event["transaction_hash"],
                    "token_in": event["tokenIn"],
                    "amount_in": event["amountIn"],
                    "swap_protocol": event["swapProtocol"],
                    "middle_token": event["middleToken"],
                    "middle_amount": event["middleAmount"],
                    "mayan_protocol": event["mayanProtocol"],
                    "trader": decoded_payload["trader"],
                    "token_out": decoded_payload["tokenOut"],
                    "min_amount_out": decoded_payload["minAmountOut"],
                    "gas_drop": decoded_payload["gasDrop"],
                    "cancel_fee": decoded_payload["cancelFee"],
                    "refund_fee": decoded_payload["refundFee"],
                    "deadline": decoded_payload["deadline"],
                    "dst_addr": decoded_payload["destAddr"],
                    "dst_chain": dst_chain,
                    "referrer_addr": decoded_payload["referrerAddr"],
                    "referrer_bps": decoded_payload["referrerBps"],
                    "auction_mode": decoded_payload["auctionMode"],
                    "random": decoded_payload["random"],
                }
            )
            return event
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e

    def handle_forwarded_eth(self, blockchain, event):
        func_name = "handle_forwarded_eth"

        event["token"] = self.populate_weth_token()

        try:
            return self.handle_forwarded(blockchain, event)
        except CustomException as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e

    def handle_forwarded_erc20(self, blockchain, event):
        func_name = "handle_forwarded_erc20"

        try:
            return self.handle_forwarded(blockchain, event)
        except CustomException as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e

    def handle_forwarded(self, blockchain, event):
        func_name = "handle_forwarded"

        try:
            if self.forwarded_repo.event_exists(event["transaction_hash"]):
                return None

            # Only interested in events from the Mayan Swift protocol (other alternatives
            # are WH Swap Bridge and Mayan MCTP, currently not supported)
            if event["mayanProtocol"] != "0xC38e4e6A15593f908255214653d3D947CA1c2338":
                return None

            decoded_payload = None

            # function signature for createOrderWithEth
            if event["protocolData"][:8] == "b866e173":
                from extractor.mayan.utils.MayanOrderParamsDecoder import MayanOrderParamsDecoder

                decoded_payload = MayanOrderParamsDecoder.decode(event["protocolData"][8:])

            # function signature for createOrderWithToken
            elif event["protocolData"][:8] == "8e8d142b":
                from extractor.mayan.utils.MayanOrderParamsDecoder import MayanOrderParamsDecoder

                decoded_payload = MayanOrderParamsDecoder.decode(event["protocolData"][136:])

            dst_chain = self.convert_id_to_blockchain_name(
                id=decoded_payload["destChainId"],
                blockchain_ids=BLOCKCHAIN_IDS,
            )

            if not dst_chain:
                return None

            self.forwarded_repo.create(
                {
                    "blockchain": blockchain,
                    "transaction_hash": event["transaction_hash"],
                    "token": event["token"],
                    "amount": event["amount"] if "amount" in event else None,
                    "mayan_protocol": event["mayanProtocol"],
                    "trader": decoded_payload["trader"],
                    "token_out": decoded_payload["tokenOut"],
                    "min_amount_out": decoded_payload["minAmountOut"],
                    "gas_drop": decoded_payload["gasDrop"],
                    "cancel_fee": decoded_payload["cancelFee"],
                    "refund_fee": decoded_payload["refundFee"],
                    "deadline": decoded_payload["deadline"],
                    "dst_addr": decoded_payload["destAddr"],
                    "dst_chain": dst_chain,
                    "referrer_addr": decoded_payload["referrerAddr"],
                    "referrer_bps": decoded_payload["referrerBps"],
                    "auction_mode": decoded_payload["auctionMode"],
                    "random": decoded_payload["random"],
                }
            )
            return event
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e

    def handle_order_created(self, blockchain, event):
        func_name = "handle_order_created"

        try:
            if self.order_created_repo.event_exists(event["key"]):
                return None

            self.order_created_repo.create(
                {
                    "blockchain": blockchain,
                    "transaction_hash": event["transaction_hash"],
                    "key": event["key"],
                }
            )
            return event
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e

    def handle_order_fulfilled(self, blockchain, event):
        func_name = "handle_order_fulfilled"

        try:
            if self.order_fulfilled_repo.event_exists(event["key"]):
                return None

            self.order_fulfilled_repo.create(
                {
                    "blockchain": blockchain,
                    "transaction_hash": event["transaction_hash"],
                    "key": event["key"],
                    "sequence": event["sequence"],
                    "net_amount": event["netAmount"],
                }
            )
            return event
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e

    def handle_order_unlocked(self, blockchain, event):
        func_name = "handle_order_unlocked"

        try:
            if self.order_unlocked_repo.event_exists(event["key"]):
                return None

            self.order_unlocked_repo.create(
                {
                    "blockchain": blockchain,
                    "transaction_hash": event["transaction_hash"],
                    "key": event["key"],
                }
            )
            return event
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e

    def populate_weth_token(self) -> str:
        return "0x0000000000000000000000000000000000000000"

    ### LOGIC FOR SOLANA ###

    def handle_solana_events(
        self,
        blockchain: str,
        start_signature: str,
        end_signature: str,
        decoded_transactions: Dict,
    ):
        included_txs = []

        for decoded_transaction in decoded_transactions:
            if (
                not decoded_transaction
                or decoded_transaction["transaction"]["meta"]["err"] is not None
            ):
                # Skip transactions with errors
                continue

            signature = decoded_transaction["transaction"]["transaction"]["signatures"][0]
            transaction_instructions = decoded_transaction["instructions"]

            mayan_instructions = [
                (idx, instr)
                for idx, instr in enumerate(transaction_instructions)
                if instr["programId"] in self.get_solana_bridge_program_ids()
            ]

            try:
                for idx, instruction in mayan_instructions:
                    included = False

                    if instruction["name"] == "initOrder":
                        transfer_instruction = None

                        if transaction_instructions[idx - 1]["name"] == "transfer":
                            transfer_instruction = transaction_instructions[idx - 1]
                        elif transaction_instructions[idx - 1]["name"] == "closeAccount":
                            transfer_instruction = transaction_instructions[idx - 2]

                        included = self.handle_init_order(
                            signature, transfer_instruction, instruction
                        )
                    elif instruction["name"] == "unlockBatch":
                        included = self.handle_unlock(
                            signature,
                            transaction_instructions[idx + 1],
                            instruction,
                        )
                    elif instruction["name"] == "unlock":
                        included = self.handle_unlock(
                            signature,
                            transaction_instructions[idx + 1],
                            instruction,
                        )
                    elif instruction["name"] == "fulfill":
                        if transaction_instructions[idx - 2]["name"] == "transferChecked":
                            transfer_instruction = transaction_instructions[idx - 2]
                        elif transaction_instructions[idx - 1]["name"] == "transfer":
                            transfer_instruction = transaction_instructions[idx - 1]

                        included = self.handle_fulfill(signature, transfer_instruction, instruction)
                    elif instruction["name"] == "settle":
                        included = self.handle_settle(
                            signature,
                            instruction,
                        )
                    elif instruction["name"] == "setAuctionWinner":
                        included = self.set_auction_winner(
                            signature,
                            instruction,
                        )
                    elif instruction["name"] == "registerOrder":
                        included = self.handle_register_order(
                            signature,
                            instruction,
                        )
                    elif instruction["name"] == "bid":
                        included = self.handle_auction_bid(
                            signature,
                            instruction,
                        )
                    elif instruction["name"] == "closeAuction":
                        included = self.handle_auction_close(
                            signature,
                            instruction,
                        )

                if included:
                    included_txs.append(decoded_transaction)

            except Exception as e:
                request_desc = (
                    f"Error processing request: {blockchain}, {start_signature}, "
                    f"{end_signature}.\n{e}"
                )
                log_error(self.bridge, request_desc)

        return included_txs

    def extract_accounts_from_instruction(
        self, instruction: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Extracts accounts from a Solana instruction.
        Args:
            instruction: The Solana instruction to extract accounts from.
        Returns:
            A list of accounts extracted from the instruction.
        """
        accounts = {}

        for account in instruction.get("accounts", []):
            if account["name"] not in accounts:
                accounts[account["name"]] = account["pubkey"]

        return accounts

    def handle_init_order(
        self, signature: str, transfer_instruction: Dict[str, Any], instruction: Dict[str, Any]
    ):
        func_name = "handle_init_order"

        account_data = self.extract_accounts_from_instruction(instruction)

        params = instruction["args"]["params"]

        try:
            order_hash = reconstruct_order_hash_from_params(
                trader=account_data["trader"],
                token_in=account_data["mintFrom"],
                src_chain_id=1,
                params=params,
            )

            if self.init_order_repo.event_exists(order_hash):
                return None

            dst_chain = self.convert_id_to_blockchain_name(
                id=params["chainDest"],
                blockchain_ids=BLOCKCHAIN_IDS,
            )

            if not dst_chain:
                return None

            # we need to extract the amount being sent to the order
            # by fetching the transfer instruction before the initOrder instruction
            if (
                transfer_instruction["name"] != "transfer"
                and transfer_instruction["name"] != "transferChecked"
            ):
                raise CustomException(
                    self.CLASS_NAME,
                    func_name,
                    f"Expected transfer instruction, got {transfer_instruction['name']}",
                )

            amount_in = int(transfer_instruction["args"]["amount"], 16)

            self.init_order_repo.create(
                {
                    "order_hash": order_hash,
                    "signature": signature,
                    "trader": account_data["trader"],
                    "relayer": account_data["relayer"],
                    "state": account_data["state"],
                    "state_from_acc": account_data["stateFromAcc"],
                    "relayer_fee_acc": account_data["relayerFeeAcc"],
                    "mint_from": account_data["mintFrom"],
                    "fee_manager_program": account_data["feeManagerProgram"],
                    "token_program": account_data["tokenProgram"],
                    "system_program": account_data["systemProgram"],
                    "amount_in_min": int(params["amountInMin"], 16),
                    "amount_in": amount_in,
                    "native_input": params["nativeInput"],
                    "fee_submit": int(params["feeSubmit"], 16),
                    "addr_dest": convert_32_byte_array_to_evm_address(params["addrDest"]),
                    "chain_dest": dst_chain,
                    "token_out": convert_32_byte_array_to_evm_address(params["tokenOut"]),
                    "amount_out_min": int(params["amountOutMin"], 16),
                    "gas_drop": int(params["gasDrop"], 16),
                    "fee_cancel": int(params["feeCancel"], 16),
                    "fee_refund": int(params["feeRefund"], 16),
                    "deadline": int(params["deadline"], 16),
                    "addr_ref": convert_32_byte_array_to_evm_address(params["addrRef"]),
                    "fee_rate_ref": params["feeRateRef"],
                    "fee_rate_mayan": params["feeRateMayan"],
                    "auction_mode": params["auctionMode"],
                    "key_rnd": bytes(params["keyRnd"]).hex(),
                }
            )

            return True

        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{'solana'} -- Tx Hash: {signature}. Error writing to DB: {e}",
            ) from e

    def handle_unlock(
        self, signature: str, transfer_instruction: Dict[str, Any], instruction: Dict[str, Any]
    ):
        func_name = "handle_unlock"

        account_data = self.extract_accounts_from_instruction(instruction)

        try:
            if self.unlock_repo.event_exists(account_data["stateFromAcc"]):
                return None

            if transfer_instruction["name"] != "transfer":
                raise CustomException(
                    self.CLASS_NAME,
                    func_name,
                    f"Expected transfer instruction, got {transfer_instruction['name']}",
                )

            amount = int(transfer_instruction["args"]["amount"], 16)

            self.unlock_repo.create(
                {
                    "signature": signature,
                    "vaa_unlock": account_data["vaaUnlock"],
                    "state": account_data["state"],
                    "state_from_acc": account_data["stateFromAcc"],
                    "mint_from": account_data["mintFrom"],
                    "driver": account_data["driver"],
                    "driver_acc": account_data["driverAcc"],
                    "token_program": account_data["tokenProgram"],
                    "system_program": account_data["systemProgram"],
                    "amount": amount,
                }
            )

            return True

        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{'solana'} -- Tx Hash: {signature}. Error writing to DB: {e}",
            ) from e

    def handle_fulfill(
        self, signature: str, transfer_instruction: Dict[str, Any], instruction: Dict[str, Any]
    ):
        func_name = "handle_fulfill"

        account_data = self.extract_accounts_from_instruction(instruction)

        addr_unlocker = convert_32_byte_array_to_solana_address(instruction["args"]["addrUnlocker"])

        try:
            if self.fulfill_repo.event_exists(signature):
                return None

            # we need to extract the amount being sent to the order
            # by fetching the transfer instruction before the initOrder instruction
            if (
                transfer_instruction["name"] != "transfer"
                and transfer_instruction["name"] != "transferChecked"
            ):
                raise CustomException(
                    self.CLASS_NAME,
                    func_name,
                    f"Expected transfer instruction, got {transfer_instruction['name']}",
                )

            amount_in = int(transfer_instruction["args"]["amount"], 16)

            self.fulfill_repo.create(
                {
                    "signature": signature,
                    "state": account_data["state"],
                    "driver": account_data["driver"],
                    "state_to_acc": account_data["stateToAcc"],
                    "mint_to": account_data["mintTo"],
                    "dest": account_data["dest"],
                    "system_program": account_data["systemProgram"],
                    "addr_unlocker": addr_unlocker,
                    "amount": amount_in,
                }
            )

            return True

        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{'solana'} -- Tx Hash: {signature}. Error writing to DB: {e}",
            ) from e

    def handle_settle(self, signature: str, instruction: Dict[str, Any]):
        func_name = "handle_settle"

        account_data = self.extract_accounts_from_instruction(instruction)

        try:
            if self.settle_repo.event_exists(signature):
                return None

            self.settle_repo.create(
                {
                    "signature": signature,
                    "state": account_data["state"],
                    "state_to_acc": account_data.get("stateToAcc"),
                    "relayer": account_data.get("relayer"),
                    "mint_to": account_data.get("mintTo"),
                    "dest": account_data.get("dest"),
                    "referrer": account_data.get("referrer"),
                    "fee_collector": account_data.get("feeCollector"),
                    "referrer_fee_acc": account_data.get("referrerFeeAcc"),
                    "mayan_fee_acc": account_data.get("mayanFeeAcc"),
                    "dest_acc": account_data.get("destAcc"),
                    "token_program": account_data.get("tokenProgram"),
                    "system_program": account_data.get("systemProgram"),
                    "associated_token_program": account_data.get("associatedTokenProgram"),
                }
            )

            return True

        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{'solana'} -- Tx Hash: {signature}. Error writing to DB: {e}",
            ) from e

    def set_auction_winner(self, signature: str, instruction: Dict[str, Any]):
        func_name = "set_auction_winner"

        account_data = self.extract_accounts_from_instruction(instruction)

        try:
            if self.set_auction_winner_repo.event_exists(signature):
                return None

            expected_winner = instruction["args"]["expectedWinner"]

            self.set_auction_winner_repo.create(
                {
                    "signature": signature,
                    "state": account_data["state"],
                    "auction": account_data["auction"],
                    "expected_winner": expected_winner,
                }
            )

            return True

        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{'solana'} -- Tx Hash: {signature}. Error writing to DB: {e}",
            ) from e

    def handle_register_order(self, signature: str, instruction: Dict[str, Any]):
        func_name = "handle_register_order"

        account_data = self.extract_accounts_from_instruction(instruction)

        params = instruction["args"]["args"]

        try:
            order_hash = reconstruct_order_hash_from_params(
                trader=convert_32_byte_array_to_evm_address(params["trader"]),
                token_in=convert_32_byte_array_to_evm_address(params["tokenIn"]),
                src_chain_id=params["chainSource"],
                params=params,
            )

            if self.register_order_repo.event_exists(order_hash):
                return None

            src_chain = self.convert_id_to_blockchain_name(
                id=params["chainSource"],
                blockchain_ids=BLOCKCHAIN_IDS,
            )

            dst_chain = self.convert_id_to_blockchain_name(
                id=params["chainDest"],
                blockchain_ids=BLOCKCHAIN_IDS,
            )

            if not src_chain or not dst_chain:
                return None

            self.register_order_repo.create(
                {
                    "order_hash": order_hash,
                    "signature": signature,
                    "relayer": account_data["relayer"],
                    "state": account_data["state"],
                    "system_program": account_data["systemProgram"],
                    "trader": convert_32_byte_array_to_evm_address(params["trader"]),
                    "chain_source": src_chain,
                    "token_in": convert_32_byte_array_to_evm_address(params["tokenIn"]),
                    "addr_dest": convert_32_byte_array_to_solana_address(params["addrDest"]),
                    "chain_dest": dst_chain,
                    "token_out": convert_32_byte_array_to_solana_address(params["tokenOut"]),
                    "amount_out_min": int(params["amountOutMin"], 16),
                    "gas_drop": int(params["gasDrop"], 16),
                    "fee_cancel": int(params["feeCancel"], 16),
                    "fee_refund": int(params["feeRefund"], 16),
                    "deadline": int(params["deadline"], 16),
                    "addr_ref": convert_32_byte_array_to_solana_address(params["addrRef"]),
                    "fee_rate_ref": params["feeRateRef"],
                    "fee_rate_mayan": params["feeRateMayan"],
                    "auction_mode": params["auctionMode"],
                    "key_rnd": bytes(params["keyRnd"]).hex(),
                }
            )

            return True

        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{'solana'} -- Tx Hash: {signature}. Error writing to DB: {e}",
            ) from e

    def handle_auction_bid(self, signature: str, instruction: Dict[str, Any]):
        func_name = "handle_auction_bid"

        account_data = self.extract_accounts_from_instruction(instruction)

        params = instruction["args"]["order"]

        try:
            src_chain = self.convert_id_to_blockchain_name(
                id=params["chainSource"],
                blockchain_ids=BLOCKCHAIN_IDS,
            )

            dst_chain = self.convert_id_to_blockchain_name(
                id=params["chainDest"],
                blockchain_ids=BLOCKCHAIN_IDS,
            )

            if not src_chain or not dst_chain:
                return None

            trader = (
                convert_32_byte_array_to_solana_address(params["trader"])
                if src_chain == "solana"
                else convert_32_byte_array_to_evm_address(params["trader"])
            )
            token_in = (
                convert_32_byte_array_to_solana_address(params["tokenIn"])
                if src_chain == "solana"
                else convert_32_byte_array_to_evm_address(params["tokenIn"])
            )
            addr_dest = (
                convert_32_byte_array_to_solana_address(params["addrDest"])
                if dst_chain == "solana"
                else convert_32_byte_array_to_evm_address(params["addrDest"])
            )
            token_out = (
                convert_32_byte_array_to_solana_address(params["tokenOut"])
                if dst_chain == "solana"
                else convert_32_byte_array_to_evm_address(params["tokenOut"])
            )
            addr_ref = (
                convert_32_byte_array_to_solana_address(params["addrRef"])
                if dst_chain == "solana"
                else convert_32_byte_array_to_evm_address(params["addrRef"])
            )

            order_hash = reconstruct_order_hash_from_params(
                trader=trader,
                token_in=token_in,
                src_chain_id=params["chainSource"],
                params=params,
            )

            if self.auction_bid_repo.event_exists(order_hash):
                return None

            self.auction_bid_repo.create(
                {
                    "order_hash": order_hash,
                    "signature": signature,
                    "config": account_data["config"],
                    "driver": account_data["driver"],
                    "auction_state": account_data["auctionState"],
                    "system_program": account_data["systemProgram"],
                    "trader": trader,
                    "chain_source": src_chain,
                    "token_in": token_in,
                    "addr_dest": addr_dest,
                    "chain_dest": dst_chain,
                    "token_out": token_out,
                    "amount_out_min": int(params["amountOutMin"], 16),
                    "gas_drop": int(params["gasDrop"], 16),
                    "fee_cancel": int(params["feeCancel"], 16),
                    "fee_refund": int(params["feeRefund"], 16),
                    "deadline": int(params["deadline"], 16),
                    "addr_ref": addr_ref,
                    "fee_rate_ref": params["feeRateRef"],
                    "fee_rate_mayan": params["feeRateMayan"],
                    "auction_mode": params["auctionMode"],
                    "key_rnd": bytes(params["keyRnd"]).hex(),
                    "amount_bid": int(instruction["args"]["amountBid"], 16),
                }
            )

            return True

        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{'solana'} -- Tx Hash: {signature}. Error writing to DB: {e}",
            ) from e

    def handle_auction_close(self, signature: str, instruction: Dict[str, Any]):
        func_name = "handle_auction_close"

        account_data = self.extract_accounts_from_instruction(instruction)

        try:
            if self.auction_close_repo.event_exists(account_data["auction"]):
                return None

            self.auction_close_repo.create(
                {
                    "signature": signature,
                    "auction": account_data["auction"],
                    "initializer": account_data["initializer"],
                }
            )

            return True

        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{'solana'} -- Tx Hash: {signature}. Error writing to DB: {e}",
            ) from e
