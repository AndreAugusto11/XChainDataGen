# Mapping of bridges to their supported blockchains and contracts
BRIDGE_CONFIG = {
    "blockchains": {
        "ethereum": [
            {
                "abi": "messenger",
                "contracts": [
                    "0xbd3fa81b58ba92a82136038b25adec7066af3155",  # Circle: Token Messenger
                ],
                "topics": [
                    "0x2fa9ca894982930190727e75500a97d8dc500233a5065e0f3126c48fbe0343c0",  # DepositForBurn
                ],
            },
            {
                "abi": "transmitter",
                "contracts": [
                    "0x0a992d191deec32afe36203ad87d7d289a738f81",  # Circle: Message Transmitter
                ],
                "topics": [
                    "0x58200b4c34ae05ee816d710053fff3fb75af4395915d3d2a771b24aa10e3cc5d",  # MessageReceived (we could listen to the MintAndWithdraw event as well, but the data is the same)
                ],
            },
        ],
        "arbitrum": [
            {
                "abi": "messenger",
                "contracts": [
                    "0x19330d10d9cc8751218eaf51e8885d058642e08a",  # Circle: Token Messenger
                ],
                "topics": [
                    "0x2fa9ca894982930190727e75500a97d8dc500233a5065e0f3126c48fbe0343c0",  # DepositForBurn
                ],
            },
            {
                "abi": "transmitter",
                "contracts": [
                    "0xc30362313fbba5cf9163f0bb16a0e01f01a896ca",  # Circle: Message Transmitter
                ],
                "topics": [
                    "0x58200b4c34ae05ee816d710053fff3fb75af4395915d3d2a771b24aa10e3cc5d",  # MessageReceived (we could listen to the MintAndWithdraw event as well, but the data is the same)
                ],
            },
        ],
        "avalanche": [
            {
                "abi": "messenger",
                "contracts": [
                    "0x6B25532e1060CE10cc3B0A99e5683b91BFDe6982",  # Circle: Token Messenger
                ],
                "topics": [
                    "0x2fa9ca894982930190727e75500a97d8dc500233a5065e0f3126c48fbe0343c0",  # DepositForBurn
                ],
            },
            {
                "abi": "transmitter",
                "contracts": [
                    "0x8186359aF5F57FbB40c6b14A588d2A59C0C29880",  # Circle: Message Transmitter
                ],
                "topics": [
                    "0x58200b4c34ae05ee816d710053fff3fb75af4395915d3d2a771b24aa10e3cc5d",  # MessageReceived (we could listen to the MintAndWithdraw event as well, but the data is the same)
                ],
            },
        ],
        "polygon": [
            {
                "abi": "messenger",
                "contracts": [
                    "0x9daf8c91aefae50b9c0e69629d3f6ca40ca3b3fe",  # Circle: Token Messenger
                ],
                "topics": [
                    "0x2fa9ca894982930190727e75500a97d8dc500233a5065e0f3126c48fbe0343c0",  # DepositForBurn
                ],
            },
            {
                "abi": "transmitter",
                "contracts": [
                    "0xf3be9355363857f3e001be68856a2f96b4c39ba9",  # Circle: Message Transmitter
                ],
                "topics": [
                    "0x58200b4c34ae05ee816d710053fff3fb75af4395915d3d2a771b24aa10e3cc5d",  # MessageReceived (we could listen to the MintAndWithdraw event as well, but the data is the same)
                ],
            },
        ],
        "optimism": [
            {
                "abi": "messenger",
                "contracts": [
                    "0x2b4069517957735be00cee0fadae88a26365528f",  # Circle: Token Messenger
                ],
                "topics": [
                    "0x2fa9ca894982930190727e75500a97d8dc500233a5065e0f3126c48fbe0343c0",  # DepositForBurn
                ],
            },
            {
                "abi": "transmitter",
                "contracts": [
                    "0x4d41f22c5a0e5c74090899e5a8fb597a8842b3e8",  # Circle: Message Transmitter
                ],
                "topics": [
                    "0x58200b4c34ae05ee816d710053fff3fb75af4395915d3d2a771b24aa10e3cc5d",  # MessageReceived (we could listen to the MintAndWithdraw event as well, but the data is the same)
                ],
            },
        ],
        "base": [
            {
                "abi": "messenger",
                "contracts": [
                    "0x1682ae6375c4e4a97e4b583bc394c861a46d8962",  # Circle: Token Messenger
                ],
                "topics": [
                    "0x2fa9ca894982930190727e75500a97d8dc500233a5065e0f3126c48fbe0343c0",  # DepositForBurn
                ],
            },
            {
                "abi": "transmitter",
                "contracts": [
                    "0xad09780d193884d503182ad4588450c416d6f9d4",  # Circle: Message Transmitter
                ],
                "topics": [
                    "0x58200b4c34ae05ee816d710053fff3fb75af4395915d3d2a771b24aa10e3cc5d",  # MessageReceived (we could listen to the MintAndWithdraw event as well, but the data is the same)
                ],
            },
        ],
    }
}


BLOCKCHAIN_IDS = {
    "6": {
        "nativeChainId": 8453,
        "name": "base",
    },
    "2": {
        "nativeChainId": 10,
        "name": "optimism",
    },
    "3": {
        "nativeChainId": 42161,
        "name": "arbitrum",
    },
    "7": {
        "nativeChainId": 137,
        "name": "polygon",
    },
    "1": {
        "nativeChainId": 43114,
        "name": "avalanche",
    },
    "0": {
        "nativeChainId": 1,
        "name": "ethereum",
    },
}
