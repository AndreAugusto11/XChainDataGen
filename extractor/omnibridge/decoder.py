from web3.contract import Contract

from extractor.base_decoder import BaseDecoder
from utils.utils import CustomException


class OmnibridgeDecoder(BaseDecoder):
    CLASS_NAME = "OmnibridgeDecoder"

    def __init__(self):
        super().__init__()

    def decode_event(self, contract: Contract, log: dict):
        func_name = "decode_event"

        if log["topics"][0] == "0x482515ce3d9494a37ce83f18b72b363449458435fafdd7a53ddea7460fe01b58":
            return contract.events.UserRequestForAffirmation().process_log(log)["args"]
        elif (
            log["topics"][0] == "0x520d2afde79cbd5db58755ac9480f81bc658e5c517fcae7365a3d832590b0183"
        ):
            return contract.events.UserRequestForSignature().process_log(log)["args"]

        raise CustomException(
            self.CLASS_NAME, func_name, f"Unknown event topic: {log['topics'][0]}"
        )
