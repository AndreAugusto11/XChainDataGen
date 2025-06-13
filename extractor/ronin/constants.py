# Mapping of bridges to their supported blockchains and contracts
BRIDGE_CONFIG = {
    "blockchains": {
        "ethereum": [
            {
                "abi": "0x64192819Ac13Ef72bF6b5AE239AC672B43a9AF08",
                "contracts": [
                    "0x64192819Ac13Ef72bF6b5AE239AC672B43a9AF08",  # Axie Infinity: Ronin Bridge V2
                ],
                "topics": [
                    "0x21e88e956aa3e086f6388e899965cef814688f99ad8bb29b08d396571016372d",  # Withdrew
                    "0xd7b25068d9dc8d00765254cfb7f5070f98d263c8d68931d937c7362fa738048b",  # DepositRequested
                ],
            },
        ],
        "ronin": [
            {
                "abi": "0x0cf8ff40a508bdbc39fbe1bb679dcba64e65c7df",
                "contracts": [
                    "0x0cf8ff40a508bdbc39fbe1bb679dcba64e65c7df",  # Ronin Gateway V3
                ],
                "topics": [
                    "0xf313c253a5be72c29d0deb2c8768a9543744ac03d6b3cafd50cc976f1c2632fc",  # WithdrawalRequested
                    "0x8d20d8121a34dded9035ff5b43e901c142824f7a22126392992c353c37890524",  # Deposited
                ],
            },
        ],
    }
}
