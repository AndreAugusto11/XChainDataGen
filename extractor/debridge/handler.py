from typing import Any, Dict, List

from config.constants import Bridge
from extractor.base_handler import BaseHandler
from extractor.debridge.constants import BLOCKCHAIN_IDS, BRIDGE_CONFIG, SOLANA_PROGRAM_ADDRESSES
from extractor.mayan.handler import MayanHandler
from repository.database import DBSession
from repository.debridge.models import (
    DeBridgeBlockchainTransaction,
    DeBridgeCreatedOrder,
    DeBridgeFulfilledOrder,
)
from repository.debridge.repository import (
    DeBridgeBlockchainTransactionRepository,
    DeBridgeClaimedUnlockRepository,
    DeBridgeCreatedOrderRepository,
    DeBridgeFulfilledOrderRepository,
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


class DebridgeHandler(BaseHandler):
    CLASS_NAME = "DebridgeHandler"

    def __init__(self, rpc_client: EvmRPCClient, blockchains: list) -> None:
        super().__init__(rpc_client, blockchains)
        self.bridge = Bridge.DEBRIDGE

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
        self.blockchain_transaction_repo = DeBridgeBlockchainTransactionRepository(DBSession)
        self.created_order_repo = DeBridgeCreatedOrderRepository(DBSession)
        self.fulfilled_order_repo = DeBridgeFulfilledOrderRepository(DBSession)
        self.claimed_unlock_repo = DeBridgeClaimedUnlockRepository(DBSession)

    def handle_transactions(self, transactions: List[Dict[str, Any]]) -> None:
        func_name = "handle_transactions"
        try:
            self.blockchain_transaction_repo.create_all(transactions)
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"Error writing transactions to database: {e}",
            ) from e

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
                    == "0xfc8703fd57380f9dd234a89dce51333782d49c5902f307b02f03e014d18fe471"
                ):  # CreatedOrder
                    event = self.handle_created_order(blockchain, event)
                elif (
                    event["topic"]
                    == "0xd281ee92bab1446041582480d2c0a9dc91f855386bb27ea295faac1e992f7fe4"
                ):  # FulfilledOrder
                    event = self.handle_fulfilled_order(blockchain, event)
                elif (
                    event["topic"]
                    == "0x33fff3d864e92b6e1ef9e830196fc019c946104ea621b833aaebd3c3e84b2f6f"
                ):  # ClaimedUnlock
                    event = self.handle_claimed_unlock(blockchain, event)

                if event:
                    included_events.append(event)

            except CustomException as e:
                request_desc = (
                    f"Error processing request: {blockchain}, {start_block}, "
                    f"{end_block}, {contract}, {topics}.\n{e}"
                )
                log_error(self.bridge, request_desc)

        return included_events

    def handle_created_order(self, blockchain, event):
        func_name = "handle_created_order"

        obj = event[
            "(makerOrderNonce,makerSrc,giveChainId,giveTokenAddress,giveAmount,takeChainId,takeTokenAddress,takeAmount,receiverDst,givePatchAuthoritySrc,orderAuthorityAddressDst,allowedTakerDst,allowedCancelBeneficiarySrc,externalCall)"
        ]

        src_blockchain = self.convert_id_to_blockchain_name(obj[2])
        dst_blockchain = self.convert_id_to_blockchain_name(obj[5])

        if src_blockchain is None or dst_blockchain is None:
            return None

        try:
            if self.created_order_repo.event_exists(obj[0]):
                return None

            self.created_order_repo.create(
                {
                    "blockchain": blockchain,
                    "transaction_hash": event["transaction_hash"],
                    "maker_order_nonce": obj[0],
                    "maker_src": unpad_address(obj[1]),
                    "src_blockchain": src_blockchain,
                    "give_token_address": unpad_address(obj[3]),
                    "give_amount": obj[4],
                    "dst_blockchain": dst_blockchain,
                    "take_token_address": unpad_address(obj[6]),
                    "take_amount": obj[7],
                    "receiver_dst": unpad_address(obj[8]),
                    "give_patch_authority_src": unpad_address(obj[9]),
                    "order_authority_address_dst": unpad_address(obj[10]),
                    "allowed_taker_dst": unpad_address(obj[11]),
                    "allowed_cancel_beneficiary_src": obj[12],
                    "external_call": obj[13],
                    "order_id": event["orderId"],
                    "affiliate_fee": event.get("affiliateFee"),
                    "native_fix_fee": event["nativeFixFee"],
                    "percent_fee": event["percentFee"],
                    "referral_code": event["referralCode"],
                    "_metadata": event.get("metadata"),
                    "original_token": None,
                    "original_amount": None,
                }
            )
            return event
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e

    def handle_fulfilled_order(self, blockchain, event):
        func_name = "handle_fulfilled_order"

        obj = event[
            "(makerOrderNonce,makerSrc,giveChainId,giveTokenAddress,giveAmount,takeChainId,takeTokenAddress,takeAmount,receiverDst,givePatchAuthoritySrc,orderAuthorityAddressDst,allowedTakerDst,allowedCancelBeneficiarySrc,externalCall)"
        ]

        src_blockchain = self.convert_id_to_blockchain_name(obj[2])
        dst_blockchain = self.convert_id_to_blockchain_name(obj[5])

        if src_blockchain is None or dst_blockchain is None:
            return None

        try:
            if self.fulfilled_order_repo.event_exists(event["orderId"]):
                return None

            self.fulfilled_order_repo.create(
                {
                    "blockchain": blockchain,
                    "transaction_hash": event["transaction_hash"],
                    "maker_order_nonce": obj[0],
                    "maker_src": unpad_address(obj[1]),
                    "src_blockchain": src_blockchain,
                    "give_token_address": unpad_address(obj[3]),
                    "give_amount": obj[4],
                    "dst_blockchain": dst_blockchain,
                    "take_token_address": unpad_address(obj[6]),
                    "take_amount": obj[7],
                    "receiver_dst": unpad_address(obj[8]),
                    "give_patch_authority_src": unpad_address(obj[9]),
                    "order_authority_address_dst": unpad_address(obj[10]),
                    "allowed_taker_dst": unpad_address(obj[11]),
                    "allowed_cancel_beneficiary_src": unpad_address(obj[12]),
                    "external_call": unpad_address(obj[13]),
                    "order_id": event["orderId"],
                    "sender": unpad_address(event["sender"]),
                    "unlock_authority": unpad_address(event["unlockAuthority"]),
                    "taker": None,
                }
            )
            return event
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e

    def handle_claimed_unlock(self, blockchain, event):
        func_name = "handle_claimed_unlock"

        try:
            if self.claimed_unlock_repo.event_exists(event["orderId"]):
                return None

            self.claimed_unlock_repo.create(
                {
                    "blockchain": blockchain,
                    "transaction_hash": event["transaction_hash"],
                    "order_id": event["orderId"],
                    "beneficiary": unpad_address(event["beneficiary"]),
                    "give_amount": event["giveAmount"],
                    "give_token_address": unpad_address(event["giveTokenAddress"]),
                    "fee": None,
                }
            )
            return event
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e

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

            debridge_instructions = [
                (idx, instr)
                for idx, instr in enumerate(transaction_instructions)
                if instr["programId"] in self.get_solana_bridge_program_ids()
            ]

            try:
                for idx, instruction in debridge_instructions:
                    included = False

                    if instruction["name"] == "create_order_with_nonce":
                        transfer_instruction = None
                        swap_instructions = [
                            instr
                            for instr in transaction_instructions
                            if instr["name"] == "SwapEvent"
                        ]

                        swap_instruction = MayanHandler.resolve_swaps(signature, swap_instructions)

                        fee_transfer_instruction = None
                        i = 1

                        while (
                            fee_transfer_instruction is None
                            or fee_transfer_instruction["name"] != "transfer"
                        ):
                            fee_transfer_instruction = transaction_instructions[idx + i]
                            i += 1

                        transfer_instruction = None

                        i = 6
                        while (
                            transfer_instruction is None
                            or transfer_instruction["name"] != "transfer"
                        ):
                            transfer_instruction = transaction_instructions[idx + i]
                            i += 1

                        included = self.handle_create_order_with_nonce(
                            signature,
                            fee_transfer_instruction,
                            transfer_instruction,
                            instruction,
                            swap_instruction,
                        )

                    elif instruction["name"] == "fulfill_order":
                        included = self.handle_fulfill_order(signature, instruction)

                    if instruction["name"] == "claim_unlock":
                        fee_transfer_instruction = transaction_instructions[idx + 1]
                        refund_transfer_instruction = transaction_instructions[idx + 2]

                        included = self.handle_claim_unlock(
                            signature,
                            instruction,
                            fee_transfer_instruction,
                            refund_transfer_instruction,
                        )

                if included:
                    included_txs.append(decoded_transaction)

            except CustomException as e:
                request_desc = (
                    f"Error processing request: {blockchain}, {start_signature}, "
                    f"{end_signature}.\n{e}"
                )
                log_error(self.bridge, request_desc)

        return included_txs

    def handle_create_order_with_nonce(
        self,
        signature: str,
        fee_transfer_instruction: Dict,
        transfer_instruction: Dict,
        instruction: Dict,
        swap_event: Dict,
    ) -> bool:
        func_name = "handle_create_order_with_nonce"

        account_data = self.extract_accounts_from_instruction(instruction)

        order_args = instruction["args"]["order_args"]

        try:
            if self.created_order_repo.event_exists(int(instruction["args"]["nonce"], 16)):
                return False

            dst_chain_id = int.from_bytes(order_args["take"]["chain_id"], byteorder="big")
            dst_blockchain = self.convert_id_to_blockchain_name(dst_chain_id)

            if dst_blockchain is None:
                return False

            if swap_event:
                original_src_token = swap_event["args"]["input_mint"]
                original_src_amount = int(swap_event["args"]["input_amount"], 16)

                middle_src_token = swap_event["args"]["output_mint"]
                middle_src_amount = int(swap_event["args"]["output_amount"], 16)
            else:
                # we need to extract the amount being sent to the order
                # by fetching the transfer instruction before the initOrder instruction
                if (
                    transfer_instruction["name"] != "transfer"
                    and transfer_instruction["name"] != "transferChecked"
                ):
                    raise CustomException(
                        self.CLASS_NAME,
                        func_name,
                        (
                            "Expected transfer instruction. "
                            f"Got {transfer_instruction['name']} in tx {signature}"
                        ),
                    )

                amount_in = int(transfer_instruction["args"]["amount"], 16)

                original_src_token = account_data["token_mint"]
                original_src_amount = amount_in

                middle_src_amount = None
                middle_src_token = None

            fee_amount = int(fee_transfer_instruction["args"]["lamports"], 16)

            self.created_order_repo.create(
                {
                    "blockchain": "solana",
                    "transaction_hash": signature,
                    "maker_order_nonce": int(instruction["args"]["nonce"], 16),
                    "maker_src": account_data["maker"],
                    "src_blockchain": "solana",
                    "give_token_address": middle_src_token
                    if middle_src_token
                    else original_src_token,
                    "give_amount": middle_src_amount if middle_src_amount else original_src_amount,
                    "dst_blockchain": dst_blockchain,
                    "take_token_address": convert_32_byte_array_to_evm_address(
                        order_args["take"]["token_address"]["data"]
                    ),
                    "take_amount": int.from_bytes(order_args["take"]["amount"], byteorder="big"),
                    "receiver_dst": convert_32_byte_array_to_evm_address(
                        order_args["receiver_dst"]["data"]
                    ),
                    "give_patch_authority_src": order_args["give_patch_authority_src"],
                    "order_authority_address_dst": convert_32_byte_array_to_evm_address(
                        order_args["order_authority_address_dst"]["data"]
                    ),
                    "allowed_taker_dst": convert_32_byte_array_to_evm_address(
                        order_args["allowed_taker_dst"]["data"]
                    )
                    if order_args["allowed_taker_dst"]
                    else None,
                    "allowed_cancel_beneficiary_src": order_args["allowed_cancel_beneficiary_src"],
                    "external_call": order_args["external_call"]["data"]
                    if order_args["external_call"]
                    else None,
                    "order_id": None,
                    "affiliate_fee": None,
                    "native_fix_fee": fee_amount,
                    "percent_fee": None,
                    "referral_code": instruction["args"]["referral_code"],
                    "_metadata": bytes(instruction["args"]["metadata"]["data"]).hex(),
                    "original_token": original_src_token,
                    "original_amount": original_src_amount,
                }
            )

            return True

        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"Solana -- Tx Signature: {signature}. Error writing to DB: {e}",
            ) from e

    def handle_claim_unlock(
        self,
        signature: str,
        instruction: Dict,
        fee_transfer_instruction: Dict,
        refund_transfer_instruction: Dict,
    ) -> bool:
        func_name = "handle_claim_unlock"

        account_data = self.extract_accounts_from_instruction(instruction)

        try:
            order_id = bytes(instruction["args"]["order_id"]).hex()

            if self.claimed_unlock_repo.event_exists(order_id):
                return False

            fee_amount = int(fee_transfer_instruction["args"]["amount"], 16)
            refund_amount = int(refund_transfer_instruction["args"]["amount"], 16)

            self.claimed_unlock_repo.create(
                {
                    "blockchain": "solana",
                    "transaction_hash": signature,
                    "order_id": order_id,
                    "beneficiary": account_data["action_beneficiary"],
                    "give_amount": refund_amount,
                    "give_token_address": account_data["token_mint"],
                    "fee": fee_amount,
                }
            )

            return True
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"Solana -- Tx Signature: {signature}. Error writing to DB: {e}",
            ) from e

    def handle_fulfill_order(self, signature: str, instruction: Dict) -> bool:
        func_name = "handle_fulfill_order"

        account_data = self.extract_accounts_from_instruction(instruction)

        try:
            order_id = bytes(instruction["args"]["order_id"]).hex()

            if self.fulfilled_order_repo.event_exists(order_id):
                return False

            src_chain_id = int.from_bytes(
                instruction["args"]["unvalidated_order"]["give"]["chain_id"], byteorder="big"
            )
            source_blockchain = self.convert_id_to_blockchain_name(src_chain_id)

            if not source_blockchain:
                return False

            unvalidated_order = instruction["args"]["unvalidated_order"]

            self.fulfilled_order_repo.create(
                {
                    "blockchain": "solana",
                    "transaction_hash": signature,
                    "maker_order_nonce": int(unvalidated_order["maker_order_nonce"], 16),
                    "maker_src": convert_32_byte_array_to_evm_address(
                        unvalidated_order["maker_src"]["data"]
                    ),
                    "src_blockchain": source_blockchain,
                    "give_token_address": convert_32_byte_array_to_evm_address(
                        unvalidated_order["give"]["token_address"]["data"]
                    ),
                    "give_amount": int.from_bytes(
                        unvalidated_order["give"]["amount"], byteorder="big"
                    ),
                    "dst_blockchain": "solana",
                    "take_token_address": convert_32_byte_array_to_solana_address(
                        unvalidated_order["take"]["token_address"]["data"]
                    ),
                    "take_amount": int.from_bytes(
                        unvalidated_order["take"]["amount"], byteorder="big"
                    ),
                    "receiver_dst": convert_32_byte_array_to_solana_address(
                        unvalidated_order["receiver_dst"]["data"]
                    ),
                    "give_patch_authority_src": convert_32_byte_array_to_evm_address(
                        unvalidated_order["give_patch_authority_src"]["data"]
                    ),
                    "order_authority_address_dst": convert_32_byte_array_to_solana_address(
                        unvalidated_order["order_authority_address_dst"]["data"]
                    ),
                    "allowed_taker_dst": convert_32_byte_array_to_solana_address(
                        unvalidated_order["allowed_taker_dst"]["data"]
                    )
                    if unvalidated_order["allowed_taker_dst"]
                    else None,
                    "allowed_cancel_beneficiary_src": convert_32_byte_array_to_evm_address(
                        unvalidated_order["allowed_cancel_beneficiary_src"]["data"]
                    )
                    if unvalidated_order["allowed_cancel_beneficiary_src"]
                    else None,
                    "external_call": convert_32_byte_array_to_evm_address(
                        unvalidated_order["external_call"]["external_call_shortcut"]
                    )
                    if unvalidated_order["external_call"]
                    else None,
                    "order_id": order_id,
                    "sender": None,
                    "unlock_authority": instruction["args"]["unlock_authority"],
                    "taker": account_data["taker"],
                }
            )

            return True
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"Solana -- Tx Signature: {signature}. Error writing to DB: {e}",
            ) from e

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

    def convert_id_to_blockchain_name(self, id: str) -> str:
        id = str(id)

        # Discard smaller blockchains as we focus on the ones with more transferred value
        # see list here https://docs.debridge.finance/the-debridge-messaging-protocol/fees-and-supported-chains
        if id.startswith("1000000"):
            return None

        return super().convert_id_to_blockchain_name(id, BLOCKCHAIN_IDS)

    def post_processing(self):
        """
        Post-process fulfill transactions in EVM to extract middle token and amount from input data.
        These are needed when swaps occur and are not emitted in the event.
        """
        func_name = "post_processing"

        try:
            # Get all fulfill orders + their input data in a single query
            with self.fulfilled_order_repo.get_session() as session:
                results = (
                    session.query(
                        DeBridgeFulfilledOrder.order_id,
                        DeBridgeFulfilledOrder.transaction_hash,
                        DeBridgeBlockchainTransaction.input_data,
                    )
                    .filter(DeBridgeFulfilledOrder.blockchain != "solana")
                    .join(
                        DeBridgeBlockchainTransaction,
                        DeBridgeBlockchainTransaction.transaction_hash
                        == DeBridgeFulfilledOrder.transaction_hash,
                    )
                    .all()
                )

            updates = []
            for order_id, tx_hash, input_data in results:
                log_to_cli(
                    build_log_message_generator(
                        self.bridge,
                        (
                            f"Post-processing fulfill order: {order_id} -- Tx Hash: {tx_hash} "
                            f" {len(updates) / len(results) * 100:.2f}% done...",
                        ),
                    ),
                    CliColor.INFO,
                )

                if not input_data:
                    continue

                try:
                    function_selector = input_data[:10]

                    if (
                        function_selector == "0x4d8160ba" or function_selector == "0xc7a76969"
                    ):  # strictlySwapAndCall or strictlySwapAndCallDln
                        token_in = unpad_address(input_data[10:74])
                        amount_in = int(input_data[74:138], 16)

                        updates.append((order_id, token_in, amount_in))

                    elif (
                        function_selector == "0xb9303701" or function_selector == "0xc358547e"
                    ):  # createSaltedOrder or fulfillOrder
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
            for order_id, middle_token, middle_amount in updates:
                self.fulfilled_order_repo.update_middle_info_order_fulfilled(
                    order_id,
                    middle_token,
                    middle_amount,
                )

            # Get all created orders + their input data in a single query
            with self.created_order_repo.get_session() as session:
                results = (
                    session.query(
                        DeBridgeCreatedOrder.order_id,
                        DeBridgeCreatedOrder.transaction_hash,
                        DeBridgeBlockchainTransaction.input_data,
                    )
                    .filter(DeBridgeCreatedOrder.blockchain != "solana")
                    .join(
                        DeBridgeBlockchainTransaction,
                        DeBridgeBlockchainTransaction.transaction_hash
                        == DeBridgeCreatedOrder.transaction_hash,
                    )
                    .all()
                )

            updates = []
            for order_id, tx_hash, input_data in results:
                log_to_cli(
                    build_log_message_generator(
                        self.bridge,
                        (
                            f"Post-processing fulfill order: {order_id} -- Tx Hash: {tx_hash} "
                            f" {len(updates) / len(results) * 100:.2f}% done...",
                        ),
                    ),
                    CliColor.INFO,
                )

                if not input_data:
                    continue

                try:
                    function_selector = input_data[:10]

                    if (
                        function_selector == "0x4d8160ba" or function_selector == "0xc7a76969"
                    ):  # strictlySwapAndCall or strictlySwapAndCallDln
                        token_in = unpad_address(input_data[10:74])
                        amount_in = int(input_data[74:138], 16)

                        updates.append((order_id, token_in, amount_in))

                    elif (
                        function_selector == "0xb9303701" or function_selector == "0xc358547e"
                    ):  # createSaltedOrder or fulfillOrder
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
            for order_id, middle_token, middle_amount in updates:
                self.created_order_repo.update_middle_info_order_fulfilled(
                    order_id,
                    middle_token,
                    middle_amount,
                )

        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{self.bridge} -- Error during post-processing: {e}",
            ) from e
