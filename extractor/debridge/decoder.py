from web3.contract import Contract

from extractor.base_decoder import BaseDecoder
from utils.utils import CustomException


class DebridgeDecoder(BaseDecoder):
    CLASS_NAME = "DebridgeDecoder"

    def __init__(self):
        super().__init__()

    def decode_event(self, contract: Contract, log: dict):
        func_name = "decode_event"

        if (
            log["topics"][0] == "0xfc8703fd57380f9dd234a89dce51333782d49c5902f307b02f03e014d18fe471"
        ):  # CreatedOrder
            return contract.events.CreatedOrder().process_log(log)["args"]
        elif (
            log["topics"][0] == "0x33fff3d864e92b6e1ef9e830196fc019c946104ea621b833aaebd3c3e84b2f6f"
        ):  # ClaimedUnlock
            return contract.events.ClaimedUnlock().process_log(log)["args"]
        elif (
            log["topics"][0] == "0x37a01d7dc38e924008cf4f2fa3d2ec1f45e7ae3c8292eb3e7d9314b7ad10e2fc"
        ):  # SentOrderUnlock
            return contract.events.SentOrderUnlock().process_log(log)["args"]
        elif (
            log["topics"][0] == "0xd281ee92bab1446041582480d2c0a9dc91f855386bb27ea295faac1e992f7fe4"
        ):  # FulfilledOrder
            return contract.events.FulfilledOrder().process_log(log)["args"]

        raise CustomException(
            self.CLASS_NAME, func_name, f"Unknown event topic: {log['topics'][0]}"
        )
