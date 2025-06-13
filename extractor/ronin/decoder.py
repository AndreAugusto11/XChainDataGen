from web3.contract import Contract

from extractor.base_decoder import BaseDecoder
from utils.utils import CustomException


class RoninDecoder(BaseDecoder):
    CLASS_NAME = "RoninDecoder"

    def __init__(self):
        super().__init__()

    def decode_event(self, contract: Contract, log: dict):
        func_name = "decode_event"

        if log["topics"][0] == "0xd7b25068d9dc8d00765254cfb7f5070f98d263c8d68931d937c7362fa738048b":
            return contract.events.DepositRequested().process_log(log)["args"]
        elif (
            log["topics"][0] == "0x8d20d8121a34dded9035ff5b43e901c142824f7a22126392992c353c37890524"
        ):
            return contract.events.Deposited().process_log(log)["args"]
        elif (
            log["topics"][0] == "0xf313c253a5be72c29d0deb2c8768a9543744ac03d6b3cafd50cc976f1c2632fc"
        ):
            return contract.events.WithdrawalRequested().process_log(log)["args"]
        elif (
            log["topics"][0] == "0x21e88e956aa3e086f6388e899965cef814688f99ad8bb29b08d396571016372d"
        ):
            return contract.events.Withdrew().process_log(log)["args"]

        raise CustomException(
            self.CLASS_NAME, func_name, f"Unknown event topic: {log['topics'][0]}"
        )
