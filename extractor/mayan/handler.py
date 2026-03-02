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
from repository.mayan.models import MayanBlockchainTransaction, MayanOrderFulfilled
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
    CliColor,
    CustomException,
    build_log_message_generator,
    convert_32_byte_array_to_evm_address,
    convert_32_byte_array_to_solana_address,
    log_error,
    log_to_cli,
    unpad_address,
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

        event["tokenIn"] = self.populate_native_token()

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

        event["token"] = self.populate_native_token()

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
                    "middle_dst_token": None,
                    "middle_dst_amount": None,
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

    def populate_native_token(self) -> str:
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
                        swap_instructions = [
                            instr
                            for instr in transaction_instructions
                            if instr["name"] == "SwapEvent"
                        ]

                        swap_instruction = MayanHandler.resolve_swaps(signature, swap_instructions)

                        if transaction_instructions[idx - 1]["name"] == "transfer":
                            transfer_instruction = transaction_instructions[idx - 1]
                        elif transaction_instructions[idx - 1]["name"] == "closeAccount":
                            transfer_instruction = transaction_instructions[idx - 2]
                        elif transaction_instructions[idx - 2]["name"] == "transfer":
                            transfer_instruction = transaction_instructions[idx - 2]
                        elif transaction_instructions[idx - 4]["name"] == "closeAccount":
                            transfer_instruction = transaction_instructions[idx - 4]
                        elif transaction_instructions[idx - 4]["name"] == "transfer":
                            transfer_instruction = transaction_instructions[idx - 4]
                        elif transaction_instructions[idx - 3]["name"] == "transferChecked":
                            transfer_instruction = transaction_instructions[idx - 3]

                        included = self.handle_init_order(
                            signature, transfer_instruction, instruction, swap_instruction
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
                        transfer_instruction = None
                        swap_instructions = [
                            instr
                            for instr in transaction_instructions
                            if instr["name"] == "SwapEvent"
                        ]

                        swap_instruction = MayanHandler.resolve_swaps(signature, swap_instructions)

                        if transaction_instructions[idx - 2]["name"] == "transferChecked":
                            transfer_instruction = transaction_instructions[idx - 2]
                        elif transaction_instructions[idx - 1]["name"] == "transfer":
                            transfer_instruction = transaction_instructions[idx - 1]
                        elif transaction_instructions[idx - 1]["name"] == "transferChecked":
                            transfer_instruction = transaction_instructions[idx - 1]

                        included = self.handle_fulfill(
                            signature, transfer_instruction, instruction, swap_instruction
                        )
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
        self,
        signature: str,
        transfer_instruction: Dict[str, Any],
        instruction: Dict[str, Any],
        swap_event: Dict[str, Any],
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

            if swap_event:
                original_src_token = swap_event["args"]["input_mint"]
                original_src_amount = int(swap_event["args"]["input_amount"], 16)
                amm = None

                middle_src_token = swap_event["args"]["output_mint"]
                middle_src_amount = int(swap_event["args"]["output_amount"], 16)
            else:
                original_src_token = account_data["mintFrom"]
                original_src_amount = amount_in
                amm = None

                middle_src_amount = None
                middle_src_token = None

            self.init_order_repo.create(
                {
                    "order_hash": order_hash,
                    "signature": signature,
                    "trader": account_data["trader"],
                    "relayer": account_data["relayer"],
                    "state": account_data["state"],
                    "state_from_acc": account_data["stateFromAcc"],
                    "relayer_fee_acc": account_data["relayerFeeAcc"],
                    "middle_src_token": middle_src_token,
                    "fee_manager_program": account_data["feeManagerProgram"],
                    "token_program": account_data["tokenProgram"],
                    "system_program": account_data["systemProgram"],
                    "middle_src_amount_min": int(params["amountInMin"], 16),
                    "middle_src_amount": middle_src_amount,
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
                    "original_src_token": original_src_token,
                    "original_src_amount": original_src_amount,
                    "amm": amm,
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
        self,
        signature: str,
        transfer_instruction: Dict[str, Any],
        instruction: Dict[str, Any],
        swap_event: Dict[str, Any],
    ):
        func_name = "handle_fulfill"

        account_data = self.extract_accounts_from_instruction(instruction)

        addr_unlocker = convert_32_byte_array_to_solana_address(instruction["args"]["addrUnlocker"])

        try:
            if self.fulfill_repo.event_exists(signature):
                return None

            if swap_event:
                middle_dst_token = swap_event["args"]["input_mint"]
                middle_dst_amount = int(swap_event["args"]["input_amount"], 16)
                amm = None

                final_amount = int(swap_event["args"]["output_amount"], 16)
            else:
                middle_dst_token = None
                middle_dst_amount = None
                amm = None

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

                final_amount = amount_in

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
                    "amount": final_amount,
                    "middle_dst_token": middle_dst_token,
                    "middle_dst_amount": middle_dst_amount,
                    "amm": amm,
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

            if self.auction_bid_repo.event_exists(signature):
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

    def post_processing(self):
        """
        Post-process fulfill transactions in EVM to extract middle token and amount from input data.
        These are needed when swaps occur and are not emitted in the event.
        """
        func_name = "post_processing"

        try:
            # Get all fulfill orders + their input data in a single query
            with self.order_fulfilled_repo.get_session() as session:
                results = (
                    session.query(
                        MayanOrderFulfilled.key,
                        MayanOrderFulfilled.transaction_hash,
                        MayanOrderFulfilled.middle_dst_token,
                        MayanOrderFulfilled.middle_dst_amount,
                        MayanBlockchainTransaction.input_data,
                    )
                    .join(
                        MayanBlockchainTransaction,
                        MayanBlockchainTransaction.transaction_hash
                        == MayanOrderFulfilled.transaction_hash,
                    )
                    .all()
                )

            updates = []
            for key, tx_hash, token, amount, input_data in results:
                log_to_cli(
                    build_log_message_generator(
                        self.bridge,
                        (f"Post-processing fulfill order: {key} -- Tx Hash: {tx_hash} "),
                    ),
                    CliColor.INFO,
                )

                if not input_data or token is not None or amount is not None:
                    continue

                try:
                    function_selector = input_data[:10]

                    if function_selector == "0xbc127b88":  # fulfillWithERC20
                        token_in = unpad_address(input_data[10:74])
                        amount_in = int(input_data[74:138], 16)

                        updates.append((key, token_in, amount_in))

                    elif function_selector == "0x1c5cf072":  # fulfillWithETH
                        token_in = self.populate_native_token()
                        amount_in = int(input_data[10:74], 16)

                        updates.append((key, token_in, amount_in))

                    elif (
                        function_selector == "0x488c3591" or function_selector == "0x6befa3a5"
                    ):  # fulfillOrder or directFulfill
                        # we skip because these functions do not have middle token or amount
                        continue

                    else:
                        err = CustomException(
                            self.CLASS_NAME,
                            func_name,
                            (
                                f"{self.bridge} -- Tx Hash: {tx_hash}. Unknown function ",
                                f"selector: {function_selector}",
                            ),
                        )
                        log_error(self.bridge, str(err))

                except Exception as decode_err:
                    err = CustomException(
                        self.CLASS_NAME,
                        func_name,
                        (
                            f"{self.bridge} -- Tx Hash: {tx_hash}. Error decoding input ",
                            f"data: {decode_err}",
                        ),
                    )
                    log_error(self.bridge, str(err))
                    continue

            # Batch update
            total = len(updates)
            for idx, (key, middle_token, middle_amount) in enumerate(updates):
                # print progress
                log_to_cli(
                    build_log_message_generator(
                        self.bridge,
                        (
                            f"Updating fulfill order info: {key} "
                            f"-- {idx + 1}/{total} ({(idx + 1) / total * 100:.2f}%)",
                        ),
                    ),
                    CliColor.INFO,
                )

                self.order_fulfilled_repo.update_middle_info_order_fulfilled(
                    key,
                    middle_token,
                    middle_amount,
                )

        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{self.bridge} -- Error during post-processing: {e}",
            ) from e

    @staticmethod
    def resolve_swaps(signature, swap):
        func_name = "resolve_swaps"

        if not swap or not isinstance(swap, list):
            return None

        counter = 0
        while True:
            aggregated = MayanHandler.aggregate_swap_instructions(swap)

            resolved = MayanHandler.resolve_swap_chain(aggregated)

            if len(resolved) == 1:
                # If there's only one swap, we can stop resolving
                break
            else:
                swap = resolved
                counter += 1

            if counter > 10:
                # Prevent infinite loops. 10 iterations should be enough to resolve any swap chain.
                break

        if len(resolved) == 1:
            item = resolved[0]
            return {
                "args": {
                    "input_mint": item["args"]["input_mint"],
                    "output_mint": item["args"]["output_mint"],
                    "input_amount": item["args"]["input_amount"],
                    "output_amount": item["args"]["output_amount"],
                }
            }
        else:
            err = CustomException(
                MayanHandler.CLASS_NAME,
                func_name,
                f"Expected one aggregated swap, got {len(aggregated)} swaps in {signature}",
            )
            log_error(
                MayanHandler.CLASS_NAME,
                str(err),
            )
            raise err

    @staticmethod
    def aggregate_swap_instructions(swap):
        func_name = "aggregate_swap_instructions"

        if not swap or not isinstance(swap, list):
            return None

        if len(swap) == 1:
            # If there's only one swap, return it as is
            return swap

        try:
            # Step 2: aggregate same (input_mint, output_mint) swaps
            aggregated = {}
            for s in swap:
                input_mint = s["args"]["input_mint"]
                output_mint = s["args"]["output_mint"]
                input_amount = int(s["args"]["input_amount"], 16)
                output_amount = int(s["args"]["output_amount"], 16)

                key = (input_mint, output_mint)
                if key not in aggregated:
                    aggregated[key] = {"input_amount": input_amount, "output_amount": output_amount}
                else:
                    aggregated[key]["input_amount"] += input_amount
                    aggregated[key]["output_amount"] += output_amount

            # return a list of aggregated swaps
            return [
                {
                    "args": {
                        "input_mint": key[0],
                        "output_mint": key[1],
                        "input_amount": hex(value["input_amount"]),
                        "output_amount": hex(value["output_amount"]),
                    }
                }
                for key, value in aggregated.items()
            ]

        except Exception as e:
            raise CustomException(
                MayanHandler.CLASS_NAME,
                func_name,
                f"Error aggregating swap instructions: {e}",
            ) from e

    @staticmethod
    def resolve_swap_chain(swap):
        func_name = "resolve_swap_chain"
        try:
            if not swap or not isinstance(swap, list):
                return []

            if len(swap) == 1:
                # If there's only one swap, return it as is
                return swap

            # Build map from (input_mint, input_amount) → swap
            input_map = {}
            for s in swap:
                key = (s["args"]["input_mint"], int(s["args"]["input_amount"], 16))
                input_map[key] = s

            used = set()
            chains = []

            for s in swap:
                if id(s) in used:
                    continue

                chain = [s]
                used.add(id(s))
                current_swap = s

                while True:
                    output_mint = current_swap["args"]["output_mint"]
                    output_amount = int(current_swap["args"]["output_amount"], 16)
                    next_key = (output_mint, output_amount)
                    next_swap = input_map.get(next_key)
                    if next_swap and id(next_swap) not in used:
                        chain.append(next_swap)
                        used.add(id(next_swap))
                        current_swap = next_swap
                    else:
                        break

                # Reduce this chain
                input_mint = chain[0]["args"]["input_mint"]
                output_mint = chain[-1]["args"]["output_mint"]
                input_amount = int(chain[0]["args"]["input_amount"], 16)
                output_amount = int(chain[-1]["args"]["output_amount"], 16)

                chains.append(
                    {
                        "args": {
                            "input_mint": input_mint,
                            "output_mint": output_mint,
                            "input_amount": hex(input_amount),
                            "output_amount": hex(output_amount),
                        }
                    }
                )

            return chains
        except Exception as e:
            raise CustomException(
                MayanHandler.CLASS_NAME,
                func_name,
                f"Error resolving swap chain: {e}",
            ) from e
