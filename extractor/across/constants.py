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
                    "0xa123dc29aebf7d0c3322c8eeb5b999e859f39937950ed31056532713d0de396f",  # V3FundsDeposited
                    "0x571749edf1d5c9599318cdbc4e28a6475d65e87fd3b2ddbe1e9a8d5e7a0f0ff7",  # FilledV3Relay
                    "0xf8bd640004bcec1b89657020f561d0b070cbdf662d0b158db9dccb0a8301bfab",  # ExecutedRelayerRefundRoot
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
                    "0xa123dc29aebf7d0c3322c8eeb5b999e859f39937950ed31056532713d0de396f",  # V3FundsDeposited
                    "0x571749edf1d5c9599318cdbc4e28a6475d65e87fd3b2ddbe1e9a8d5e7a0f0ff7",  # FilledV3Relay
                    "0xf8bd640004bcec1b89657020f561d0b070cbdf662d0b158db9dccb0a8301bfab",  # ExecutedRelayerRefundRoot
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
                    "0xa123dc29aebf7d0c3322c8eeb5b999e859f39937950ed31056532713d0de396f",  # V3FundsDeposited
                    "0x571749edf1d5c9599318cdbc4e28a6475d65e87fd3b2ddbe1e9a8d5e7a0f0ff7",  # FilledV3Relay
                    "0xf8bd640004bcec1b89657020f561d0b070cbdf662d0b158db9dccb0a8301bfab",  # ExecutedRelayerRefundRoot
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
                    "0xa123dc29aebf7d0c3322c8eeb5b999e859f39937950ed31056532713d0de396f",  # V3FundsDeposited
                    "0x571749edf1d5c9599318cdbc4e28a6475d65e87fd3b2ddbe1e9a8d5e7a0f0ff7",  # FilledV3Relay
                    "0xf8bd640004bcec1b89657020f561d0b070cbdf662d0b158db9dccb0a8301bfab",  # ExecutedRelayerRefundRoot
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
                    "0xa123dc29aebf7d0c3322c8eeb5b999e859f39937950ed31056532713d0de396f",  # V3FundsDeposited
                    "0x571749edf1d5c9599318cdbc4e28a6475d65e87fd3b2ddbe1e9a8d5e7a0f0ff7",  # FilledV3Relay
                    "0xf8bd640004bcec1b89657020f561d0b070cbdf662d0b158db9dccb0a8301bfab",  # ExecutedRelayerRefundRoot
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
                    "0xa123dc29aebf7d0c3322c8eeb5b999e859f39937950ed31056532713d0de396f",  # V3FundsDeposited
                    "0x571749edf1d5c9599318cdbc4e28a6475d65e87fd3b2ddbe1e9a8d5e7a0f0ff7",  # FilledV3Relay
                    "0xf8bd640004bcec1b89657020f561d0b070cbdf662d0b158db9dccb0a8301bfab",  # ExecutedRelayerRefundRoot
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
                    "0xa123dc29aebf7d0c3322c8eeb5b999e859f39937950ed31056532713d0de396f",  # V3FundsDeposited
                    "0x571749edf1d5c9599318cdbc4e28a6475d65e87fd3b2ddbe1e9a8d5e7a0f0ff7",  # FilledV3Relay
                    "0xf8bd640004bcec1b89657020f561d0b070cbdf662d0b158db9dccb0a8301bfab",  # ExecutedRelayerRefundRoot
                ],
            }
        ],
    }
}
