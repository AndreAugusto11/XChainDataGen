from web3.contract import Contract

from extractor.base_decoder import BaseDecoder
from utils.utils import CustomException


class CctpDecoder(BaseDecoder):
    CLASS_NAME = "CctpDecoder"

    def __init__(self):
        super().__init__()

    def decode_event(self, contract: Contract, log: dict):
        func_name = "decode_event"

        if log["topics"][0] == "0x58200b4c34ae05ee816d710053fff3fb75af4395915d3d2a771b24aa10e3cc5d":
            return contract.events.MessageReceived().process_log(log)["args"]

        raise CustomException(
            self.CLASS_NAME, func_name, f"Unknown event topic: {log['topics'][0]}"
        )
