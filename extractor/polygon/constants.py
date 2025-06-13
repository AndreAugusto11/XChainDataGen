# Mapping of bridges to their supported blockchains and contracts
BRIDGE_CONFIG = {
    "blockchains": {
        "ethereum": [
            {
                "abi": "0x28e4f3a7f651294b9564800b2d01f35189a5bfbe",
                "contracts": [
                    "0x28e4f3a7f651294b9564800b2d01f35189a5bfbe",  # Polygon (Matic): State Syncer
                ],
                "topics": [
                    "0x103fed9db65eac19c4d870f49ab7520fe03b99f1838e5996caf47e9e43308392",  # StateSynced
                ],
            },
            {
                "abi": "0x40ec5b33f54e0e8a33a975908c5ba1c14e5bbbdf",
                "contracts": [
                    "0x40ec5b33f54e0e8a33a975908c5ba1c14e5bbbdf",  # Polygon (Matic): ERC20 Bridge
                ],
                "topics": [
                    "0x9b217a401a5ddf7c4d474074aff9958a18d48690d77cc2151c4706aa7348b401",  # LockedERC20
                    "0xbb61bd1b26b3684c7c028ff1a8f6dabcac2fac8ac57b66fa6b1efb6edeab03c4",  # ExitedERC20
                ],
            },
            {
                "abi": "0x8484ef722627bf18ca5ae6bcf031c23e6e922b30",
                "contracts": [
                    "0x8484ef722627bf18ca5ae6bcf031c23e6e922b30",  # Polygon (Matic): Ether Bridge
                ],
                "topics": [
                    "0x3e799b2d61372379e767ef8f04d65089179b7a6f63f9be3065806456c7309f1b",  # LockedEther
                    "0x0fc0eed41f72d3da77d0f53b9594fc7073acd15ee9d7c536819a70a67c57ef3c",  # ExitedEther
                ],
            },
            {
                "abi": "0x401f6c983ea34274ec46f84d70b31c151321188b",
                "contracts": [
                    "0x401f6c983ea34274ec46f84d70b31c151321188b",  # Polygon (Matic): Plasma Bridge
                ],
                "topics": [
                    "0x1dadc8d0683c6f9824e885935c1bec6f76816730dcec148dda8cf25a7b9f797b",  # NewDepositBlock
                ],
            },
            {
                "abi": "0x2a88696e0ffa76baa1338f2c74497cc013495922",
                "contracts": [
                    "0x2a88696e0ffa76baa1338f2c74497cc013495922",  # Polygon (Matic): Withdraw Manager Proxy
                ],
                "topics": [
                    "0xfeb2000dca3e617cd6f3a8bbb63014bb54a124aac6ccbf73ee7229b4cd01f120",  # Withdraw
                ],
            },
        ],
        "polygon": [
            {
                "abi": "0x0000000000000000000000000000000000001001",
                "contracts": [
                    "0x0000000000000000000000000000000000001001",  # StateReceiver
                ],
                "topics": [
                    "0x5a22725590b0a51c923940223f7458512164b1113359a735e86e7f27f44791ee",  # StateCommitted
                ],
            },
            {
                "abi": "0xd9c7c4ed4b66858301d0cb28cc88bf655fe34861",
                "contracts": [
                    "0xd9c7c4ed4b66858301d0cb28cc88bf655fe34861",  # Polygon: Child Chain
                ],
                "topics": [
                    "0xec3afb067bce33c5a294470ec5b29e6759301cd3928550490c6d48816cdc2f5d",  # TokenDeposited
                ],
            },
            {
                "abi": "0x0000000000000000000000000000000000001010",
                "contracts": [
                    "0x0000000000000000000000000000000000001010",  # Polygon: POL Token
                ],
                "topics": [
                    "0xebff2602b3f468259e1e99f613fed6691f3a6526effe6ef3e768ba7ae7a36c4f",  # Withdraw
                ],
            },
            # {
            #     we will need to listen to the Transfer events in the most used ERC20 contracts. below is a preliminary list
            # }
            # {
            #     "abi": "erc20",
            #     "contracts": [
            #         "0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619",
            #         "0xc2132D05D31c914a87C6611C10748AEb04B58e8F",
            #         "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",
            #         "	0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063",
            #         "0x1BFD67037B42Cf73acF2047067bd4F2C47D9BfD6",
            #         "0x467bccd9d29f223bce8043b84e8c8b282827790f",
            #         "0x25f8087ead173b73d6e8b84329989a8eea16cf73",
            #         "0x423071774c43c0aaf4210b439e7cda8c797e2f26",
            #         "0x0001a500a6b18995b03f44bb040a5ffc28e45cb0",
            #         "0x514910771af9ca656af840dff83e8264ecf986ca",
            #         "0x3845badade8e6dff049820680d1f14bd3903a5d0",
            #         "0x5b649c07e7ba0a1c529deaabed0b47699919b4a2",
            #         "0x7fc66500c84a76ad7e9c93437bfc5ac33e2ddae9",
            #         "0x5a98fcbea516cf06857215779fd812ca3bef1b32",
            #         "0x3593d125a4f7849a1b059e64f4517a86dd60c95d",
            #         "0xba100000625a3754423978a60c9317c58a424e3d",
            #         "0x967da4048cd07ab37855c090aaf366e4ce1b9f48",
            #         "0xb17548c7b510427baac4e267bea62e800b247173",
            #         "0x6de037ef9ad2725eb40118bb1702ebb27e4aeb24",
            #         "0x111111517e4929d3dcbdfa7cce55d30d4b6bc4d6",
            #         "0x55296f69f40ea6d20e478533c15a6b08b654e758",
            #         "0x249e38ea4102d0cf8264d3701f1a0e39c4f2dc3b",
            #         "0x340d2bde5eb28c1eed91b2f790723e3b160613b7",
            #         "0xd3e4ba569045546d09cf021ecc5dfe42b1d7f6e4",
            #         "0xe0bceef36f3a6efdd5eebfacd591423f8549b9d5",
            #         "0x7f39c581f595b53c5cb19bd0b3f8da6c935e2ca0",
            #         "0xd7d9babf56a66daff2ac5dc96f7e886c05124676",
            #         "0xc477d038d5420c6a9e0b031712f61c5120090de9",
            #         "0x6f40d4a6237c257fff2db00fa0510deeecd303eb",
            #         "0x9f9c8ec3534c3ce16f928381372bfbfbfb9f4d24",
            #         "0xe53ec727dbdeb9e2d5456c3be40cff031ab40a55",
            #         "0x4104b135dbc9609fc1a9490e61369036497660c8",
            #         "0x6b0b3a982b4634ac68dd83a4dbf02311ce324181",
            #         "0x7dd9c5cba05e151c895fde1cf355c9a1d5da6429",
            #         "0x06f3c323f0238c72bf35011071f2b5b7f43a054c",
            #         "0xb705268213d593b8fd88d3fdeff93aff5cbdcfae",
            #         "0x21bfbda47a0b4b5b1248c767ee49f7caa9b23697",
            #         "0xc28eb2250d1ae32c7e74cfb6d6b86afc9beb6509",
            #     ],
            #     "topics": [
            #         "", # Transfer
            #     ],
            # },
        ],
    }
}
