from web3.contract import Contract

from extractor.base_decoder import BaseDecoder
from utils.utils import CustomException


class AcrossDecoder(BaseDecoder):
    CLASS_NAME = "AcrossDecoder"

    def __init__(self):
        super().__init__()

    def decode_event(self, contract: Contract, log: dict):
        func_name = "decode_event"

        if log["topics"][0] == "0xa123dc29aebf7d0c3322c8eeb5b999e859f39937950ed31056532713d0de396f":
            return contract.events.V3FundsDeposited().process_log(log)["args"]
        elif (
            log["topics"][0] == "0x571749edf1d5c9599318cdbc4e28a6475d65e87fd3b2ddbe1e9a8d5e7a0f0ff7"
        ):
            return contract.events.FilledV3Relay().process_log(log)["args"]
        elif (
            log["topics"][0] == "0xf8bd640004bcec1b89657020f561d0b070cbdf662d0b158db9dccb0a8301bfab"
        ):
            return contract.events.ExecutedRelayerRefundRoot().process_log(log)["args"]

        raise CustomException(
            self.CLASS_NAME, func_name, f"Unknown event topic: {log['topics'][0]}"
        )
