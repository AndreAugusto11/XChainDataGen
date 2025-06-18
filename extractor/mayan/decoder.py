from web3.contract import Contract

from extractor.base_decoder import BaseDecoder
from utils.utils import CustomException


class MayanDecoder(BaseDecoder):
    CLASS_NAME = "MayanDecoder"

    def __init__(self):
        super().__init__()

    def decode_event(self, contract: Contract, log: dict):
        func_name = "decode_event"

        if log["topics"][0] == "0x7cbff921ae1f3ea71284120d2aabde13587df067f2bb5c831ea6e35d7a9242ac":
            return contract.events.SwapAndForwardedEth().process_log(log)["args"]
        elif (
            log["topics"][0] == "0x23278f58875126c795a4072b98b5851fe9b21cea19895b02a6224fefbb1e3298"
        ):
            return contract.events.SwapAndForwardedERC20().process_log(log)["args"]
        elif (
            log["topics"][0] == "0xb8543d214cab9591941648db8d40126a163bfd0db4a865678320b921e1398043"
        ):
            return contract.events.ForwardedEth().process_log(log)["args"]
        elif (
            log["topics"][0] == "0xbf150db6b4a14b084f7346b4bc300f552ce867afe55be27bce2d6b37e3307cda"
        ):
            return contract.events.ForwardedERC20().process_log(log)["args"]
        elif (
            log["topics"][0] == "0x918554b6bd6e2895ce6553de5de0e1a69db5289aa0e4fe193a0dcd1f14347477"
        ):
            return contract.events.OrderCreated().process_log(log)["args"]
        elif (
            log["topics"][0] == "0x6ec9b1b5a9f54d929394f18dac4ba1b1cc79823f2266c2d09cab8a3b4700b40b"
        ):
            return contract.events.OrderFulfilled().process_log(log)["args"]
        elif (
            log["topics"][0] == "0x4bdcff348c4d11383c487afb95f732f243d93fbfc478aa736a4981cf6a640911"
        ):
            return contract.events.OrderUnlocked().process_log(log)["args"]

        raise CustomException(
            self.CLASS_NAME, func_name, f"Unknown event topic: {log['topics'][0]}"
        )
