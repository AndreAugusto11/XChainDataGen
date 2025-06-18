from extractor.mayan.utils.MayanOrderParamsDecoder import MayanOrderParamsDecoder


def test_order_params_decoder():
    # Initialize the decoder
    decoder = MayanOrderParamsDecoder()

    # Example payload for ethereum tx hash:
    # 0x52cb475fae780aa3bb7364b494b209caedd2cc1493bebc91295ed20960b55bd6
    payload = (
        "0000000000000000000000001ca9a7ae16e65197a8c20a33495224fbfd873149"
        "0000000000000000000000000000000000000000000000000000000000000000"
        "000000000000000000000000000000000000000000000000000000000234c11a"
        "0000000000000000000000000000000000000000000000000000000000000000"
        "0000000000000000000000000000000000000000000000000000000000006525"
        "000000000000000000000000000000000000000000000000000000000000f0ab"
        "0000000000000000000000000000000000000000000000000000000067c9d752"
        "316501f1057141493288a69bd07d94b7c7b8407f2517d39a949b0109769f7624"
        "0000000000000000000000000000000000000000000000000000000000000001"
        "5d573be539baecd902affec2a76021ae3258ed57894419b006bc6fe4c9ee1c86"
        "0000000000000000000000000000000000000000000000000000000000000000"
        "0000000000000000000000000000000000000000000000000000000000000002"
        "c29659703a460be916906d6cca00651dec4b5e6d9a303494e03991e23adb5c70"
    )

    # Decode the payload
    decoded_data = decoder.decode(payload)

    print(decoded_data)

    assert decoded_data is not None

    assert decoded_data["trader"] == "0x1ca9a7ae16e65197a8c20a33495224fbfd873149"
    assert decoded_data["tokenOut"] == "0x0000000000000000000000000000000000000000"
    assert decoded_data["minAmountOut"] == 37011738
    assert decoded_data["gasDrop"] == 0
    assert decoded_data["cancelFee"] == 25893
    assert decoded_data["refundFee"] == 61611
    assert decoded_data["deadline"] == 1741281106
    assert decoded_data["destAddr"] == "0xd07d94b7c7b8407f2517d39a949b0109769f7624"
    assert decoded_data["destChainId"] == 1
    assert decoded_data["referrerAddr"] == "0xa76021ae3258ed57894419b006bc6fe4c9ee1c86"
    assert decoded_data["referrerBps"] == 0
    assert decoded_data["auctionMode"] == 2
    assert decoded_data["random"] == "0xca00651dec4b5e6d9a303494e03991e23adb5c70"
