import struct
from typing import Union

from utils.utils import trim0x

NONCE_OFFSET = 0
SRC_CHAIN_OFFSET = 8
UA_OFFSET = 10
DST_CHAIN_OFFSET = 30
DST_ADDRESS_OFFSET = 32
PAYLOAD_OFFSET = 52


class PacketDecoder:
    @staticmethod
    def decode(payload: Union[bytes, str]):
        if isinstance(payload, str):
            payload = bytes.fromhex(trim0x(payload))

        nonce = struct.unpack_from(">Q", payload, NONCE_OFFSET)[0]
        srcChainId = struct.unpack_from(">H", payload, SRC_CHAIN_OFFSET)[0]
        srcAddress = "0x" + payload[UA_OFFSET : UA_OFFSET + 20].hex()
        dstChainId = struct.unpack_from(">H", payload, DST_CHAIN_OFFSET)[0]
        dstAddress = "0x" + payload[DST_ADDRESS_OFFSET : DST_ADDRESS_OFFSET + 20].hex()
        payload = "0x" + payload[PAYLOAD_OFFSET:].hex()

        return {
            "nonce": nonce,
            "srcChainId": srcChainId,
            "srcAddress": srcAddress,
            "dstChainId": dstChainId,
            "dstAddress": dstAddress,
            "payload": payload,
        }
