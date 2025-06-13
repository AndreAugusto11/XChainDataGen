import struct
from typing import Union

from utils.utils import trim0x

PACKET_VERSION_OFFSET = 0
NONCE_OFFSET = 1
SRC_CHAIN_OFFSET = 9
SRC_ADDRESS_OFFSET = 13
DST_CHAIN_OFFSET = 45
DST_ADDRESS_OFFSET = 49
GUID_OFFSET = 81
MESSAGE_OFFSET = 113


class PacketSentDecoder:
    @staticmethod
    def decode(payload: Union[bytes, str]):
        if isinstance(payload, str):
            payload = bytes.fromhex(trim0x(payload))

        version = payload[PACKET_VERSION_OFFSET]
        nonce = struct.unpack_from(">Q", payload, NONCE_OFFSET)[0]
        srcEid = struct.unpack_from(">I", payload, SRC_CHAIN_OFFSET)[0]
        sender = "0x" + payload[SRC_ADDRESS_OFFSET : SRC_ADDRESS_OFFSET + 32].hex()
        dstEid = struct.unpack_from(">I", payload, DST_CHAIN_OFFSET)[0]
        receiver = "0x" + payload[DST_ADDRESS_OFFSET : DST_ADDRESS_OFFSET + 32].hex()
        guid = "0x" + payload[GUID_OFFSET : GUID_OFFSET + 32].hex()
        message = "0x" + payload[MESSAGE_OFFSET:].hex()

        return {
            "guid": guid,
            "nonce": nonce,
            "version": version,
            "src_eid": srcEid,
            "sender": sender,
            "dst_eid": dstEid,
            "receiver": receiver,
            "message": message,
        }
