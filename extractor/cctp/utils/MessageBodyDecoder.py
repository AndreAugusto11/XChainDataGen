from typing import Union

from utils.utils import trim0x, unpad_address

VERSION_OFFSET = 4
RECIPIENT_OFFSET = 36
AMOUNT_OFFSET = 68
DEPOSITOR_OFFSET = 100
END_OFFSET = 132


class MessageBodyDecoder:
    @staticmethod
    def decode(payload: Union[bytes, str]):
        # Convert hex string to bytes if needed
        if isinstance(payload, str):
            payload = bytes.fromhex(trim0x(payload))

        input_token = payload[VERSION_OFFSET:RECIPIENT_OFFSET].hex()
        recipient = payload[RECIPIENT_OFFSET:AMOUNT_OFFSET].hex()
        amount = payload[AMOUNT_OFFSET:DEPOSITOR_OFFSET].hex()
        depositor = payload[DEPOSITOR_OFFSET:END_OFFSET].hex()

        return {
            "input_token": unpad_address(input_token),
            "recipient": unpad_address(recipient),
            "amount": unpad_address(amount),
            "depositor": unpad_address(depositor),
        }
