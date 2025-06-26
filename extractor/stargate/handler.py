import time
from typing import Any, Dict, List

from config.constants import Bridge
from extractor.base_handler import BaseHandler
from extractor.stargate.constants import BLOCKCHAIN_IDS, BRIDGE_CONFIG
from extractor.stargate.utils.PacketDecoder import PacketDecoder
from extractor.stargate.utils.PacketSentDecoder import PacketSentDecoder
from repository.database import DBSession
from repository.stargate.repository import (
    StargateBlockchainTransactionRepository,
    StargateBusDrivenRepository,
    StargateBusRodeRepository,
    StargateComposeDeliveredRepository,
    StargateComposeSentRepository,
    StargateDVNFeePaidRepository,
    StargateExecutorFeePaidRepository,
    StargateOFTReceivedRepository,
    StargateOFTReceiveFromChainRepository,
    StargateOFTSendToChainRepository,
    StargateOFTSentRepository,
    StargatePacketDeliveredRepository,
    StargatePacketReceivedRepository,
    StargatePacketRepository,
    StargatePacketSentRepository,
    StargatePacketVerifiedRepository,
    StargatePayloadVerifiedRepository,
    StargateRelayerFeeRepository,
    StargateSwapRemoteRepository,
    StargateSwapRepository,
    StargateUlnConfigSetRepository,
    StargateVerifierFeeRepository,
)
from rpcs.evm_rpc_client import EvmRPCClient
from utils.utils import CustomException, log_error, unpad_address


