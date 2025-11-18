# Mapping of bridges to their supported blockchains and contracts
BRIDGE_CONFIG = {
    "blockchains": {
        "ethereum": [
            {
                "abi": "across",
                "contracts": [
                    "0x5c7bcd6e7de5423a257d81b442095a1a6ced35c5",  # Across Protocol: SpokePool
                ],
                "topics": [
                    "0x32ed1a409ef04c7b0227189c3a103dc5ac10e775a15b785dcc510201f7c25ad3",  # FundsDeposited
                    "0x44b559f101f8fbcc8a0ea43fa91a05a729a5ea6e14a7c75aa750374690137208",  # FilledRelay
                    "0xf4ad92585b1bc117fbdd644990adf0827bc4c95baeae8a23322af807b6d0020e",  # ExecutedRelayerRefundRoot
                ],
            },
        ],
        "unichain": [
            {
                "abi": "across",
                "contracts": [
                    "0x09aea4b2242abc8bb4bb78d537a67a245a7bec64",  # Across Protocol: SpokePool
                ],
                "topics": [
                    "0x32ed1a409ef04c7b0227189c3a103dc5ac10e775a15b785dcc510201f7c25ad3",  # FundsDeposited
                    "0x44b559f101f8fbcc8a0ea43fa91a05a729a5ea6e14a7c75aa750374690137208",  # FilledRelay
                    "0xf4ad92585b1bc117fbdd644990adf0827bc4c95baeae8a23322af807b6d0020e",  # ExecutedRelayerRefundRoot
                ],
            },
        ],
        "arbitrum": [
            {
                "abi": "across",
                "contracts": [
                    "0xe35e9842fceaca96570b734083f4a58e8f7c5f2a",  # Across Protocol: SpokePool
                ],
                "topics": [
                    "0x32ed1a409ef04c7b0227189c3a103dc5ac10e775a15b785dcc510201f7c25ad3",  # FundsDeposited
                    "0x44b559f101f8fbcc8a0ea43fa91a05a729a5ea6e14a7c75aa750374690137208",  # FilledRelay
                    "0xf4ad92585b1bc117fbdd644990adf0827bc4c95baeae8a23322af807b6d0020e",  # ExecutedRelayerRefundRoot
                ],
            },
        ],
        "polygon": [
            {
                "abi": "across",
                "contracts": [
                    "0x9295ee1d8c5b022be115a2ad3c30c72e34e7f096",  # Across Protocol: SpokePool
                ],
                "topics": [
                    "0x32ed1a409ef04c7b0227189c3a103dc5ac10e775a15b785dcc510201f7c25ad3",  # FundsDeposited
                    "0x44b559f101f8fbcc8a0ea43fa91a05a729a5ea6e14a7c75aa750374690137208",  # FilledRelay
                    "0xf4ad92585b1bc117fbdd644990adf0827bc4c95baeae8a23322af807b6d0020e",  # ExecutedRelayerRefundRoot
                ],
            },
        ],
        "optimism": [
            {
                "abi": "across",
                "contracts": [
                    "0x6f26Bf09B1C792e3228e5467807a900A503c0281",  # Across Protocol: SpokePool
                ],
                "topics": [
                    "0x32ed1a409ef04c7b0227189c3a103dc5ac10e775a15b785dcc510201f7c25ad3",  # FundsDeposited
                    "0x44b559f101f8fbcc8a0ea43fa91a05a729a5ea6e14a7c75aa750374690137208",  # FilledRelay
                    "0xf4ad92585b1bc117fbdd644990adf0827bc4c95baeae8a23322af807b6d0020e",  # ExecutedRelayerRefundRoot
                ],
            }
        ],
        "base": [
            {
                "abi": "across",
                "contracts": [
                    "0x09aea4b2242abC8bb4BB78D537A67a245A7bEC64",  # Across Protocol: SpokePool
                ],
                "topics": [
                    "0x32ed1a409ef04c7b0227189c3a103dc5ac10e775a15b785dcc510201f7c25ad3",  # FundsDeposited
                    "0x44b559f101f8fbcc8a0ea43fa91a05a729a5ea6e14a7c75aa750374690137208",  # FilledRelay
                    "0xf4ad92585b1bc117fbdd644990adf0827bc4c95baeae8a23322af807b6d0020e",  # ExecutedRelayerRefundRoot
                ],
            }
        ],
        "scroll": [
            {
                "abi": "across",
                "contracts": [
                    "0x3bad7ad0728f9917d1bf08af5782dcbd516cdd96",  # Across Protocol: SpokePool
                ],
                "topics": [
                    "0x32ed1a409ef04c7b0227189c3a103dc5ac10e775a15b785dcc510201f7c25ad3",  # FundsDeposited
                    "0x44b559f101f8fbcc8a0ea43fa91a05a729a5ea6e14a7c75aa750374690137208",  # FilledRelay
                    "0xf4ad92585b1bc117fbdd644990adf0827bc4c95baeae8a23322af807b6d0020e",  # ExecutedRelayerRefundRoot
                ],
            }
        ],
        "linea": [
            {
                "abi": "across",
                "contracts": [
                    "0x7e63a5f1a8f0b4d0934b2f2327daed3f6bb2ee75",  # Across Protocol: SpokePool
                ],
                "topics": [
                    "0x32ed1a409ef04c7b0227189c3a103dc5ac10e775a15b785dcc510201f7c25ad3",  # FundsDeposited
                    "0x44b559f101f8fbcc8a0ea43fa91a05a729a5ea6e14a7c75aa750374690137208",  # FilledRelay
                    "0xf4ad92585b1bc117fbdd644990adf0827bc4c95baeae8a23322af807b6d0020e",  # ExecutedRelayerRefundRoot
                ],
            }
        ],
    }
}
