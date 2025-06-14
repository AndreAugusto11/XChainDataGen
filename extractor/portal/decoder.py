from web3.contract import Contract

from extractor.base_decoder import BaseDecoder
from utils.utils import CustomException


class PortalDecoder(BaseDecoder):
    CLASS_NAME = "PortalDecoder"

    def __init__(self):
        super().__init__()

    def decode_event(self, contract: Contract, log: dict):
        func_name = "decode_event"

        if log["topics"][0] == "0x6eb224fb001ed210e379b335e35efe88672a8ce935d981a6896b27ffdf52a3b2":
            return contract.events.LogMessagePublished().process_log(log)["args"]
        elif (
            log["topics"][0] == "0xcaf280c8cfeba144da67230d9b009c8f868a75bac9a528fa0474be1ba317c169"
        ):
            return contract.events.TransferRedeemed().process_log(log)["args"]

        raise CustomException(
            self.CLASS_NAME, func_name, f"Unknown event topic: {log['topics'][0]}"
        )
