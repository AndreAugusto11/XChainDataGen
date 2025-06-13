from web3.contract import Contract

from extractor.base_decoder import BaseDecoder
from utils.utils import CustomException


class CcipDecoder(BaseDecoder):
    CLASS_NAME = "CcipDecoder"

    def __init__(self):
        super().__init__()

    def decode_event(self, contract: Contract, log: dict):
        func_name = "decode_event"

        if log["topics"][0] == "0xd0c3c799bf9e2639de44391e7f524d229b2b55f5b1ea94b2bf7da42f7243dddd":
            return contract.events.CCIPSendRequested().process_log(log)["args"]
        elif (
            log["topics"][0] == "0xd4f851956a5d67c3997d1c9205045fef79bae2947fdee7e9e2641abc7391ef65"
        ):
            return contract.events.ExecutionStateChanged().process_log(log)["args"]

        raise CustomException(
            self.CLASS_NAME, func_name, f"Unknown event topic: {log['topics'][0]}"
        )
