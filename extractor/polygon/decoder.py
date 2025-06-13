from web3.contract import Contract

from extractor.base_decoder import BaseDecoder
from utils.utils import CustomException


class PolygonDecoder(BaseDecoder):
    CLASS_NAME = "PolygonDecoder"

    def __init__(self):
        super().__init__()

    def decode_event(self, contract: Contract, log: dict):
        func_name = "decode_event"

        if log["topics"][0] == "0x103fed9db65eac19c4d870f49ab7520fe03b99f1838e5996caf47e9e43308392":
            return contract.events.StateSynced().process_log(log)["args"]

        raise CustomException(
            self.CLASS_NAME, func_name, f"Unknown event topic: {log['topics'][0]}"
        )
