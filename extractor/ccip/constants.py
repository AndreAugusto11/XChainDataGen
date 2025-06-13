# Mapping of bridges to their supported blockchains and contracts
BRIDGE_CONFIG = {
    "blockchains": {
        "ethereum": [
            {
                "abi": "evm2evmonramp",
                "contracts": [
                    "0x69eCC4E2D8ea56E2d0a05bF57f4Fd6aEE7f2c284",  # EVM2EVMOnRamp arbitrum
                    "0xaFd31C0C78785aDF53E4c185670bfd5376249d8A",  # EVM2EVMOnRamp avalanche
                    "0x15a9D79d6b3485F70bF82bC49dDD1fcB37A7149c",  # EVM2EVMOnRamp polygon
                    "0x3455D8E039736944e66e19eAc77a42e8077B07bf",  # EVM2EVMOnRamp optimism
                    "0x948306C220Ac325fa9392A6E601042A3CD0b480d",  # EVM2EVMOnRamp bnb
                    "0xb8a882f3B88bd52D1Ff56A873bfDB84b70431937",  # EVM2EVMOnRamp base
                    "0xf50B9A46C394bD98491ce163d420222d8030F6F0",  # EVM2EVMOnRamp gnosis
                    "0xdC5b578ff3AFcC4A4a6E149892b9472390b50844",  # EVM2EVMOnRamp ronin
                    "0x626189C882A80fF0D036d8D9f6447555e81F78E9",  # EVM2EVMOnRamp linea
                    "0x362A221C3cfd7F992DFE221687323F0BA9BA8187",  # EVM2EVMOnRamp scroll
                ],
                "topics": [
                    "0xd0c3c799bf9e2639de44391e7f524d229b2b55f5b1ea94b2bf7da42f7243dddd",  # CCIPSendRequested
                ],
            },
            {
                "abi": "evm2evmofframp",
                "contracts": [
                    "0xdf615eF8D4C64d0ED8Fd7824BBEd2f6a10245aC9",  # EVM2EVMOffRamp arbitrum
                    "0xd98E80C79a15E4dbaF4C40B6cCDF690fe619BFBb",  # EVM2EVMOffRamp avalanche
                    "0x718672076D6d51E4c76142B37bC99E4945d704a3",  # EVM2EVMOffRamp polygon
                    "0x562a2025E60AA19Aa03Ea41D70ea1FD3286d1D3B",  # EVM2EVMOffRamp optimism
                    "0x66d84fedED0e51aeB47ceD1BB2fc0221Ae8D7C12",  # EVM2EVMOffRamp bnb
                    "0x6B4B6359Dd5B47Cdb030E5921456D2a0625a9EbD",  # EVM2EVMOffRamp base
                    "0x70C705ff3eCAA04c8c61d581a59a168a1c49c2ec",  # EVM2EVMOffRamp gnosis
                    "0x9a3Ed7007809CfD666999e439076B4Ce4120528D",  # EVM2EVMOffRamp ronin
                    "0x418dcbCf229897d0CCf1B8B464Db06C23879FBB4",  # EVM2EVMOffRamp linea
                    "0x26a10137A54F4Ea01D20758Ac5AdBf9326340Fc3",  # EVM2EVMOffRamp scroll
                ],
                "topics": [
                    "0xd4f851956a5d67c3997d1c9205045fef79bae2947fdee7e9e2641abc7391ef65",  # ExecutionStateChanged
                ],
            },
        ],
        "arbitrum": [
            {
                "abi": "evm2evmonramp",
                "contracts": [
                    "0x67761742ac8A21Ec4D76CA18cbd701e5A6F3Bef3",  # EVM2EVMOnRamp ethereum
                    "0xe80cC83B895ada027b722b78949b296Bd1fC5639",  # EVM2EVMOnRamp avalanche
                    "0x6087d6C33946670232DF09Fe93eECbaEa3D6864d",  # EVM2EVMOnRamp polygon
                    "0xAFECc7b67c6a8e606e94ce4e2F70D83C2206C2cb",  # EVM2EVMOnRamp optimism
                    "0x14bF7b1Ca6b843f386bfDfa76BFd439919b9378D",  # EVM2EVMOnRamp bnb
                    "0xc1b6287A3292d6469F2D8545877E40A2f75CA9a6",  # EVM2EVMOnRamp base
                    "0xCeAB512ed28727EeAB94698281F38A2c04b0ce78",  # EVM2EVMOnRamp linea
                ],
                "topics": [
                    "0xd0c3c799bf9e2639de44391e7f524d229b2b55f5b1ea94b2bf7da42f7243dddd",  # CCIPSendRequested
                ],
            },
            {
                "abi": "evm2evmofframp",
                "contracts": [
                    "0x91e46cc5590A4B9182e47f40006140A7077Dec31",  # EVM2EVMOffRamp ethereum
                    "0x95095007d5Cc3E7517A1A03c9e228adA5D0bc376",  # EVM2EVMOffRamp avalanche
                    "0xcabc2D71dC3172a154A5A34cD706B050e0ef9b6f",  # EVM2EVMOffRamp polygon
                    "0x27a971D482335d0f8d1917451390734f7372A4a3",  # EVM2EVMOffRamp optimism
                    "0x16B9709F8A23B9EB922E8Dde7EaB1Ede7C79F663",  # EVM2EVMOffRamp bnb
                    "0xb62178f8198905D0Fa6d640Bdb188E4E8143Ac4b",  # EVM2EVMOffRamp base
                    "0xCb1DBBb4Be5aEc889C65ff34882f1eAb2Cd5785B",  # EVM2EVMOffRamp linea
                ],
                "topics": [
                    "0xd4f851956a5d67c3997d1c9205045fef79bae2947fdee7e9e2641abc7391ef65",  # ExecutionStateChanged
                ],
            },
        ],
        "avalanche": [
            {
                "abi": "evm2evmonramp",
                "contracts": [
                    "0xe8784c29c583C52FA89144b9e5DD91Df2a1C2587",  # EVM2EVMOnRamp ethereum
                    "0x4e910c8Bbe88DaDF90baa6c1B7850DbeA32c5B29",  # EVM2EVMOnRamp arbitrum
                    "0x5570a4E979d7460F13b84075ACEF69FAc73914b1",  # EVM2EVMOnRamp polygon
                    "0x3e3b4Fba004E7824219e79aE9f676d9D41A216Fa",  # EVM2EVMOnRamp optimism
                    "0xe6e161d55019AA5960DcF0Af9bB6e4d574C69F99",  # EVM2EVMOnRamp bnb
                    "0x139D4108C23e66745Eda4ab47c25C83494b7C14d",  # EVM2EVMOnRamp base
                    "0xc432b86153Eb64D46ecea00591EE7CBc27538c4b",  # EVM2EVMOnRamp linea
                ],
                "topics": [
                    "0xd0c3c799bf9e2639de44391e7f524d229b2b55f5b1ea94b2bf7da42f7243dddd",  # CCIPSendRequested
                ],
            },
            {
                "abi": "evm2evmofframp",
                "contracts": [
                    "0xE5F21F43937199D4D57876A83077b3923F68EB76",  # EVM2EVMOffRamp ethereum
                    "0x508Ea280D46E4796Ce0f1Acf8BEDa610c4238dB3",  # EVM2EVMOffRamp arbitrum
                    "0xFf49E35626Eba28Bee1d251782AB75A6cEd91c45",  # EVM2EVMOffRamp polygon
                    "0x376C0AFC9E64efE0d9202E1F02c3d7f9Dc15e404",  # EVM2EVMOffRamp optimism
                    "0x6CDAa2711BdF0B719911BF00588A79FA97bf9264",  # EVM2EVMOffRamp bnb
                    "0x37879EBFCb807f8C397fCe2f42DC0F5329AD6823",  # EVM2EVMOffRamp base
                    "0x6A3CEf8e5CA7135C574f69d0b58dd0ac9DB2D892",  # EVM2EVMOffRamp linea
                ],
                "topics": [
                    "0xd4f851956a5d67c3997d1c9205045fef79bae2947fdee7e9e2641abc7391ef65",  # ExecutionStateChanged
                ],
            },
        ],
        "polygon": [
            {
                "abi": "evm2evmonramp",
                "contracts": [
                    "0x1DAcBae00c779913e6E9fc1A3323FbA4847ba53C",  # EVM2EVMOnRamp ethereum
                    "0x13263aC754d1e29430930672E3C0019f2BC44Ba2",  # EVM2EVMOnRamp arbitrum
                    "0x56cb9Cd82553Bd8157e6504020c38f6DA4971717",  # EVM2EVMOnRamp avalanche
                    "0x868B71490B36674B3B9006fa8711C6fA26A26631",  # EVM2EVMOnRamp optimism
                    "0x164507757F7d5Ab35C6af44EeEB099F5be29Da57",  # EVM2EVMOnRamp bnb
                    "0xD26A4E0c664E72e3c29E634867191cB1cb9AF570",  # EVM2EVMOnRamp base
                ],
                "topics": [
                    "0xd0c3c799bf9e2639de44391e7f524d229b2b55f5b1ea94b2bf7da42f7243dddd",  # CCIPSendRequested
                ],
            },
            {
                "abi": "evm2evmofframp",
                "contracts": [
                    "0xa06e68a11d5694316Cc819f2FFD02663e3314C7C",  # EVM2EVMOffRamp ethereum
                    "0x60f2788225CeE4a94f8E7589931d5A14Cbc4367d",  # EVM2EVMOffRamp arbitrum
                    "0x35c1Bb5A9c2F3fa8f8dFF470a6bE7d362CeA1ef3",  # EVM2EVMOffRamp avalanche
                    "0x805c292775Be43b10Cc744ea7E81d9939a08cEa4",  # EVM2EVMOffRamp optimism
                    "0xE58074f8F56E23836f088Ac8b4f3882c1b4CAcbb",  # EVM2EVMOffRamp bnb
                    "0xF4a9Dbb7f3FBa02e3a244B464e459C32B63857F1",  # EVM2EVMOffRamp base
                ],
                "topics": [
                    "0xd4f851956a5d67c3997d1c9205045fef79bae2947fdee7e9e2641abc7391ef65",  # ExecutionStateChanged
                ],
            },
        ],
        "optimism": [
            {
                "abi": "evm2evmonramp",
                "contracts": [
                    "0xE4C51Dc01A4E0aB14c7a7a2ed1655E9CF8A3E698",  # EVM2EVMOnRamp ethereum
                    "0x6bA81b83091A23e8F2AA173B2b939fAf9E320DfB",  # EVM2EVMOnRamp arbitrum
                    "0xB9D655Ad5ba80036725d6c753Fa6AF0454cBF630",  # EVM2EVMOnRamp avalanche
                    "0x9c725164b60E3f6d4d5b7A2841C63E9FD0988805",  # EVM2EVMOnRamp polygon
                    "0xfC51a4CF925f202d86c6092cda879689d2C17201",  # EVM2EVMOnRamp bnb
                    "0xfE11cfC957cCa331192EAC60040b442303CcA0a9",  # EVM2EVMOnRamp base
                ],
                "topics": [
                    "0xd0c3c799bf9e2639de44391e7f524d229b2b55f5b1ea94b2bf7da42f7243dddd",  # CCIPSendRequested
                ],
            },
            {
                "abi": "evm2evmofframp",
                "contracts": [
                    "0x9979c2dfEcA9051Cf7f08274d978984B2dB12C60",  # EVM2EVMOffRamp ethereum
                    "0xEB3d6956BCf7b1E29634C8cd182fC9FA740Bce34",  # EVM2EVMOffRamp arbitrum
                    "0xF8E38B4503418659F791F2135c4912F85BFB7988",  # EVM2EVMOffRamp avalanche
                    "0x4BA0A3bD1E2b70b2fe165A53219e7eF6376849a4",  # EVM2EVMOffRamp polygon
                    "0x51f37b538aD2Bcb9Eaf884859BF7C5Ec58AEc885",  # EVM2EVMOffRamp bnb
                    "0x519ee6B83f57df95486aeA6E26819cb7b4B8ee99",  # EVM2EVMOffRamp base
                ],
                "topics": [
                    "0xd4f851956a5d67c3997d1c9205045fef79bae2947fdee7e9e2641abc7391ef65",  # ExecutionStateChanged
                ],
            },
        ],
        "bnb": [
            {
                "abi": "evm2evmonramp",
                "contracts": [
                    "0x35C724666ba31632A56Bad4390eb69f206ab60C7",  # EVM2EVMOnRamp ethereum
                    "0x5577c19bD183e39a007ce4CE236f1D91e9132D5c",  # EVM2EVMOnRamp arbitrum
                    "0x43F00dBf0Aa61A099c674A74FBdCb93786564950",  # EVM2EVMOnRamp avalanche
                    "0x1C88e3Fd2B0a8735D1b19A77AA6e2333555BB95c",  # EVM2EVMOnRamp polygon
                    "0x3A3649852A518ab180f41f28288c6c9184563616",  # EVM2EVMOnRamp optimism
                    "0xdABb6De5eC48dd2fcF28ac85CbEFe3F19E03F1BD",  # EVM2EVMOnRamp base
                    "0x86768B77C971524D5042631749A59527E8a9604d",  # EVM2EVMOnRamp linea
                ],
                "topics": [
                    "0xd0c3c799bf9e2639de44391e7f524d229b2b55f5b1ea94b2bf7da42f7243dddd",  # CCIPSendRequested
                ],
            },
            {
                "abi": "evm2evmofframp",
                "contracts": [
                    "0xF616733641D420207b8F30db9C4cE39684768991",  # EVM2EVMOffRamp ethereum
                    "0x2A9C65afF39758CeAa24dBD1ACd1BeB3618e6780",  # EVM2EVMOffRamp arbitrum
                    "0xc69a550470bEbC5c3Be98A4C3dD26C6AdD90C64b",  # EVM2EVMOffRamp avalanche
                    "0x21159ebdA3E6A2437bCD6ef39853042ACC436D2D",  # EVM2EVMOffRamp polygon
                    "0x3c5E62cdFD08e23a0961ff2A3155CaBb96cbc89D",  # EVM2EVMOffRamp optimism
                    "0x133672C0F0067573254dd7C8C9818a37d6208610",  # EVM2EVMOffRamp base
                    "0x0c42a007BF89DC2CAfAb3fbd2eC1C1cA5BFe7d7C",  # EVM2EVMOffRamp linea
                ],
                "topics": [
                    "0xd4f851956a5d67c3997d1c9205045fef79bae2947fdee7e9e2641abc7391ef65",  # ExecutionStateChanged
                ],
            },
        ],
        "base": [
            {
                "abi": "evm2evmonramp",
                "contracts": [
                    "0x56b30A0Dcd8dc87Ec08b80FA09502bAB801fa78e",  # EVM2EVMOnRamp ethereum
                    "0x9D0ffA76C7F82C34Be313b5bFc6d42A72dA8CA69",  # EVM2EVMOnRamp arbitrum
                    "0x4be6E0F97EA849FF80773af7a317356E6c646FD7",  # EVM2EVMOnRamp avalanche
                    "0xd3Bde678BB706Cf727A512515C254BcF021dD203",  # EVM2EVMOnRamp polygon
                    "0x362E6bE957c18e268ad91046CA6b47EB09AD98C1",  # EVM2EVMOnRamp optimism
                    "0xE5FD5A0ec3657Ad58E875518e73F6264E00Eb754",  # EVM2EVMOnRamp bnb
                    "0xB1ddDDe9C1e88DF7751f8f2cf18569B13C8AF670",  # EVM2EVMOnRamp linea
                ],
                "topics": [
                    "0xd0c3c799bf9e2639de44391e7f524d229b2b55f5b1ea94b2bf7da42f7243dddd",  # CCIPSendRequested
                ],
            },
            {
                "abi": "evm2evmofframp",
                "contracts": [
                    "0xCA04169671A81E4fB8768cfaD46c347ae65371F1",  # EVM2EVMOffRamp ethereum
                    "0x7D38c6363d5E4DFD500a691Bc34878b383F58d93",  # EVM2EVMOffRamp arbitrum
                    "0x61C3f6d72c80A3D1790b213c4cB58c3d4aaFccDF",  # EVM2EVMOffRamp avalanche
                    "0x74d574D11977fC8D40f8590C419504cbE178ADB7",  # EVM2EVMOffRamp polygon
                    "0x18095fbD53184A50C2BB3929a6c62Ca328732062",  # EVM2EVMOffRamp optimism
                    "0x45d524b6Fe99C005C52C65c578dc0e02d9751083",  # EVM2EVMOffRamp bnb
                    "0x335581943Ef47030e52E4Fe921d4b72d15a20aB3",  # EVM2EVMOffRamp linea
                ],
                "topics": [
                    "0xd4f851956a5d67c3997d1c9205045fef79bae2947fdee7e9e2641abc7391ef65",  # ExecutionStateChanged
                ],
            },
        ],
        "gnosis": [
            {
                "abi": "evm2evmonramp",
                "contracts": [
                    "0x014ABcfDbCe9F67d0Df34574664a6C0A241Ec03A",  # EVM2EVMOnRamp ethereum
                ],
                "topics": [
                    "0xd0c3c799bf9e2639de44391e7f524d229b2b55f5b1ea94b2bf7da42f7243dddd",  # CCIPSendRequested
                ],
            },
            {
                "abi": "evm2evmofframp",
                "contracts": [
                    "0x658d9ae41A9c291De423d3B4B6C064f6dD0e7Ed2",  # EVM2EVMOffRamp ethereum
                ],
                "topics": [
                    "0xd4f851956a5d67c3997d1c9205045fef79bae2947fdee7e9e2641abc7391ef65",  # ExecutionStateChanged
                ],
            },
        ],
        "ronin": [
            {
                "abi": "evm2evmonramp",
                "contracts": [
                    "0x02b60267bceeaFDC45005e0Fa0dd783eFeBc9F1b",  # EVM2EVMOnRamp ethereum
                ],
                "topics": [
                    "0xd0c3c799bf9e2639de44391e7f524d229b2b55f5b1ea94b2bf7da42f7243dddd",  # CCIPSendRequested
                ],
            },
            {
                "abi": "evm2evmofframp",
                "contracts": [
                    "0x320A10449556388503Fd71D74A16AB52e0BD1dEb",  # EVM2EVMOffRamp ethereum
                ],
                "topics": [
                    "0xd4f851956a5d67c3997d1c9205045fef79bae2947fdee7e9e2641abc7391ef65",  # ExecutionStateChanged
                ],
            },
        ],
        "linea": [
            {
                "abi": "evm2evmonramp",
                "contracts": [
                    "0x69AbB6043BBEA2467f41CCD0144d1b3b4ECd20f4",  # EVM2EVMOnRamp ethereum
                    "0x6d297Db3471057D7d014D7100A073de2e2656b8F",  # EVM2EVMOnRamp arbitrum
                    "0x03dD4319019435D8FD5aE5920B96f37989EA410e",  # EVM2EVMOnRamp avalanche
                    "0x39ee3A92a5E836eD5a3CceB6B6F00481B5093b3e",  # EVM2EVMOnRamp base
                    "0xd0F398854358f8846596C78f8363F3d182e77cC8",  # EVM2EVMOnRamp bnb
                    "0x30ebb71dAa827bEAE71EE325A77Ca47dAED7Ec9B",  # EVM2EVMOnRamp scroll
                ],
                "topics": [
                    "0xd0c3c799bf9e2639de44391e7f524d229b2b55f5b1ea94b2bf7da42f7243dddd",  # CCIPSendRequested
                ],
            },
            {
                "abi": "evm2evmofframp",
                "contracts": [
                    "0x656e2aA127Cb15815a90Ef70c6AA7Ed449D689ce",  # EVM2EVMOffRamp ethereum
                    "0x90388147f034A60Adc4FbE9dc93084bab639D047",  # EVM2EVMOffRamp arbitrum
                    "0xd2f4330dc0f587770f0fCb61F8D96409f4BD23Fe",  # EVM2EVMOffRamp avalanche
                    "0x502eAaF47ECC410ed5f7b39Dd476d0d05Ae55864",  # EVM2EVMOffRamp base
                    "0xa7e7cb9185Ff4A17f54fEDeD3eeb8d09935a879d",  # EVM2EVMOffRamp bnb
                    "0xa3Ea5eB15711041fd28950438b5a682392b54e6C",  # EVM2EVMOffRamp scroll
                ],
                "topics": [
                    "0xd4f851956a5d67c3997d1c9205045fef79bae2947fdee7e9e2641abc7391ef65",  # ExecutionStateChanged
                ],
            },
        ],
        "scroll": [
            {
                "abi": "evm2evmonramp",
                "contracts": [
                    "0x28cCF73F7982c1786b84e243FFbD47F4fB8ae43d",  # EVM2EVMOnRamp ethereum
                    "0x05d472b114D57E6035089A58Fa997A7940D29a23",  # EVM2EVMOnRamp linea
                ],
                "topics": [
                    "0xd0c3c799bf9e2639de44391e7f524d229b2b55f5b1ea94b2bf7da42f7243dddd",  # CCIPSendRequested
                ],
            },
            {
                "abi": "evm2evmofframp",
                "contracts": [
                    "0x77601F272dd2d6481Ac3a13942075388097245Fb",  # EVM2EVMOffRamp ethereum
                    "0x5834e1C639418A4973391126576f550A6996836a",  # EVM2EVMOffRamp linea
                ],
                "topics": [
                    "0xd4f851956a5d67c3997d1c9205045fef79bae2947fdee7e9e2641abc7391ef65",  # ExecutionStateChanged
                ],
            },
        ],
    }
}
