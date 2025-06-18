from utils.utils import unpad_address

TRADER_OFFSET = 0
TOKEN_OUT_OFFSET = 64
MIN_AMOUNT_OUT_OFFSET = 128
GAS_DROP_OFFSET = 192
CANCEL_FEE_OFFSET = 256
REFUND_FEE_OFFSET = 320
DEADLINE_OFFSET = 384
DEST_ADDR_OFFSET = 448
DEST_CHAIN_ID_OFFSET = 512
REFERRER_ADDR_OFFSET = 576
REFERRER_BPS_OFFSET = 640
AUCTION_MODE_OFFSET = 704
RANDOM_OFFSET = 768


# Decode OrderParams from Mayan Swift contract 0xc38e4e6a15593f908255214653d3d947ca1c2338#code
class MayanOrderParamsDecoder:
    @staticmethod
    def decode(data: str) -> dict:
        trader = data[TRADER_OFFSET : TRADER_OFFSET + 64]
        token_out = data[TOKEN_OUT_OFFSET : TOKEN_OUT_OFFSET + 64]
        min_amount_out = data[MIN_AMOUNT_OUT_OFFSET : MIN_AMOUNT_OUT_OFFSET + 64]
        gas_drop = data[GAS_DROP_OFFSET : GAS_DROP_OFFSET + 64]
        cancel_fee = data[CANCEL_FEE_OFFSET : CANCEL_FEE_OFFSET + 64]
        refund_fee = data[REFUND_FEE_OFFSET : REFUND_FEE_OFFSET + 64]
        deadline = data[DEADLINE_OFFSET : DEADLINE_OFFSET + 64]
        dest_addr = data[DEST_ADDR_OFFSET : DEST_ADDR_OFFSET + 64]
        dest_chain_id = data[DEST_CHAIN_ID_OFFSET : DEST_CHAIN_ID_OFFSET + 64]
        referrer_addr = data[REFERRER_ADDR_OFFSET : REFERRER_ADDR_OFFSET + 64]
        referrer_bps = data[REFERRER_BPS_OFFSET : REFERRER_BPS_OFFSET + 64]
        auction_mode = data[AUCTION_MODE_OFFSET : AUCTION_MODE_OFFSET + 64]
        random = data[RANDOM_OFFSET : RANDOM_OFFSET + 64]

        return {
            "trader": unpad_address(trader),
            "tokenOut": unpad_address(token_out),
            "minAmountOut": int(min_amount_out, 16),
            "gasDrop": int(gas_drop, 16),
            "cancelFee": int(cancel_fee, 16),
            "refundFee": int(refund_fee, 16),
            "deadline": int(deadline, 16),
            "destAddr": unpad_address(dest_addr),
            "destChainId": int(dest_chain_id, 16),
            "referrerAddr": unpad_address(referrer_addr),
            "referrerBps": int(referrer_bps, 16),
            "auctionMode": int(auction_mode, 16),
            "random": unpad_address(random),
        }
