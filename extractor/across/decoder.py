from web3.contract import Contract

from extractor.base_decoder import BaseDecoder
from utils.utils import CustomException


class AcrossDecoder(BaseDecoder):
    CLASS_NAME = "AcrossDecoder"

    def __init__(self):
        super().__init__()

    def decode_event(self, contract: Contract, log: dict):
        func_name = "decode_event"

        if log["topics"][0] == "0x32ed1a409ef04c7b0227189c3a103dc5ac10e775a15b785dcc510201f7c25ad3":
            return contract.events.FundsDeposited().process_log(log)["args"]
        elif (
            log["topics"][0] == "0x44b559f101f8fbcc8a0ea43fa91a05a729a5ea6e14a7c75aa750374690137208"
        ):
            return contract.events.FilledRelay().process_log(log)["args"]
        elif (
            log["topics"][0] == "0xf4ad92585b1bc117fbdd644990adf0827bc4c95baeae8a23322af807b6d0020e"
        ):
            return contract.events.ExecutedRelayerRefundRoot().process_log(log)["args"]

        raise CustomException(
            self.CLASS_NAME, func_name, f"Unknown event topic: {log['topics'][0]}"
        )
