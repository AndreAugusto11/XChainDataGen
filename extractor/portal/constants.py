# Mapping of bridges to their supported blockchains and contracts
BRIDGE_CONFIG = {
    "blockchains": {
        "ethereum": [
            {
                "abi": "wormhole-core-bridge",
                "contracts": [
                    "0x98f3c9e6e3face36baad05fe09d375ef1464288b",  # Wormhole: Ethereum Core Bridge
                ],
                "topics": [
                    "0x6eb224fb001ed210e379b335e35efe88672a8ce935d981a6896b27ffdf52a3b2",  # LogMessagePublished (index_topic_1 address sender, uint64 sequence, uint32 nonce, bytes payload, uint8 consistencyLevel)
                ],
            },
            {
                "abi": "portal-token-bridge",
                "contracts": [
                    "0x3ee18b2214aff97000d974cf647e7c347e8fa585",  # Wormhole: Portal Token Bridge
                ],
                "topics": [
                    "0xcaf280c8cfeba144da67230d9b009c8f868a75bac9a528fa0474be1ba317c169",  # TransferRedeemed (index_topic_1 uint16 emitterChain, index_topic_2 address emitter, uint64 sequence, bytes data)
                ],
            },
        ],
        "bnb": [
            {
                "abi": "wormhole-core-bridge",
                "contracts": [
                    "0x98f3c9e6e3face36baad05fe09d375ef1464288b",  
                ],
                "topics": [
                    "0x6eb224fb001ed210e379b335e35efe88672a8ce935d981a6896b27ffdf52a3b2",  # LogMessagePublished (index_topic_1 address sender, uint64 sequence, uint32 nonce, bytes payload, uint8 consistencyLevel)
                ],
            },
            {
                "abi": "portal-token-bridge",
                "contracts": [
                    "0xb6f6d86a8f9879a9c87f643768d9efc38c1da6e7",  
                ],
                "topics": [
                    "0xcaf280c8cfeba144da67230d9b009c8f868a75bac9a528fa0474be1ba317c169",  # TransferRedeemed (index_topic_1 uint16 emitterChain, index_topic_2 address emitter, uint64 sequence, bytes data)
                ],
            },
        ],
        "arbitrum": [
            {
                "abi": "wormhole-core-bridge",
                "contracts": [
                    "0xa5f208e072434bc67592e4c49c1b991ba79bca46",  
                ],
                "topics": [
                    "0x6eb224fb001ed210e379b335e35efe88672a8ce935d981a6896b27ffdf52a3b2",  # LogMessagePublished (index_topic_1 address sender, uint64 sequence, uint32 nonce, bytes payload, uint8 consistencyLevel)
                ],
            },
            {
                "abi": "portal-token-bridge",
                "contracts": [
                    "0x0b2402144bb366a632d14b83f244d2e0e21bd39c",  
                ],
                "topics": [
                    "0xcaf280c8cfeba144da67230d9b009c8f868a75bac9a528fa0474be1ba317c169",  # TransferRedeemed (index_topic_1 uint16 emitterChain, index_topic_2 address emitter, uint64 sequence, bytes data)
                ],
            },
        ],
        "polygon": [
            {
                "abi": "wormhole-core-bridge",
                "contracts": [
                    "0x7a4b5a56256163f07b2c80a7ca55abe66c4ec4d7",  
                ],
                "topics": [
                    "0x6eb224fb001ed210e379b335e35efe88672a8ce935d981a6896b27ffdf52a3b2",  # LogMessagePublished (index_topic_1 address sender, uint64 sequence, uint32 nonce, bytes payload, uint8 consistencyLevel)
                ],
            },
            {
                "abi": "portal-token-bridge",
                "contracts": [
                    "0x5a58505a96d1dbf8df91cb21b54419fc36e93fde",  
                ],
                "topics": [
                    "0xcaf280c8cfeba144da67230d9b009c8f868a75bac9a528fa0474be1ba317c169",  # TransferRedeemed (index_topic_1 uint16 emitterChain, index_topic_2 address emitter, uint64 sequence, bytes data)
                ],
            },
        ],
        "optimism": [
            {
                "abi": "wormhole-core-bridge",
                "contracts": [
                    "0xee91c335eab126df5fdb3797ea9d6ad93aec9722",  
                ],
                "topics": [
                    "0x6eb224fb001ed210e379b335e35efe88672a8ce935d981a6896b27ffdf52a3b2",  # LogMessagePublished (index_topic_1 address sender, uint64 sequence, uint32 nonce, bytes payload, uint8 consistencyLevel)
                ],
            },
            {
                "abi": "portal-token-bridge",
                "contracts": [
                    "0x1d68124e65fafc907325e3edbf8c4d84499daa8b",  
                ],
                "topics": [
                    "0xcaf280c8cfeba144da67230d9b009c8f868a75bac9a528fa0474be1ba317c169",  # TransferRedeemed (index_topic_1 uint16 emitterChain, index_topic_2 address emitter, uint64 sequence, bytes data)
                ],
            },
        ],
        "avalanche": [
            {
                "abi": "wormhole-core-bridge",
                "contracts": [
                    "0x54a8e5f9c4CbA08F9943965859F6c34eAF03E26c",  
                ],
                "topics": [
                    "0x6eb224fb001ed210e379b335e35efe88672a8ce935d981a6896b27ffdf52a3b2",  # LogMessagePublished (index_topic_1 address sender, uint64 sequence, uint32 nonce, bytes payload, uint8 consistencyLevel)
                ],
            },
            {
                "abi": "portal-token-bridge",
                "contracts": [
                    "0x0e082F06FF657D94310cB8cE8B0D9a04541d8052",  
                ],
                "topics": [
                    "0xcaf280c8cfeba144da67230d9b009c8f868a75bac9a528fa0474be1ba317c169",  # TransferRedeemed (index_topic_1 uint16 emitterChain, index_topic_2 address emitter, uint64 sequence, bytes data)
                ],
            },
        ],
        "base": [
            {
                "abi": "wormhole-core-bridge",
                "contracts": [
                    "0xbebdb6c8ddc678ffa9f8748f85c815c556dd8ac6",  
                ],
                "topics": [
                    "0x6eb224fb001ed210e379b335e35efe88672a8ce935d981a6896b27ffdf52a3b2",  # LogMessagePublished (index_topic_1 address sender, uint64 sequence, uint32 nonce, bytes payload, uint8 consistencyLevel)
                ],
            },
            {
                "abi": "portal-token-bridge",
                "contracts": [
                    "0x8d2de8d2f73f1f4cab472ac9a881c9b123c79627",  
                ],
                "topics": [
                    "0xcaf280c8cfeba144da67230d9b009c8f868a75bac9a528fa0474be1ba317c169",  # TransferRedeemed (index_topic_1 uint16 emitterChain, index_topic_2 address emitter, uint64 sequence, bytes data)
                ],
            },
        ],
        "scroll": [
            {
                "abi": "wormhole-core-bridge",
                "contracts": [
                    "0xbebdb6C8ddC678FfA9f8748f85C815C556Dd8ac6",  
                ],
                "topics": [
                    "0x6eb224fb001ed210e379b335e35efe88672a8ce935d981a6896b27ffdf52a3b2",  # LogMessagePublished (index_topic_1 address sender, uint64 sequence, uint32 nonce, bytes payload, uint8 consistencyLevel)
                ],
            },
            {
                "abi": "portal-token-bridge",
                "contracts": [
                    "0x24850c6f61C438823F01B7A3BF2B89B72174Fa9d",  
                ],
                "topics": [
                    "0xcaf280c8cfeba144da67230d9b009c8f868a75bac9a528fa0474be1ba317c169",  # TransferRedeemed (index_topic_1 uint16 emitterChain, index_topic_2 address emitter, uint64 sequence, bytes data)
                ],
            },
        ],
    }
}


BLOCKCHAIN_IDS = {
    30: {
        "nativeChainId": 8453,
        "name": "base",
    },
    24: {
        "nativeChainId": 10,
        "name": "optimism",
    },
    23: {
        "nativeChainId": 42161,
        "name": "arbitrum",
    },
    5: {
        "nativeChainId": 137,
        "name": "polygon",
    },
    6: {
        "nativeChainId": 43114,
        "name": "avalanche",
    },
    4: {
        "nativeChainId": 56,
        "name": "bnb",
    },
    2: {
        "nativeChainId": 1,
        "name": "ethereum",
    },
    38: {
        "nativeChainId": 59144,
        "name": "linea",
    },
    34: {
        "nativeChainId": 534352,
        "name": "scroll",
    }
}