class StargateHandler(BaseHandler):
    CLASS_NAME = "StargateHandler"

    def __init__(self, rpc_client: EvmRPCClient, blockchains: list) -> None:
        super().__init__(rpc_client, blockchains)
        self.bridge = Bridge.STARGATE

    def get_bridge_contracts_and_topics(self, bridge: str, blockchain: List[str]) -> None:
        return super().get_bridge_contracts_and_topics(
            config=BRIDGE_CONFIG,
            bridge=bridge,
            blockchain=blockchain,
        )

    def bind_db_to_repos(self):
        self.blockchain_transaction_repo = StargateBlockchainTransactionRepository(DBSession)
        self.executor_fee_paid_repo = StargateExecutorFeePaidRepository(DBSession)
        self.uln_config_set_repo = StargateUlnConfigSetRepository(DBSession)
        self.packet_delivered_repo = StargatePacketDeliveredRepository(DBSession)
        self.packet_verified_repo = StargatePacketVerifiedRepository(DBSession)
        self.packet_sent_repo = StargatePacketSentRepository(DBSession)
        self.packet_received_repo = StargatePacketReceivedRepository(DBSession)
        self.packet_repo = StargatePacketRepository(DBSession)
        self.payload_verified_repo = StargatePayloadVerifiedRepository(DBSession)
        self.dvn_fee_paid_repo = StargateDVNFeePaidRepository(DBSession)
        self.oft_received_repo = StargateOFTReceivedRepository(DBSession)
        self.oft_sent_repo = StargateOFTSentRepository(DBSession)
        self.oft_send_to_chain_repo = StargateOFTSendToChainRepository(DBSession)
        self.oft_receive_from_chain_repo = StargateOFTReceiveFromChainRepository(DBSession)
        self.bus_rode_repo = StargateBusRodeRepository(DBSession)
        self.bus_driven_repo = StargateBusDrivenRepository(DBSession)
        self.swap_repo = StargateSwapRepository(DBSession)
        self.swap_remote_repo = StargateSwapRemoteRepository(DBSession)
        self.verifier_fee_repo = StargateVerifierFeeRepository(DBSession)
        self.relayer_fee_repo = StargateRelayerFeeRepository(DBSession)
        self.compose_sent_repo = StargateComposeSentRepository(DBSession)
        self.compose_delivered_repo = StargateComposeDeliveredRepository(DBSession)

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
                start_ts = time.time()
                if (
                    event["topic"]
                    == "0x1ab700d4ced0c005b164c0f789fd09fcbb0156d4c2041b8a3bfbcd961cd1567f"
                ):  # PacketSent
                    event = self.handle_packet_sent(blockchain, event)
                elif (
                    event["topic"]
                    == "0xe9bded5f24a4168e4f3bf44e00298c993b22376aad8c58c7dda9718a54cbea82"
                ):  # Packet
                    event = self.handle_packet(blockchain, event)
                elif (
                    event["topic"]
                    == "0x3cd5e48f9730b129dc7550f0fcea9c767b7be37837cd10e55eb35f734f4bca04"
                ):  # PacketDelivered
                    event = self.handle_packet_delivered(blockchain, event)
                elif (
                    event["topic"]
                    == "0x0d87345f3d1c929caba93e1c3821b54ff3512e12b66aa3cfe54b6bcbc17e59b4"
                ):  # PacketVerified
                    event = self.handle_packet_verified(blockchain, event)
                elif (
                    event["topic"]
                    == "0x2bd2d8a84b748439fd50d79a49502b4eb5faa25b864da6a9ab5c150704be9a4d"
                ):  # PacketReceived
                    event = self.handle_packet_received(blockchain, event)
                elif (
                    event["topic"]
                    == "0x61ed099e74a97a1d7f8bb0952a88ca8b7b8ebd00c126ea04671f92a81213318a"
                ):  # ExecutorFeePaid
                    event = self.handle_executor_fee_paid(blockchain, event)
                elif (
                    event["topic"]
                    == "0x82118522aa536ac0e96cc5c689407ae42b89d592aa133890a01f1509842f5081"
                ):  # UlnConfigSet
                    event = self.handle_uln_config_set(blockchain, event)
                elif (
                    event["topic"]
                    == "0x2cb0eed7538baeae4c6fde038c0fd0384d27de0dd55a228c65847bda6aa1ab56"
                ):  # PayloadVerified
                    event = self.handle_payload_verified(blockchain, event)
                elif (
                    event["topic"]
                    == "0x07ea52d82345d6e838192107d8fd7123d9c2ec8e916cd0aad13fd2b60db24644"
                ):  # DVNFeePaid
                    event = self.handle_dvn_fee_paid(blockchain, event)
                elif (
                    event["topic"]
                    == "0x85496b760a4b7f8d66384b9df21b381f5d1b1e79f229a47aaf4c232edc2fe59a"
                ):  # OFTSent
                    event = self.handle_oft_sent(blockchain, event)
                elif (
                    event["topic"]
                    == "0xefed6d3500546b29533b128a29e3a94d70788727f0507505ac12eaf2e578fd9c"
                ):  # OFTReceived
                    event = self.handle_oft_received(blockchain, event)
                elif (
                    event["topic"]
                    == "0xd81fc9b8523134ed613870ed029d6170cbb73aa6a6bc311b9a642689fb9df59a"
                ):  # SendToChain BaseOFTV2
                    event = self.handle_oft_send_to_chain(blockchain, event)
                elif (
                    event["topic"]
                    == "0xbf551ec93859b170f9b2141bd9298bf3f64322c6f7beb2543a0cb669834118bf"
                ):  # ReceiveFromChain BaseOFTV2
                    event = self.handle_oft_receive_from_chain(blockchain, event)
                elif (
                    event["topic"]
                    == "0x664e26797cde1146ddfcb9a5d3f4de61179f9c11b2698599bb09e686f442172b"
                ):  # SendToChain Stargate Token
                    event = self.handle_oft_send_to_chain_2(blockchain, event)
                elif (
                    event["topic"]
                    == "0x1e43690f7c7ebcc548b8e72d1ec2273acd54666f0330bef2eeb2268ee9f28988"
                ):  # ReceiveFromChain Stargate Token
                    event = self.handle_oft_receive_from_chain_2(blockchain, event)
                elif (
                    event["topic"]
                    == "0x831bc68226f8d1f734ffcca73602efc4eca13711402ba1d2cc05ee17bb54f631"
                ):  # ReceiveFromChain Stargate Token (Polygon)
                    event = self.handle_oft_receive_from_chain_3(blockchain, event)
                elif (
                    event["topic"]
                    == "0x15955c5a4cc61b8fbb05301bce47fd31c0e6f935e1ab97fdac9b134c887bb074"
                ):  # BusRode
                    event = self.handle_bus_rode(blockchain, event)
                elif (
                    event["topic"]
                    == "0x1623f9ea59bd6f214c9571a892da012fc23534aa5906bef4ae8c5d15ee7d2d6e"
                ):  # BusDriven
                    event = self.handle_bus_driven(blockchain, event)
                elif (
                    event["topic"]
                    == "0x34660fc8af304464529f48a778e03d03e4d34bcd5f9b6f0cfbf3cd238c642f7f"
                ):  # Swap
                    event = self.handle_swap(blockchain, event)
                elif (
                    event["topic"]
                    == "0xfb2b592367452f1c437675bed47f5e1e6c25188c17d7ba01a12eb030bc41ccef"
                ):  # SwapRemote
                    event = self.handle_swap_remote(blockchain, event)
                elif (
                    event["topic"]
                    == "0x87e46b0a6199bc734632187269a103c05714ee0adae5b28f30723955724f37ef"
                ):  # VerifierFee
                    event = self.handle_verifier_fee(blockchain, event)
                elif (
                    event["topic"]
                    == "0xdf21c415b78ed2552cc9971249e32a053abce6087a0ae0fbf3f78db5174a3493"
                ):  # AssignJob
                    event = self.handle_assign_job(blockchain, event)
                elif (
                    event["topic"]
                    == "0x3d52ff888d033fd3dd1d8057da59e850c91d91a72c41dfa445b247dfedeb6dc1"
                ):  # ComposeSent
                    event = self.handle_compose_sent(blockchain, event)
                elif (
                    event["topic"]
                    == "0x0036c98efcf9e6641dfbc9051f66f405253e8e0c2ab4a24dccda15595b7378c8"
                ):  # ComposeDelivered
                    event = self.handle_compose_delivered(blockchain, event)
                endd_ts = time.time()
                if endd_ts - start_ts > 1:
                    print(f"Time taken to process event: {endd_ts - start_ts}")
                if event:
                    included_events.append(event)

            except CustomException as e:
                request_desc = (
                    f"Error processing request: {blockchain}, {start_block}, "
                    f"{end_block}, {contract}, {topics}.\n{e}"
                )
                log_error(self.bridge, request_desc)
        return included_events

    def handle_packet_sent(self, blockchain, event):
        func_name = "handle_packet_sent"
        """
        Handles an event by decoding its payload and storing the decoded data in the database.

        Args:
            event: each event contains:
                - encodedPayload: The payload that needs to be decoded.
                - options: Additional options for the event.
                - sendLibrary: The library used to send the event.
        """

        decoded_event = PacketSentDecoder.decode(event["encodedPayload"])

        try:
            src_blockchain = self.convert_eid_to_blockchain_name(decoded_event["src_eid"])
            dst_blockchain = self.convert_eid_to_blockchain_name(decoded_event["dst_eid"])

            if src_blockchain is None or dst_blockchain is None:
                return None

            if self.packet_sent_repo.event_exists(decoded_event["guid"]):
                return None

            self.packet_sent_repo.create(
                {
                    "guid": decoded_event["guid"],
                    "blockchain": blockchain,
                    "transaction_hash": event["transaction_hash"],
                    "nonce": decoded_event["nonce"],
                    "version": decoded_event["version"],
                    "src_blockchain": src_blockchain,
                    "sender": unpad_address(decoded_event["sender"]),
                    "dst_blockchain": dst_blockchain,
                    "receiver": unpad_address(decoded_event["receiver"]),
                    "message": decoded_event["message"],
                }
            )
            return event
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e

    def handle_packet(self, blockchain, event):
        func_name = "handle_packet"

        decoded_event = PacketDecoder.decode(event["payload"])
        try:
            src_blockchain = self.convert_chain_id_to_blockchain_name(decoded_event["srcChainId"])
            dst_blockchain = self.convert_chain_id_to_blockchain_name(decoded_event["dstChainId"])

            if src_blockchain is None or dst_blockchain is None:
                return None

            if self.packet_repo.event_exists(
                event["transaction_hash"], dst_blockchain, decoded_event["nonce"]
            ):
                return None

            self.packet_repo.create(
                {
                    "blockchain": blockchain,
                    "transaction_hash": event["transaction_hash"],
                    "nonce": decoded_event["nonce"],
                    "src_blockchain": src_blockchain,
                    "src_address": decoded_event["srcAddress"],
                    "dst_blockchain": dst_blockchain,
                    "dst_address": decoded_event["dstAddress"],
                    "payload": decoded_event["payload"],
                }
            )
            return event
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e

    def handle_packet_delivered(self, blockchain, event):
        func_name = "handle_packet_delivered"

        flattened_object = BaseHandler.flatten_object(event)

        try:
            src_blockchain = self.convert_eid_to_blockchain_name(flattened_object["srcEid"])

            if src_blockchain is None:
                return None

            if self.packet_delivered_repo.event_exists(
                event["transaction_hash"],
            ):
                return None

            self.packet_delivered_repo.create(
                {
                    "blockchain": blockchain,
                    "transaction_hash": event["transaction_hash"],
                    "src_blockchain": src_blockchain,
                    "sender": unpad_address(flattened_object["sender"]),
                    "nonce": flattened_object["nonce"],
                    "receiver": event["receiver"],
                }
            )
            return event
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e

    def handle_packet_verified(self, blockchain, event):
        func_name = "handle_packet_verified"

        flattened_object = BaseHandler.flatten_object(event)

        try:
            src_blockchain = self.convert_eid_to_blockchain_name(flattened_object["srcEid"])

            if src_blockchain is None:
                return None

            if self.packet_verified_repo.event_exists(
                event["transaction_hash"],
            ):
                return None

            self.packet_verified_repo.create(
                {
                    "blockchain": blockchain,
                    "transaction_hash": event["transaction_hash"],
                    "src_blockchain": src_blockchain,
                    "sender": unpad_address(flattened_object["sender"]),
                    "nonce": flattened_object["nonce"],
                    "receiver": event["receiver"],
                    "payload_hash": event["payloadHash"],
                }
            )
            return event
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e

    def handle_packet_received(self, blockchain, event):
        func_name = "handle_packet_received"

        try:
            src_blockchain = self.convert_chain_id_to_blockchain_name(event["srcChainId"])

            if src_blockchain is None:
                return None

            if self.packet_received_repo.event_exists(
                event["transaction_hash"],
            ):
                return None

            self.packet_received_repo.create(
                {
                    "blockchain": blockchain,
                    "transaction_hash": event["transaction_hash"],
                    "src_blockchain": src_blockchain,
                    "src_address": event["srcAddress"],
                    "dst_address": event["dstAddress"],
                    "nonce": event["nonce"],
                    "payload_hash": event["payloadHash"],
                }
            )
            return event
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e

    def handle_executor_fee_paid(self, blockchain, event):
        func_name = "handle_executor_fee_paid"
        try:
            self.executor_fee_paid_repo.create(
                {
                    "blockchain": blockchain,
                    "transaction_hash": event["transaction_hash"],
                    "executor": event["executor"],
                    "fee": str(event["fee"]),
                }
            )
            return event
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e

    def handle_uln_config_set(self, blockchain, event):
        func_name = "handle_uln_config_set"

        flattened_object = BaseHandler.flatten_object(event)

        try:
            dst_blockchain = self.convert_eid_to_blockchain_name(event["eid"])

            if dst_blockchain is None:
                return None

            if self.uln_config_set_repo.event_exists(
                event["transaction_hash"],
                dst_blockchain,
                event["oapp"],
            ):
                return None

            self.uln_config_set_repo.create(
                {
                    "blockchain": blockchain,
                    "transaction_hash": event["transaction_hash"],
                    "oapp": event["oapp"],
                    "dst_blockchain": dst_blockchain,
                    "confirmations": flattened_object["confirmations"],
                    "required_dvn_count": flattened_object["requiredDVNCount"],
                    "optional_dvn_count": flattened_object["optionalDVNCount"],
                    "optional_dvn_threshold": flattened_object["optionalDVNThreshold"],
                    "required_dvns": str(flattened_object["requiredDVNs"]),
                    "optional_dvns": str(flattened_object["optionalDVNs"]),
                }
            )
            return event
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e

    def handle_payload_verified(self, blockchain, event):
        func_name = "handle_payload_verified"

        try:
            if self.payload_verified_repo.event_exists(
                event["transaction_hash"],
            ):
                return None

            self.payload_verified_repo.create(
                {
                    "blockchain": blockchain,
                    "transaction_hash": event["transaction_hash"],
                    "dvn": event["dvn"],
                    "header": event["header"],
                    "confirmations": str(event["confirmations"]),
                    "proof_hash": event["proofHash"],
                }
            )
            return event
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e

    def handle_dvn_fee_paid(self, blockchain, event):
        func_name = "handle_dvn_fee_paid"
        fees = event["fees"]

        try:
            total_fees = sum(fees)

            self.dvn_fee_paid_repo.create(
                {
                    "blockchain": blockchain,
                    "transaction_hash": event["transaction_hash"],
                    "fee": total_fees,
                }
            )
            return event
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e

    def handle_oft_sent(self, blockchain, event):
        func_name = "handle_oft_sent"
        try:
            dst_blockchain = self.convert_eid_to_blockchain_name(event["dstEid"])

            if dst_blockchain is None:
                return None

            if self.oft_sent_repo.event_exists(
                event["transaction_hash"],
                event["guid"],
                event["amountReceivedLD"],
            ):
                return None

            self.oft_sent_repo.create(
                {
                    "blockchain": blockchain,
                    "transaction_hash": event["transaction_hash"],
                    "contract_address": event["contract_address"],
                    "guid": event["guid"],
                    "dst_blockchain": dst_blockchain,
                    "from_address": event["fromAddress"],
                    "amount_sent_ld": event["amountSentLD"],
                    "amount_received_ld": event["amountReceivedLD"],
                }
            )
            return event
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e

    def handle_oft_received(self, blockchain, event):
        func_name = "handle_oft_received"
        try:
            src_blockchain = self.convert_eid_to_blockchain_name(event["srcEid"])

            if src_blockchain is None:
                return None

            self.oft_received_repo.create(
                {
                    "blockchain": blockchain,
                    "transaction_hash": event["transaction_hash"],
                    "contract_address": event["contract_address"],
                    "guid": event["guid"],
                    "src_blockchain": src_blockchain,
                    "to_address": event["toAddress"].lower(),
                    "amount_received_ld": str(event["amountReceivedLD"]),
                }
            )
            return event
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e

    def handle_oft_send_to_chain(self, blockchain, event):
        func_name = "handle_oft_send_to_chain"

        try:
            dst_blockchain = self.convert_chain_id_to_blockchain_name(event["_dstChainId"])

            if dst_blockchain is None:
                return None

            if self.oft_send_to_chain_repo.event_exists(event["transaction_hash"], dst_blockchain):
                return None

            self.oft_send_to_chain_repo.create(
                {
                    "blockchain": blockchain,
                    "transaction_hash": event["transaction_hash"],
                    "contract_address": event["contract_address"],
                    "dst_blockchain": dst_blockchain,
                    "from_address": event["_from"],
                    "to_address": unpad_address(event["_toAddress"]),
                    "amount": str(event["_amount"]),
                }
            )
            return event
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e

    def handle_oft_send_to_chain_2(self, blockchain, event):
        func_name = "handle_oft_send_to_chain_2"

        try:
            dst_blockchain = self.convert_chain_id_to_blockchain_name(event["dstChainId"])

            if dst_blockchain is None:
                return None

            if self.oft_send_to_chain_repo.event_exists(event["transaction_hash"], dst_blockchain):
                return None

            self.oft_send_to_chain_repo.create(
                {
                    "blockchain": blockchain,
                    "transaction_hash": event["transaction_hash"],
                    "contract_address": event["contract_address"],
                    "dst_blockchain": dst_blockchain,
                    "from_address": None,
                    "to_address": unpad_address(event["to"]),
                    "amount": str(event["qty"]),
                }
            )
            return event
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e

    def handle_oft_receive_from_chain(self, blockchain, event):
        func_name = "handle_oft_receive_from_chain"

        try:
            src_blockchain = self.convert_chain_id_to_blockchain_name(event["_srcChainId"])

            if src_blockchain is None:
                return None

            if self.oft_receive_from_chain_repo.event_exists(
                event["transaction_hash"],
                src_blockchain,
            ):
                return None

            self.oft_receive_from_chain_repo.create(
                {
                    "blockchain": blockchain,
                    "transaction_hash": event["transaction_hash"],
                    "contract_address": event["contract_address"],
                    "src_blockchain": src_blockchain,
                    "to_address": event["_to"],
                    "nonce": None,
                    "amount": str(event["_amount"]),
                }
            )
            return event
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e

    def handle_oft_receive_from_chain_2(self, blockchain, event):
        func_name = "handle_oft_receive_from_chain_2"

        try:
            src_blockchain = self.convert_chain_id_to_blockchain_name(event["_srcChainId"])

            if src_blockchain is None:
                return None

            if self.oft_receive_from_chain_repo.event_exists(
                event["transaction_hash"],
                src_blockchain,
            ):
                return None

            self.oft_receive_from_chain_repo.create(
                {
                    "blockchain": blockchain,
                    "transaction_hash": event["transaction_hash"],
                    "contract_address": event["contract_address"],
                    "src_blockchain": src_blockchain,
                    "to_address": None,
                    "nonce": event["nonce"],
                    "amount": str(event["_amount"]),
                }
            )
            return event
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e

    def handle_oft_receive_from_chain_3(self, blockchain, event):
        func_name = "handle_oft_receive_from_chain_3"

        try:
            src_blockchain = self.convert_chain_id_to_blockchain_name(event["srcChainId"])

            if src_blockchain is None:
                return None

            if self.oft_receive_from_chain_repo.event_exists(
                event["transaction_hash"],
                src_blockchain,
            ):
                return None

            self.oft_receive_from_chain_repo.create(
                {
                    "blockchain": blockchain,
                    "transaction_hash": event["transaction_hash"],
                    "contract_address": event["contract_address"],
                    "src_blockchain": src_blockchain,
                    "to_address": None,
                    "nonce": event["nonce"],
                    "amount": str(event["qty"]),
                }
            )
            return event
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e

    def handle_bus_rode(self, blockchain, event):
        func_name = "handle_bus_rode"
        try:
            dst_blockchain = self.convert_eid_to_blockchain_name(event["dstEid"])

            if dst_blockchain is None:
                return None

            if self.bus_rode_repo.event_exists(
                event["transaction_hash"],
                event["ticketId"],
            ):
                return

            self.bus_rode_repo.create(
                {
                    "blockchain": blockchain,
                    "transaction_hash": event["transaction_hash"],
                    "dst_blockchain": dst_blockchain,
                    "ticket_id": event["ticketId"],
                    "fare": str(event["fare"]),
                    "passenger": self.extract_address_from_passenger(event["passenger"]),
                }
            )
            return event
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e

    def handle_bus_driven(self, blockchain, event):
        func_name = "handle_bus_driven"
        try:
            dst_blockchain = self.convert_eid_to_blockchain_name(event["dstEid"])

            if dst_blockchain is None:
                return None

            if self.bus_driven_repo.event_exists(
                event["guid"],
            ):
                return

            self.bus_driven_repo.create(
                {
                    "blockchain": blockchain,
                    "transaction_hash": event["transaction_hash"],
                    "dst_blockchain": dst_blockchain,
                    "start_ticket_id": event["startTicketId"],
                    "num_passengers": event["numPassengers"],
                    "guid": event["guid"],
                }
            )
            return event
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e

    def handle_swap(self, blockchain, event):
        func_name = "handle_swap"
        try:
            dst_blockchain = self.convert_chain_id_to_blockchain_name(event["chainId"])

            if dst_blockchain is None:
                return None

            self.swap_repo.create(
                {
                    "blockchain": blockchain,
                    "transaction_hash": event["transaction_hash"],
                    "contract_address": event["contract_address"],
                    "dst_blockchain": dst_blockchain,
                    "dst_pool_id": event["dstPoolId"],
                    "from_address": event["from"],
                    "amount_sd": str(event["amountSD"]),
                    "eq_reward": str(event["eqReward"]),
                    "eq_fee": str(event["eqFee"]),
                    "protocol_fee": str(event["protocolFee"]),
                    "lp_fee": str(event["lpFee"]),
                }
            )
            return event
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e

    def handle_swap_remote(self, blockchain, event):
        func_name = "handle_swap_remote"
        try:
            if self.swap_remote_repo.event_exists(
                event["transaction_hash"],
            ):
                return

            self.swap_remote_repo.create(
                {
                    "blockchain": blockchain,
                    "transaction_hash": event["transaction_hash"],
                    "contract_address": event["contract_address"],
                    "to_address": event["to"],
                    "amount_sd": str(event["amountSD"]),
                    "protocol_fee": str(event["protocolFee"]),
                    "dst_fee": str(event["dstFee"]),
                }
            )
            return event
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e

    def handle_compose_sent(self, blockchain, event):
        func_name = "handle_compose_sent"

        try:
            if self.compose_sent_repo.event_exists(
                event["guid"],
            ):
                return

            self.compose_sent_repo.create(
                {
                    "blockchain": blockchain,
                    "transaction_hash": event["transaction_hash"],
                    "from_address": event["from"],
                    "to_address": event["to"],
                    "guid": event["guid"],
                    "index": event["index"],
                    "message": event["message"],
                }
            )
            return event
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e

    def handle_compose_delivered(self, blockchain, event):
        func_name = "handle_compose_delivered"

        try:
            if self.compose_delivered_repo.event_exists(
                event["guid"],
            ):
                return

            self.compose_delivered_repo.create(
                {
                    "blockchain": blockchain,
                    "transaction_hash": event["transaction_hash"],
                    "from_address": event["from"],
                    "to_address": event["to"],
                    "guid": event["guid"],
                    "index": event["index"],
                }
            )
            return event
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e

    def handle_verifier_fee(self, blockchain, event):
        func_name = "handle_verifier_fee"
        try:
            self.verifier_fee_repo.create(
                {
                    "blockchain": blockchain,
                    "transaction_hash": event["transaction_hash"],
                    "fee": str(event["fee"]),
                }
            )
            return event
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e

    def handle_assign_job(self, blockchain, event):
        func_name = "handle_assign_job"

        try:
            self.relayer_fee_repo.create(
                {
                    "blockchain": blockchain,
                    "transaction_hash": event["transaction_hash"],
                    "fee": str(event["totalFee"]),
                }
            )
            return event
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e

    def convert_eid_to_blockchain_name(self, eid: str) -> str:
        func_name = "convert_eid_to_blockchain_name"

        eid = str(eid)

        if eid in BLOCKCHAIN_IDS:
            blockchain_name = BLOCKCHAIN_IDS[eid]["name"]

            if self.counterPartyBlockchainsMap.get(blockchain_name):
                return blockchain_name
        else:
            CustomException(self.CLASS_NAME, func_name, f"Blockchain not found for EID: {eid}")
            # log_to_file(e, "data/out_of_scope_blockchains.log")
            return None

    def convert_chain_id_to_blockchain_name(self, chain_id: str) -> str:
        eid = "30" + str(chain_id)
        return self.convert_eid_to_blockchain_name(eid)

    def extract_address_from_passenger(self, passenger: str):
        return "0x" + passenger[28:68]
