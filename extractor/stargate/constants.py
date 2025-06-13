# Mapping of bridges to their supported blockchains and contracts
BRIDGE_CONFIG = {
    "blockchains": {
        "ethereum": [
            # based on https://stargateprotocol.gitbook.io/stargate/v2-developer-docs/technical-reference/mainnet-contracts
            {
                "abi": "0x6d6620efa72948c5f68a3c8646d58c00d3f4a980",
                "contracts": [
                    "0x6d6620efa72948c5f68a3c8646d58c00d3f4a980",  # Stargate: Token Messaging
                ],
                "topics": [
                    "0x15955c5a4cc61b8fbb05301bce47fd31c0e6f935e1ab97fdac9b134c887bb074",  # BusRode
                    "0x1623f9ea59bd6f214c9571a892da012fc23534aa5906bef4ae8c5d15ee7d2d6e",  # BusDriven
                ],
            },
            {
                "abi": "0x1a44076050125825900e736c501f859c50fe728c",
                "contracts": [
                    "0x1a44076050125825900e736c501f859c50fe728c",  # EndpointV2
                ],
                "topics": [
                    "0x1ab700d4ced0c005b164c0f789fd09fcbb0156d4c2041b8a3bfbcd961cd1567f",  # PacketSent
                    "0x3cd5e48f9730b129dc7550f0fcea9c767b7be37837cd10e55eb35f734f4bca04",  # PacketDelivered
                    "0x0d87345f3d1c929caba93e1c3821b54ff3512e12b66aa3cfe54b6bcbc17e59b4",  # PacketVerified
                    "0x3d52ff888d033fd3dd1d8057da59e850c91d91a72c41dfa445b247dfedeb6dc1",  # ComposeSent
                    "0x0036c98efcf9e6641dfbc9051f66f405253e8e0c2ab4a24dccda15595b7378c8",  # ComposeDelivered
                ],
            },
            {
                "abi": "0x4d73adb72bc3dd368966edd0f0b2148401a178e2",
                "contracts": [
                    "0x4d73adb72bc3dd368966edd0f0b2148401a178e2",  # Layer Zero: Ultra Light Node v2
                ],
                "topics": [
                    "0xe9bded5f24a4168e4f3bf44e00298c993b22376aad8c58c7dda9718a54cbea82",  # Packet
                    "0x2bd2d8a84b748439fd50d79a49502b4eb5faa25b864da6a9ab5c150704be9a4d",  # PacketReceived
                ],
            },
            {
                "abi": "0xbb2ea70c9e858123480642cf96acbcce1372dce1",
                "contracts": [
                    "0xbb2ea70c9e858123480642cf96acbcce1372dce1",  # SendUln302
                ],
                "topics": [
                    "0x61ed099e74a97a1d7f8bb0952a88ca8b7b8ebd00c126ea04671f92a81213318a",  # ExecutorFeePaid
                    "0x07ea52d82345d6e838192107d8fd7123d9c2ec8e916cd0aad13fd2b60db24644",  # DVNFeePaid
                ],
            },
            {
                "abi": "0xc02ab410f0734efa3f14628780e6e695156024c2",
                "contracts": [
                    "0xc02ab410f0734efa3f14628780e6e695156024c2",  # ReceiveUln302
                ],
                "topics": [
                    "0x82118522aa536ac0e96cc5c689407ae42b89d592aa133890a01f1509842f5081",  # UlnConfigSet
                    "0x2cb0eed7538baeae4c6fde038c0fd0384d27de0dd55a228c65847bda6aa1ab56",  # PayloadVerified
                ],
            },
            {
                "abi": "0xd56e4eab23cb81f43168f9f45211eb027b9ac7cc",
                "contracts": [
                    "0xd56e4eab23cb81f43168f9f45211eb027b9ac7cc",  # VerifierNetwork
                ],
                "topics": [
                    "0x87e46b0a6199bc734632187269a103c05714ee0adae5b28f30723955724f37ef",  # VerifierFeePaid
                ],
            },
            {
                "abi": "relayerv2",
                "contracts": [
                    "0x902f09715b6303d4173037652fa7377e5b98089e",  # Layer Zero: Relayer V2
                ],
                "topics": [
                    "0xdf21c415b78ed2552cc9971249e32a053abce6087a0ae0fbf3f78db5174a3493",  # AssignJob
                ],
            },
            {
                "abi": "0xaf5191b0de278c7286d6c7cc6ab6bb8a73ba2cd6",
                "contracts": [
                    "0xaf5191b0de278c7286d6c7cc6ab6bb8a73ba2cd6",  # Stargate Token
                ],
                "topics": [
                    "0x664e26797cde1146ddfcb9a5d3f4de61179f9c11b2698599bb09e686f442172b",  # SendToChain       SendToChain (uint16 dstChainId, bytes to, uint256 qty)
                    "0x1e43690f7c7ebcc548b8e72d1ec2273acd54666f0330bef2eeb2268ee9f28988",  # ReceiveFromChain  ReceiveFromChain(uint16 srcChainId, uint64 nonce, uint256 qty)
                ],
            },
            {
                "abi": "baseoftv2",
                "contracts": [
                    "0x7122985656e38bdc0302db86685bb972b145bd3c",
                    "0x0b7f0e51cd1739d6c96982d55ad8fa634dd43a9c",
                    "0x39b1f7c5b1ae6a3cb9bbbd616b44ced9f53882e0",
                    "0x7bb83ccb91aaee77f8e9bdcdd311e83aff6ff1f9",
                    "0x58ff71c056942600bc4acf8bdf48f82e6ad1f392",
                    "0x152649ea73beab28c5b49b26eb48f7ead6d4c898",
                    "0x28a92dde19d9989f39a49905d7c9c2fac7799bdf",
                    "0x39d5313c3750140e5042887413ba8aa6145a9bd2",
                    "0x25d887ce7a35172c62febfd67a1856f20faebb00",
                    "0x580e933d90091b9ce380740e3a4a39c67eb85b4c",
                    "0x8d279274789ccec8af94a430a5996eaace9609a9",
                    "0x193f4a4a6ea24102f49b931deeeb931f6e32405d",
                    "0xdc402b5bb2725f8761c600aad79f06085fa5fbc4",
                    "0x98d4c2300b2916d56fb26308ee6870460c86859b",
                    "0x227dcc37d9a071d1a2adb7edc40b7ec38a2097b3",
                    "0x8aed0055d691e6d619acc96ad0fb3461f5774646",
                    "0xf8173a39c56a554837c4c7f104153a005d284d11",
                    "0x560363bda52bc6a44ca6c8c9b4a5fadbda32fa60",
                    "0x888e317606b4c590bbad88653863e8b345702633",
                    "0x439a5f0f5e8d149dda9a0ca367d4a8e4d6f83c10",
                    "0xc31813c38b32c0f826c2dbf3360d5899740c9669",
                    "0xf2a3300eb0574951e893ebff15089edb38fcfa3e",
                    "0x2297aebd383787a160dd0d9f71508148769342e3",
                    "0xb401f0cff9f05d10699c0e2c88a81dd923c1ffff",
                    "0x137ddb47ee24eaa998a535ab00378d6bfa84f893",
                    "0xe6828d65bf5023ae1851d90d8783cc821ba7eee1",
                    "0x6ae382814e24b6ddf588901c597f26a9e945c577",
                    "0x8cfa44e930b7743123738eb2d7e78beaa964732e",
                ],
                "topics": [
                    "0xd81fc9b8523134ed613870ed029d6170cbb73aa6a6bc311b9a642689fb9df59a",  # SendToChain       SendToChain (index_topic_1 uint16 _dstChainId, index_topic_2 address _from, index_topic_3 bytes32 _toAddress, uint256 _amount)
                    "0xbf551ec93859b170f9b2141bd9298bf3f64322c6f7beb2543a0cb669834118bf",  # ReceiveFromChain  ReceiveFromChain (index_topic_1 uint16 _srcChainId, index_topic_2 address _to, uint256 _amount)
                ],
            },
            {
                "abi": "lptokenerc20",
                "contracts": [
                    "0x38ea452219524bb87e18de1c24d3bb59510bd783",  # Stargate Finance: S*USDT Token (LPTokenERC20)
                    "0xdf0770df86a8034b3efef0a1bb3c889b8332ff56",  # Stargate Finance: S*USDC Token (LPTokenERC20)
                    "0x0Faf1d2d3CED330824de3B8200fc8dc6E397850d",  # Stargate Finance: S*DAI Token (LPTokenERC20)
                    "0xfA0F307783AC21C39E939ACFF795e27b650F6e68",  # Stargate Finance: S*FRAX Token (LPTokenERC20)
                    "0x692953e758c3669290cb1677180c64183cEe374e",  # Stargate Finance: S*USDD Token (LPTokenERC20)
                    "0x101816545f6bd2b1076434b54383a1e633390a2e",  # Stargate Finance: S*SGETH Token (LPTokenERC20)
                ],
                "topics": [
                    "0x34660fc8af304464529f48a778e03d03e4d34bcd5f9b6f0cfbf3cd238c642f7f",  # Swap
                    "0xfb2b592367452f1c437675bed47f5e1e6c25188c17d7ba01a12eb030bc41ccef",  # SwapRemote
                ],
            },
            {
                "abi": "oft",
                "contracts": [
                    "0x77b2043768d28e9c9ab44e1abfc95944bce57931",  # Stargate Pool Native
                    "0xc026395860db2d07ee33e05fe50ed7bd583189c7",  # Stargate Pool USDC
                    "0x933597a323eb81cae705c5bc29985172fd5a3973",  # Stargate Pool USDT
                    "0x6985884c4392d348587b19cb9eaaf157f13271cd",  # Layer Zero Token OFT
                ],
                "topics": [
                    "0x85496b760a4b7f8d66384b9df21b381f5d1b1e79f229a47aaf4c232edc2fe59a",  # OFTSent
                    "0xefed6d3500546b29533b128a29e3a94d70788727f0507505ac12eaf2e578fd9c",  # OFTReceived
                ],
            },
        ],
        "arbitrum": [
            {
                "abi": "0x19cfce47ed54a88614648dc3f19a5980097007dd",
                "contracts": [
                    "0x19cfce47ed54a88614648dc3f19a5980097007dd",  # Stargate: Token Messaging
                ],
                "topics": [
                    "0x15955c5a4cc61b8fbb05301bce47fd31c0e6f935e1ab97fdac9b134c887bb074",  # BusRode
                    "0x1623f9ea59bd6f214c9571a892da012fc23534aa5906bef4ae8c5d15ee7d2d6e",  # BusDriven
                ],
            },
            {
                "abi": "0x1a44076050125825900e736c501f859c50fe728c",
                "contracts": [
                    "0x1a44076050125825900e736c501f859c50fe728c",  # EndpointV2
                ],
                "topics": [
                    "0x1ab700d4ced0c005b164c0f789fd09fcbb0156d4c2041b8a3bfbcd961cd1567f",  # PacketSent
                    "0x3cd5e48f9730b129dc7550f0fcea9c767b7be37837cd10e55eb35f734f4bca04",  # PacketDelivered
                    "0x0d87345f3d1c929caba93e1c3821b54ff3512e12b66aa3cfe54b6bcbc17e59b4",  # PacketVerified
                    "0x3d52ff888d033fd3dd1d8057da59e850c91d91a72c41dfa445b247dfedeb6dc1",  # ComposeSent
                    "0x0036c98efcf9e6641dfbc9051f66f405253e8e0c2ab4a24dccda15595b7378c8",  # ComposeDelivered
                ],
            },
            {
                "abi": "0x4d73adb72bc3dd368966edd0f0b2148401a178e2",
                "contracts": [
                    "0x4d73adb72bc3dd368966edd0f0b2148401a178e2",  # Layer Zero: Ultra Light Node v2
                ],
                "topics": [
                    "0xe9bded5f24a4168e4f3bf44e00298c993b22376aad8c58c7dda9718a54cbea82",  # Packet
                    "0x2bd2d8a84b748439fd50d79a49502b4eb5faa25b864da6a9ab5c150704be9a4d",  # PacketReceived
                ],
            },
            {
                "abi": "0x975bcd720be66659e3eb3c0e4f1866a3020e493a",
                "contracts": [
                    "0x975bcd720be66659e3eb3c0e4f1866a3020e493a",  # SendUln302
                ],
                "topics": [
                    "0x61ed099e74a97a1d7f8bb0952a88ca8b7b8ebd00c126ea04671f92a81213318a",  # ExecutorFeePaid
                    "0x07ea52d82345d6e838192107d8fd7123d9c2ec8e916cd0aad13fd2b60db24644",  # DVNFeePaid
                ],
            },
            {
                "abi": "0x7b9e184e07a6ee1ac23eae0fe8d6be2f663f05e6",
                "contracts": [
                    "0x7b9e184e07a6ee1ac23eae0fe8d6be2f663f05e6",  # ReceiveUln302
                ],
                "topics": [
                    "0x82118522aa536ac0e96cc5c689407ae42b89d592aa133890a01f1509842f5081",  # UlnConfigSet
                    "0x2cb0eed7538baeae4c6fde038c0fd0384d27de0dd55a228c65847bda6aa1ab56",  # PayloadVerified
                ],
            },
            {
                "abi": "0xd56e4eab23cb81f43168f9f45211eb027b9ac7cc",
                "contracts": [
                    "0xd56e4eab23cb81f43168f9f45211eb027b9ac7cc",  # VerifierNetwork
                ],
                "topics": [
                    "0x87e46b0a6199bc734632187269a103c05714ee0adae5b28f30723955724f37ef",  # VerifierFeePaid
                ],
            },
            {
                "abi": "relayerv2",
                "contracts": [
                    "0x177d36dbe2271a4ddb2ad8304d82628eb921d790",  # Layer Zero: Relayer V2
                ],
                "topics": [
                    "0xdf21c415b78ed2552cc9971249e32a053abce6087a0ae0fbf3f78db5174a3493",  # AssignJob
                ],
            },
            {
                "abi": "0x6694340fc020c5e6b96567843da2df01b2ce1eb6",
                "contracts": [
                    "0x6694340fc020c5e6b96567843da2df01b2ce1eb6",  # Stargate Token
                ],
                "topics": [
                    "0x664e26797cde1146ddfcb9a5d3f4de61179f9c11b2698599bb09e686f442172b",  # SendToChain
                    "0x831bc68226f8d1f734ffcca73602efc4eca13711402ba1d2cc05ee17bb54f631",  # ReceiveFromChain
                ],
            },
            {
                "abi": "baseoftv2",
                "contracts": [
                    "0x1572d48a52906b834fb236aa77831d669f6d87a1",
                    "0x6db8b088c4d41d622b44cd81b900ba690f2d496c",
                    "0x1b896893dfc86bb67cf57767298b9073d2c1ba2c",
                    "0x1509706a6c66ca549ff0cb464de88231ddbe213b",
                    "0x3082cc23568ea640225c2467653db90e9250aaa0",
                    "0x2297aebd383787a160dd0d9f71508148769342e3",
                    "0x3de81ce90f5a27c5e6a5adb04b54aba488a6d14e",
                    "0xbfd5206962267c7b4b4a8b3d76ac2e1b2a5c4d5e",
                    "0x9e20461bc2c4c980f62f1b279d71734207a6a356",
                    "0x2b1d36f5b61addaf7da7ebbd11b35fd8cfb0de31",
                    "0x20cea49b5f7a6dbd78cae772ca5973ef360aa1e6",
                    "0x371c7ec6d8039ff7933a2aa28eb827ffe1f52f07",
                    "0x04ac146cebd110adf4350df7ad029794a7528bd0",
                    "0x2ac2b254bc18cd4999f64773a966e4f4869c34ee",
                    "0xe71bdfe1df69284f00ee185cf0d95d0c7680c0d4",
                    "0x957a8af7894e76e16db17c2a913496a4e60b7090",
                    "0x66e535e8d2ebf13f49f3d49e5c50395a97c137b1",
                    "0x25d887ce7a35172c62febfd67a1856f20faebb00",
                    "0x560363bda52bc6a44ca6c8c9b4a5fadbda32fa60",
                    "0xbdfdb3665c7d8374d86d54203e31f5c46c9f1712",
                    "0x188fb5f5ae5bbe4154d5778f2bbb2fb985c94d25",
                    "0xddbfbd5dc3ba0feb96cb513b689966b2176d4c09",
                    "0x7f4db37d7beb31f445307782bc3da0f18df13696",
                    "0xb688ba096b7bb75d7841e47163cd12d18b36a5bf",
                    "0xba0dda8762c24da9487f5fa026a9b64b695a07ea",
                    "0xa9004a5421372e1d83fb1f85b0fc986c912f91f3",
                    "0x7be5dd337cc6ce3e474f64e2a92a566445290864",
                    "0x3b58a4c865b568a2f6a957c264f6b50cba35d8ce",
                    "0x7448c7456a97769f6cd04f1e83a4a23ccdc46abd",
                    "0x9f018bda8f6b507a0c9e6f290b2f7c49c2f8daf8",
                ],
                "topics": [
                    "0xd81fc9b8523134ed613870ed029d6170cbb73aa6a6bc311b9a642689fb9df59a",  # SendToChain
                    "0xbf551ec93859b170f9b2141bd9298bf3f64322c6f7beb2543a0cb669834118bf",  # ReceiveFromChain
                ],
            },
            {
                "abi": "oft",
                "contracts": [
                    "0xa45b5130f36cdca45667738e2a258ab09f4a5f7f",  # Stargate Pool Native
                    "0xe8CDF27AcD73a434D661C84887215F7598e7d0d3",  # Stargate Pool USDC
                    "0xce8cca271ebc0533920c83d39f417ed6a0abb7d0",  # Stargate Pool USDT
                    "0x6985884c4392d348587b19cb9eaaf157f13271cd",  # Layer Zero Token OFT
                ],
                "topics": [
                    "0x85496b760a4b7f8d66384b9df21b381f5d1b1e79f229a47aaf4c232edc2fe59a",  # OFTSent
                    "0xefed6d3500546b29533b128a29e3a94d70788727f0507505ac12eaf2e578fd9c",  # OFTReceived
                ],
            },
            {
                "abi": "lptokenerc20",
                "contracts": [
                    "0xB6CfcF89a7B22988bfC96632aC2A9D6daB60d641",  # Stargate Finance: S*USDT Token (LPTokenERC20)
                    "0x892785f33cdee22a30aef750f285e18c18040c3e",  # Stargate Finance: S*USDC Token (LPTokenERC20)
                    "0x600e576f9d853c95d58029093a16ee49646f3ca5",  # Stargate Finance: S*LUSD Token (LPTokenERC20)
                    "0x915A55e36A01285A14f05dE6e81ED9cE89772f8e",  # Stargate Finance: S*SGETH Token (LPTokenERC20)
                ],
                "topics": [
                    "0x34660fc8af304464529f48a778e03d03e4d34bcd5f9b6f0cfbf3cd238c642f7f",  # Swap
                    "0xfb2b592367452f1c437675bed47f5e1e6c25188c17d7ba01a12eb030bc41ccef",  # SwapRemote
                ],
            },
        ],
        "bnb": [
            {
                "abi": "0x6e3d884c96d640526f273c61dfcf08915ebd7e2b",
                "contracts": [
                    "0x6e3d884c96d640526f273c61dfcf08915ebd7e2b",  # Stargate: Token Messaging
                ],
                "topics": [
                    "0x15955c5a4cc61b8fbb05301bce47fd31c0e6f935e1ab97fdac9b134c887bb074",  # BusRode
                    "0x1623f9ea59bd6f214c9571a892da012fc23534aa5906bef4ae8c5d15ee7d2d6e",  # BusDriven
                ],
            },
            {
                "abi": "0x1a44076050125825900e736c501f859c50fe728c",
                "contracts": [
                    "0x1a44076050125825900e736c501f859c50fe728c",  # EndpointV2
                ],
                "topics": [
                    "0x1ab700d4ced0c005b164c0f789fd09fcbb0156d4c2041b8a3bfbcd961cd1567f",  # PacketSent
                    "0x3cd5e48f9730b129dc7550f0fcea9c767b7be37837cd10e55eb35f734f4bca04",  # PacketDelivered
                    "0x0d87345f3d1c929caba93e1c3821b54ff3512e12b66aa3cfe54b6bcbc17e59b4",  # PacketVerified
                    "0x3d52ff888d033fd3dd1d8057da59e850c91d91a72c41dfa445b247dfedeb6dc1",  # ComposeSent
                    "0x0036c98efcf9e6641dfbc9051f66f405253e8e0c2ab4a24dccda15595b7378c8",  # ComposeDelivered
                ],
            },
            {
                "abi": "0x4d73adb72bc3dd368966edd0f0b2148401a178e2",
                "contracts": [
                    "0x4d73adb72bc3dd368966edd0f0b2148401a178e2",  # Layer Zero: Ultra Light Node v2
                ],
                "topics": [
                    "0xe9bded5f24a4168e4f3bf44e00298c993b22376aad8c58c7dda9718a54cbea82",  # Packet
                    "0x2bd2d8a84b748439fd50d79a49502b4eb5faa25b864da6a9ab5c150704be9a4d",  # PacketReceived
                ],
            },
            {
                "abi": "0x9f8c645f2d0b2159767bd6e0839de4be49e823de",
                "contracts": [
                    "0x9f8c645f2d0b2159767bd6e0839de4be49e823de",  # SendUln302
                ],
                "topics": [
                    "0x61ed099e74a97a1d7f8bb0952a88ca8b7b8ebd00c126ea04671f92a81213318a",  # ExecutorFeePaid
                    "0x07ea52d82345d6e838192107d8fd7123d9c2ec8e916cd0aad13fd2b60db24644",  # DVNFeePaid
                ],
            },
            {
                "abi": "0xb217266c3a98c8b2709ee26836c98cf12f6ccec1",
                "contracts": [
                    "0xb217266c3a98c8b2709ee26836c98cf12f6ccec1",  # ReceiveUln302
                ],
                "topics": [
                    "0x82118522aa536ac0e96cc5c689407ae42b89d592aa133890a01f1509842f5081",  # UlnConfigSet
                    "0x2cb0eed7538baeae4c6fde038c0fd0384d27de0dd55a228c65847bda6aa1ab56",  # PayloadVerified
                ],
            },
            {
                "abi": "0xd56e4eab23cb81f43168f9f45211eb027b9ac7cc",
                "contracts": [
                    "0xd56e4eab23cb81f43168f9f45211eb027b9ac7cc",  # VerifierNetwork
                ],
                "topics": [
                    "0x87e46b0a6199bc734632187269a103c05714ee0adae5b28f30723955724f37ef",  # VerifierFeePaid
                ],
            },
            {
                "abi": "relayerv2",
                "contracts": [
                    "0xa27a2ca24dd28ce14fb5f5844b59851f03dcf182",  # Layer Zero: Relayer V2
                ],
                "topics": [
                    "0xdf21c415b78ed2552cc9971249e32a053abce6087a0ae0fbf3f78db5174a3493",  # AssignJob
                ],
            },
            {
                "abi": "0xb0d502e938ed5f4df2e681fe6e419ff29631d62b",
                "contracts": [
                    "0xb0d502e938ed5f4df2e681fe6e419ff29631d62b",  # StargateToken
                ],
                "topics": [
                    "0x664e26797cde1146ddfcb9a5d3f4de61179f9c11b2698599bb09e686f442172b",  # SendToChain
                    "0x831bc68226f8d1f734ffcca73602efc4eca13711402ba1d2cc05ee17bb54f631",  # ReceiveFromChain
                ],
            },
            {
                "abi": "baseoftv2",
                "contracts": [
                    "0xb274202daba6ae180c665b4fbe59857b7c3a8091",
                    "0xcf7d4b692c478b77aff32bb1493c54c84f27f85a",
                    "0xf8f46791e3db29a029ec6c9d946226f3c613e854",
                    "0x2297aebd383787a160dd0d9f71508148769342e3",
                    "0x982e609643794a31a07f5c5b142dd3a9cf0690be",
                    "0x11cd72f7a4b699c67f225ca8abb20bc9f8db90c7",
                    "0x560363bda52bc6a44ca6c8c9b4a5fadbda32fa60",
                    "0x336f374198c872ba760e85af9c6331c3c5a535d3",
                    "0x193f4a4a6ea24102f49b931deeeb931f6e32405d",
                    "0x25d887ce7a35172c62febfd67a1856f20faebb00",
                    "0x5012c90f14d190607662ca8344120812aaa2639d",
                    "0x371c7ec6d8039ff7933a2aa28eb827ffe1f52f07",
                    "0xf7de7e8a6bd59ed41a4b5fe50278b3b7f31384df",
                    "0x9e20461bc2c4c980f62f1b279d71734207a6a356",
                    "0x80137510979822322193fc997d400d5a6c747bf7",
                    "0xe62b7c22484f8b031930275d31f42b9a517fe038",
                    "0x8d279274789ccec8af94a430a5996eaace9609a9",
                    "0xa9004a5421372e1d83fb1f85b0fc986c912f91f3",
                    "0xcecb301c2e2a04dd631428c386dd21db70716f8a",
                    "0xe6828d65bf5023ae1851d90d8783cc821ba7eee1",
                    "0x0e446faad63e344167489b5cf1111f4cc305cbd3",
                    "0x67fb304001ad03c282266b965b51e97aa54a2fab",
                    "0x25ea98ac87a38142561ea70143fd44c4772a16b6",
                    "0xb7e2713cf55cf4b469b5a8421ae6fc0ed18f1467",
                    "0x0465aad9da170798433f4ab7fa7ec8b9b9bf0bb1",
                ],
                "topics": [
                    "0xd81fc9b8523134ed613870ed029d6170cbb73aa6a6bc311b9a642689fb9df59a",  # SendToChain
                    "0xbf551ec93859b170f9b2141bd9298bf3f64322c6f7beb2543a0cb669834118bf",  # ReceiveFromChain
                ],
            },
            {
                "abi": "oft",
                "contracts": [
                    "0x962Bd449E630b0d928f308Ce63f1A21F02576057",  # Stargate Pool USDC
                    "0x138EB30f73BC423c6455C53df6D89CB01d9eBc63",  # Stargate Pool USDT
                    "0x6985884c4392d348587b19cb9eaaf157f13271cd",  # Layer Zero Token OFT
                ],
                "topics": [
                    "0x85496b760a4b7f8d66384b9df21b381f5d1b1e79f229a47aaf4c232edc2fe59a",  # OFTSent
                    "0xefed6d3500546b29533b128a29e3a94d70788727f0507505ac12eaf2e578fd9c",  # OFTReceived
                ],
            },
            {
                "abi": "lptokenerc20",
                "contracts": [
                    "0x9aA83081AA06AF7208Dcc7A4cB72C94d057D2cda",  # Stargate Finance: S*USDT Token (LPTokenERC20)
                    "0x98a5737749490856b401DB5Dc27F522fC314A4e1",  # Stargate Finance: S*BUSD Token
                    "0x4e145a589e4c03cBe3d28520e4BF3089834289Df",  # Stargate Finance: S*USDD Token
                ],
                "topics": [
                    "0x34660fc8af304464529f48a778e03d03e4d34bcd5f9b6f0cfbf3cd238c642f7f",  # Swap
                    "0xfb2b592367452f1c437675bed47f5e1e6c25188c17d7ba01a12eb030bc41ccef",  # SwapRemote
                ],
            },
        ],
        "polygon": [
            {
                "abi": "0x6ce9bf8cdab780416ad1fd87b318a077d2f50eac",
                "contracts": [
                    "0x6ce9bf8cdab780416ad1fd87b318a077d2f50eac",  # Stargate: Token Messaging
                ],
                "topics": [
                    "0x15955c5a4cc61b8fbb05301bce47fd31c0e6f935e1ab97fdac9b134c887bb074",  # BusRode
                    "0x1623f9ea59bd6f214c9571a892da012fc23534aa5906bef4ae8c5d15ee7d2d6e",  # BusDriven
                ],
            },
            {
                "abi": "0x1a44076050125825900e736c501f859c50fe728c",
                "contracts": [
                    "0x1a44076050125825900e736c501f859c50fe728c",  # EndpointV2
                ],
                "topics": [
                    "0x1ab700d4ced0c005b164c0f789fd09fcbb0156d4c2041b8a3bfbcd961cd1567f",  # PacketSent
                    "0x3cd5e48f9730b129dc7550f0fcea9c767b7be37837cd10e55eb35f734f4bca04",  # PacketDelivered
                    "0x0d87345f3d1c929caba93e1c3821b54ff3512e12b66aa3cfe54b6bcbc17e59b4",  # PacketVerified
                    "0x3d52ff888d033fd3dd1d8057da59e850c91d91a72c41dfa445b247dfedeb6dc1",  # ComposeSent
                    "0x0036c98efcf9e6641dfbc9051f66f405253e8e0c2ab4a24dccda15595b7378c8",  # ComposeDelivered
                ],
            },
            {
                "abi": "0x4d73adb72bc3dd368966edd0f0b2148401a178e2",
                "contracts": [
                    "0x4d73adb72bc3dd368966edd0f0b2148401a178e2",  # Layer Zero: Ultra Light Node v2
                ],
                "topics": [
                    "0xe9bded5f24a4168e4f3bf44e00298c993b22376aad8c58c7dda9718a54cbea82",  # Packet
                    "0x2bd2d8a84b748439fd50d79a49502b4eb5faa25b864da6a9ab5c150704be9a4d",  # PacketReceived
                ],
            },
            {
                "abi": "0x6c26c61a97006888ea9e4fa36584c7df57cd9da3",
                "contracts": [
                    "0x6c26c61a97006888ea9e4fa36584c7df57cd9da3",  # SendUln302
                ],
                "topics": [
                    "0x61ed099e74a97a1d7f8bb0952a88ca8b7b8ebd00c126ea04671f92a81213318a",  # ExecutorFeePaid
                    "0x07ea52d82345d6e838192107d8fd7123d9c2ec8e916cd0aad13fd2b60db24644",  # DVNFeePaid
                ],
            },
            {
                "abi": "0x1322871e4ab09bc7f5717189434f97bbd9546e95",
                "contracts": [
                    "0x1322871e4ab09bc7f5717189434f97bbd9546e95",  # ReceiveUln302
                ],
                "topics": [
                    "0x82118522aa536ac0e96cc5c689407ae42b89d592aa133890a01f1509842f5081",  # UlnConfigSet
                    "0x2cb0eed7538baeae4c6fde038c0fd0384d27de0dd55a228c65847bda6aa1ab56",  # PayloadVerified
                ],
            },
            {
                "abi": "0xd56e4eab23cb81f43168f9f45211eb027b9ac7cc",
                "contracts": [
                    "0xd56e4eab23cb81f43168f9f45211eb027b9ac7cc",  # VerifierNetwork
                ],
                "topics": [
                    "0x87e46b0a6199bc734632187269a103c05714ee0adae5b28f30723955724f37ef",  # VerifierFeePaid
                ],
            },
            {
                "abi": "relayerv2",
                "contracts": [
                    "0x75dc8e5f50c8221a82ca6af64af811caa983b65f",  # Layer Zero: Relayer V2
                ],
                "topics": [
                    "0xdf21c415b78ed2552cc9971249e32a053abce6087a0ae0fbf3f78db5174a3493",  # AssignJob
                ],
            },
            {
                "abi": "0x2f6f07cdcf3588944bf4c42ac74ff24bf56e7590",
                "contracts": [
                    "0x2f6f07cdcf3588944bf4c42ac74ff24bf56e7590",  # STG Token
                ],
                "topics": [
                    "0x664e26797cde1146ddfcb9a5d3f4de61179f9c11b2698599bb09e686f442172b",  # SendToChain
                    "0x831bc68226f8d1f734ffcca73602efc4eca13711402ba1d2cc05ee17bb54f631",  # ReceiveFromChain
                ],
            },
            {
                "abi": "baseoftv2",
                "contracts": [
                    "0xfe0855903e32953de8e63ff6585f3fb5a2b4deff",
                    "0x2297aebd383787a160dd0d9f71508148769342e3",
                    "0x110b25d2b21ee73eb401f3ae7833f7072912a0bf",
                    "0x9e20461bc2c4c980f62f1b279d71734207a6a356",
                    "0x00e8c0e92eb3ad88189e7125ec8825edc03ab265",
                    "0x11cd72f7a4b699c67f225ca8abb20bc9f8db90c7",
                    "0xe6828d65bf5023ae1851d90d8783cc821ba7eee1",
                    "0x1509706a6c66ca549ff0cb464de88231ddbe213b",
                    "0xc19669a405067927865b40ea045a2baabbbe57f5",
                    "0xdef87c507ef911fd99c118c53171510eb7967738",
                ],
                "topics": [
                    "0xd81fc9b8523134ed613870ed029d6170cbb73aa6a6bc311b9a642689fb9df59a",  # SendToChain
                    "0xbf551ec93859b170f9b2141bd9298bf3f64322c6f7beb2543a0cb669834118bf",  # ReceiveFromChain
                ],
            },
            {
                "abi": "oft",
                "contracts": [
                    "0x9aa02d4fae7f58b8e8f34c66e756cc734dac7fe4",  # Stargate Pool USDC
                    "0xd47b03ee6d86Cf251ee7860FB2ACf9f91B9fD4d7",  # Stargate Pool USDT
                    "0x6985884c4392d348587b19cb9eaaf157f13271cd",  # Layer Zero Token OFT
                ],
                "topics": [
                    "0x85496b760a4b7f8d66384b9df21b381f5d1b1e79f229a47aaf4c232edc2fe59a",  # OFTSent
                    "0xefed6d3500546b29533b128a29e3a94d70788727f0507505ac12eaf2e578fd9c",  # OFTReceived
                ],
            },
            {
                "abi": "lptokenerc20",
                "contracts": [
                    "0x29e38769f23701a2e4a8ef0492e19da4604be62c",  # Stargate Finance: S*USDT Token (LPTokenERC20)
                    "0x1205f31718499dbf1fca446663b532ef87481fe1",  # Stargate Finance: S*USDC Token (LPTokenERC20)
                    "0x1c272232df0bb6225da87f4decd9d37c32f63eea",  # Stargate Finance: S*DAI Token (LPTokenERC20)
                ],
                "topics": [
                    "0x34660fc8af304464529f48a778e03d03e4d34bcd5f9b6f0cfbf3cd238c642f7f",  # Swap
                    "0xfb2b592367452f1c437675bed47f5e1e6c25188c17d7ba01a12eb030bc41ccef",  # SwapRemote
                ],
            },
        ],
        "optimism": [
            {
                "abi": "0xf1fcb4cbd57b67d683972a59b6a7b1e2e8bf27e6",
                "contracts": [
                    "0xf1fcb4cbd57b67d683972a59b6a7b1e2e8bf27e6",  # Stargate: Token Messaging
                ],
                "topics": [
                    "0x15955c5a4cc61b8fbb05301bce47fd31c0e6f935e1ab97fdac9b134c887bb074",  # BusRode
                    "0x1623f9ea59bd6f214c9571a892da012fc23534aa5906bef4ae8c5d15ee7d2d6e",  # BusDriven
                ],
            },
            {
                "abi": "0x1a44076050125825900e736c501f859c50fe728c",
                "contracts": [
                    "0x1a44076050125825900e736c501f859c50fe728c",  # EndpointV2
                ],
                "topics": [
                    "0x1ab700d4ced0c005b164c0f789fd09fcbb0156d4c2041b8a3bfbcd961cd1567f",  # PacketSent
                    "0x3cd5e48f9730b129dc7550f0fcea9c767b7be37837cd10e55eb35f734f4bca04",  # PacketDelivered
                    "0x0d87345f3d1c929caba93e1c3821b54ff3512e12b66aa3cfe54b6bcbc17e59b4",  # PacketVerified
                    "0x3d52ff888d033fd3dd1d8057da59e850c91d91a72c41dfa445b247dfedeb6dc1",  # ComposeSent
                    "0x0036c98efcf9e6641dfbc9051f66f405253e8e0c2ab4a24dccda15595b7378c8",  # ComposeDelivered
                ],
            },
            {
                "abi": "0x4d73adb72bc3dd368966edd0f0b2148401a178e2",
                "contracts": [
                    "0x4d73adb72bc3dd368966edd0f0b2148401a178e2",  # Layer Zero: Ultra Light Node v2
                ],
                "topics": [
                    "0xe9bded5f24a4168e4f3bf44e00298c993b22376aad8c58c7dda9718a54cbea82",  # Packet
                    "0x2bd2d8a84b748439fd50d79a49502b4eb5faa25b864da6a9ab5c150704be9a4d",  # PacketReceived
                ],
            },
            {
                "abi": "0x1322871e4ab09bc7f5717189434f97bbd9546e95",
                "contracts": [
                    "0x1322871e4ab09bc7f5717189434f97bbd9546e95",  # SendUln302
                ],
                "topics": [
                    "0x61ed099e74a97a1d7f8bb0952a88ca8b7b8ebd00c126ea04671f92a81213318a",  # ExecutorFeePaid
                    "0x07ea52d82345d6e838192107d8fd7123d9c2ec8e916cd0aad13fd2b60db24644",  # DVNFeePaid
                ],
            },
            {
                "abi": "0x3c4962ff6258dcfcafd23a814237b7d6eb712063",
                "contracts": [
                    "0x3c4962ff6258dcfcafd23a814237b7d6eb712063",  # ReceiveUln302
                ],
                "topics": [
                    "0x82118522aa536ac0e96cc5c689407ae42b89d592aa133890a01f1509842f5081",  # UlnConfigSet
                    "0x2cb0eed7538baeae4c6fde038c0fd0384d27de0dd55a228c65847bda6aa1ab56",  # PayloadVerified
                ],
            },
            {
                "abi": "0xd56e4eab23cb81f43168f9f45211eb027b9ac7cc",
                "contracts": [
                    "0xd56e4eab23cb81f43168f9f45211eb027b9ac7cc",  # VerifierNetwork
                ],
                "topics": [
                    "0x87e46b0a6199bc734632187269a103c05714ee0adae5b28f30723955724f37ef",  # VerifierFeePaid
                ],
            },
            {
                "abi": "relayerv2",
                "contracts": [
                    "0x81e792e5a9003cc1c8bf5569a00f34b65d75b017",  # Layer Zero: Relayer V2
                ],
                "topics": [
                    "0xdf21c415b78ed2552cc9971249e32a053abce6087a0ae0fbf3f78db5174a3493",  # AssignJob
                ],
            },
            {
                "abi": "0x296f55f8fb28e498b858d0bcda06d955b2cb3f97",
                "contracts": [
                    "0x296f55f8fb28e498b858d0bcda06d955b2cb3f97",  # STG Token
                ],
                "topics": [
                    "0x664e26797cde1146ddfcb9a5d3f4de61179f9c11b2698599bb09e686f442172b",  # SendToChain
                    "0x831bc68226f8d1f734ffcca73602efc4eca13711402ba1d2cc05ee17bb54f631",  # ReceiveFromChain
                ],
            },
            {
                "abi": "baseoftv2",
                "contracts": [
                    "0xe2510aa4b019af3eb835d3ac9c800382109a4631",
                    "0x0c9d44f5a573f6cfc9e8264a5ca72a1184616ef4",
                    "0x1f514a61bcde34f94bc39731235690ab9da737f7",
                    "0x2297aebd383787a160dd0d9f71508148769342e3",
                    "0x66e535e8d2ebf13f49f3d49e5c50395a97c137b1",
                    "0xbfd5206962267c7b4b4a8b3d76ac2e1b2a5c4d5e",
                    "0xe71bdfe1df69284f00ee185cf0d95d0c7680c0d4",
                ],
                "topics": [
                    "0xd81fc9b8523134ed613870ed029d6170cbb73aa6a6bc311b9a642689fb9df59a",  # SendToChain
                    "0xbf551ec93859b170f9b2141bd9298bf3f64322c6f7beb2543a0cb669834118bf",  # ReceiveFromChain
                ],
            },
            {
                "abi": "oft",
                "contracts": [
                    "0xe8CDF27AcD73a434D661C84887215F7598e7d0d3",  # Stargate Pool Native
                    "0xcE8CcA271Ebc0533920C83d39F417ED6A0abB7D0",  # Stargate Pool USDC
                    "0x19cFCE47eD54a88614648DC3f19A5980097007dD",  # Stargate Pool USDT
                    "0x6985884c4392d348587b19cb9eaaf157f13271cd",  # Layer Zero Token OFT
                ],
                "topics": [
                    "0x85496b760a4b7f8d66384b9df21b381f5d1b1e79f229a47aaf4c232edc2fe59a",  # OFTSent
                    "0xefed6d3500546b29533b128a29e3a94d70788727f0507505ac12eaf2e578fd9c",  # OFTReceived
                ],
            },
            {
                "abi": "lptokenerc20",
                "contracts": [
                    "0x368605d9c6243a80903b9e326f1cddde088b8924",  # Stargate Finance: S*FRAX Token (LPTokenERC20)
                    "0x165137624f1f692e69659f944bf69de02874ee27",  # Stargate Finance: S*DAI Token (LPTokenERC20)
                    "0xDecC0c09c3B5f6e92EF4184125D5648a66E35298",  # Stargate Finance: S*USDC Token (LPTokenERC20)
                    "0xd22363e3762cA7339569F3d33EADe20127D5F98C",  # Stargate Finance: S*GETH Token (LPTokenERC20)
                    "0x3533f5e279bdbf550272a199a223da798d9eff78",  # Stargate Finance: S*LUSD Token
                ],
                "topics": [
                    "0x34660fc8af304464529f48a778e03d03e4d34bcd5f9b6f0cfbf3cd238c642f7f",  # Swap
                    "0xfb2b592367452f1c437675bed47f5e1e6c25188c17d7ba01a12eb030bc41ccef",  # SwapRemote
                ],
            },
        ],
        "avalanche": [
            {
                "abi": "0x17e450be3ba9557f2378e20d64ad417e59ef9a34",
                "contracts": [
                    "0x17e450be3ba9557f2378e20d64ad417e59ef9a34",  # Stargate: Token Messaging
                ],
                "topics": [
                    "0x15955c5a4cc61b8fbb05301bce47fd31c0e6f935e1ab97fdac9b134c887bb074",  # BusRode
                    "0x1623f9ea59bd6f214c9571a892da012fc23534aa5906bef4ae8c5d15ee7d2d6e",  # BusDriven
                ],
            },
            {
                "abi": "0x1a44076050125825900e736c501f859c50fe728c",
                "contracts": [
                    "0x1a44076050125825900e736c501f859c50fe728c",  # EndpointV2
                ],
                "topics": [
                    "0x1ab700d4ced0c005b164c0f789fd09fcbb0156d4c2041b8a3bfbcd961cd1567f",  # PacketSent
                    "0x3cd5e48f9730b129dc7550f0fcea9c767b7be37837cd10e55eb35f734f4bca04",  # PacketDelivered
                    "0x0d87345f3d1c929caba93e1c3821b54ff3512e12b66aa3cfe54b6bcbc17e59b4",  # PacketVerified
                    "0x3d52ff888d033fd3dd1d8057da59e850c91d91a72c41dfa445b247dfedeb6dc1",  # ComposeSent
                    "0x0036c98efcf9e6641dfbc9051f66f405253e8e0c2ab4a24dccda15595b7378c8",  # ComposeDelivered
                ],
            },
            {
                "abi": "0x4d73adb72bc3dd368966edd0f0b2148401a178e2",
                "contracts": [
                    "0x4d73adb72bc3dd368966edd0f0b2148401a178e2",  # Layer Zero: Ultra Light Node v2
                ],
                "topics": [
                    "0xe9bded5f24a4168e4f3bf44e00298c993b22376aad8c58c7dda9718a54cbea82",  # Packet
                    "0x2bd2d8a84b748439fd50d79a49502b4eb5faa25b864da6a9ab5c150704be9a4d",  # PacketReceived
                ],
            },
            {
                "abi": "0x197d1333dea5fe0d6600e9b396c7f1b1cfcc558a",
                "contracts": [
                    "0x197d1333dea5fe0d6600e9b396c7f1b1cfcc558a",  # SendUln302
                ],
                "topics": [
                    "0x61ed099e74a97a1d7f8bb0952a88ca8b7b8ebd00c126ea04671f92a81213318a",  # ExecutorFeePaid
                    "0x07ea52d82345d6e838192107d8fd7123d9c2ec8e916cd0aad13fd2b60db24644",  # DVNFeePaid
                ],
            },
            {
                "abi": "0xbf3521d309642FA9B1c91A08609505BA09752c61",
                "contracts": [
                    "0xbf3521d309642FA9B1c91A08609505BA09752c61",  # ReceiveUln302
                ],
                "topics": [
                    "0x82118522aa536ac0e96cc5c689407ae42b89d592aa133890a01f1509842f5081",  # UlnConfigSet
                    "0x2cb0eed7538baeae4c6fde038c0fd0384d27de0dd55a228c65847bda6aa1ab56",  # PayloadVerified
                ],
            },
            {
                "abi": "0xd56e4eab23cb81f43168f9f45211eb027b9ac7cc",
                "contracts": [
                    "0xd56e4eab23cb81f43168f9f45211eb027b9ac7cc",  # VerifierNetwork
                ],
                "topics": [
                    "0x87e46b0a6199bc734632187269a103c05714ee0adae5b28f30723955724f37ef",  # VerifierFeePaid
                ],
            },
            {
                "abi": "relayerv2",
                "contracts": [
                    "0xCD2E3622d483C7Dc855F72e5eafAdCD577ac78B4",  # Layer Zero: Relayer V2
                ],
                "topics": [
                    "0xdf21c415b78ed2552cc9971249e32a053abce6087a0ae0fbf3f78db5174a3493",  # AssignJob
                ],
            },
            {
                "abi": "0x2f6f07cdcf3588944bf4c42ac74ff24bf56e7590",
                "contracts": [
                    "0x2f6f07cdcf3588944bf4c42ac74ff24bf56e7590",  # STG Token
                ],
                "topics": [
                    "0x664e26797cde1146ddfcb9a5d3f4de61179f9c11b2698599bb09e686f442172b",  # SendToChain
                    "0x831bc68226f8d1f734ffcca73602efc4eca13711402ba1d2cc05ee17bb54f631",  # ReceiveFromChain
                ],
            },
            {
                "abi": "baseoftv2",
                "contracts": [
                    "0x371c7ec6d8039ff7933a2aa28eb827ffe1f52f07",
                    "0x2297aebd383787a160dd0d9f71508148769342e3",
                    "0x62d0a8458ed7719fdaf978fe5929c6d342b0bfce",
                    "0x96e1056a8814de39c8c3cd0176042d6cecd807d7",
                    "0x35643752f4ea0ba70456f0ca1e2778f783206a20",
                    "0x656d33bfb74863e7ab1f5496a7a86a717a18a8d9",
                    "0x188fb5f5ae5bbe4154d5778f2bbb2fb985c94d25",
                    "0x2ec2fceffea8bca4e60c2c813f81f9ade7d323d2",
                    "0xb2c659255f3428824d03f7410058476d6e820580",
                ],
                "topics": [
                    "0xd81fc9b8523134ed613870ed029d6170cbb73aa6a6bc311b9a642689fb9df59a",  # SendToChain
                    "0xbf551ec93859b170f9b2141bd9298bf3f64322c6f7beb2543a0cb669834118bf",  # ReceiveFromChain
                ],
            },
            {
                "abi": "oft",
                "contracts": [
                    "0x12dC9256Acc9895B076f6638D628382881e62CeE",  # Stargate Pool USDT
                    "0x5634c4a5FEd09819E3c46D86A965Dd9447d86e47",  # Stargate Pool USDC
                    "0x6985884C4392D348587B19cb9eAAf157F13271cd",  # Layer Zero OFT Token
                ],
                "topics": [
                    "0x85496b760a4b7f8d66384b9df21b381f5d1b1e79f229a47aaf4c232edc2fe59a",  # OFTSent
                    "0xefed6d3500546b29533b128a29e3a94d70788727f0507505ac12eaf2e578fd9c",  # OFTReceived
                ],
            },
            {
                "abi": "lptokenerc20",
                "contracts": [
                    "0x29e38769f23701a2e4a8ef0492e19da4604be62c",  # Stargate Finance: S*USDT Token (LPTokenERC20)
                    "0x1205f31718499dBf1fCa446663B532Ef87481fe1",  # Stargate Finance: S*USDC Token (LPTokenERC20)
                    "0xEAe5c2F6B25933deB62f754f239111413A0A25ef",  # Stargate Finance: Tether Token-LP
                    "0x1c272232df0bb6225da87f4decd9d37c32f63eea",  # Stargate Finance: S*FRAX Token (LPTokenERC20)
                ],
                "topics": [
                    "0x34660fc8af304464529f48a778e03d03e4d34bcd5f9b6f0cfbf3cd238c642f7f",  # Swap
                    "0xfb2b592367452f1c437675bed47f5e1e6c25188c17d7ba01a12eb030bc41ccef",  # SwapRemote
                ],
            },
        ],
        "base": [
            {
                "abi": "0x5634c4a5FEd09819E3c46D86A965Dd9447d86e47",
                "contracts": [
                    "0x5634c4a5FEd09819E3c46D86A965Dd9447d86e47",  # Stargate: Token Messaging
                ],
                "topics": [
                    "0x15955c5a4cc61b8fbb05301bce47fd31c0e6f935e1ab97fdac9b134c887bb074",  # BusRode
                    "0x1623f9ea59bd6f214c9571a892da012fc23534aa5906bef4ae8c5d15ee7d2d6e",  # BusDriven
                ],
            },
            {
                "abi": "0x1a44076050125825900e736c501f859c50fE728c",
                "contracts": [
                    "0x1a44076050125825900e736c501f859c50fE728c",  # EndpointV2
                ],
                "topics": [
                    "0x1ab700d4ced0c005b164c0f789fd09fcbb0156d4c2041b8a3bfbcd961cd1567f",  # PacketSent
                    "0x3cd5e48f9730b129dc7550f0fcea9c767b7be37837cd10e55eb35f734f4bca04",  # PacketDelivered
                    "0x0d87345f3d1c929caba93e1c3821b54ff3512e12b66aa3cfe54b6bcbc17e59b4",  # PacketVerified
                    "0x3d52ff888d033fd3dd1d8057da59e850c91d91a72c41dfa445b247dfedeb6dc1",  # ComposeSent
                    "0x0036c98efcf9e6641dfbc9051f66f405253e8e0c2ab4a24dccda15595b7378c8",  # ComposeDelivered
                ],
            },
            {
                "abi": "0x38de71124f7a447a01d67945a51edce9ff491251",
                "contracts": [
                    "0x38de71124f7a447a01d67945a51edce9ff491251",  # Layer Zero: Ultra Light Node v2
                ],
                "topics": [
                    "0xe9bded5f24a4168e4f3bf44e00298c993b22376aad8c58c7dda9718a54cbea82",  # Packet
                    "0x2bd2d8a84b748439fd50d79a49502b4eb5faa25b864da6a9ab5c150704be9a4d",  # PacketReceived
                ],
            },
            {
                "abi": "0xB5320B0B3a13cC860893E2Bd79FCd7e13484Dda2",
                "contracts": [
                    "0xB5320B0B3a13cC860893E2Bd79FCd7e13484Dda2",  # SendUln302
                ],
                "topics": [
                    "0x61ed099e74a97a1d7f8bb0952a88ca8b7b8ebd00c126ea04671f92a81213318a",  # ExecutorFeePaid
                    "0x07ea52d82345d6e838192107d8fd7123d9c2ec8e916cd0aad13fd2b60db24644",  # DVNFeePaid
                ],
            },
            {
                "abi": "0xc70AB6f32772f59fBfc23889Caf4Ba3376C84bAf",
                "contracts": [
                    "0xc70AB6f32772f59fBfc23889Caf4Ba3376C84bAf",  # ReceiveUln302
                ],
                "topics": [
                    "0x82118522aa536ac0e96cc5c689407ae42b89d592aa133890a01f1509842f5081",  # UlnConfigSet
                    "0x2cb0eed7538baeae4c6fde038c0fd0384d27de0dd55a228c65847bda6aa1ab56",  # PayloadVerified
                ],
            },
            {
                "abi": "0xD56e4eAb23cb81f43168F9F45211Eb027b9aC7cc",
                "contracts": [
                    "0xD56e4eAb23cb81f43168F9F45211Eb027b9aC7cc",  # VerifierNetwork
                ],
                "topics": [
                    "0x87e46b0a6199bc734632187269a103c05714ee0adae5b28f30723955724f37ef",  # VerifierFeePaid
                ],
            },
            {
                "abi": "relayerv2",
                "contracts": [
                    "0xcb566e3B6934Fa77258d68ea18E931fa75e1aaAa",  # Layer Zero: Relayer V2
                ],
                "topics": [
                    "0xdf21c415b78ed2552cc9971249e32a053abce6087a0ae0fbf3f78db5174a3493",  # AssignJob
                ],
            },
            {
                "abi": "0xE3B53AF74a4BF62Ae5511055290838050bf764Df",
                "contracts": [
                    "0xE3B53AF74a4BF62Ae5511055290838050bf764Df",  # STG Token
                ],
                "topics": [
                    "0x664e26797cde1146ddfcb9a5d3f4de61179f9c11b2698599bb09e686f442172b",  # SendToChain
                    "0x831bc68226f8d1f734ffcca73602efc4eca13711402ba1d2cc05ee17bb54f631",  # ReceiveFromChain
                ],
            },
            {
                "abi": "baseoftv2",
                "contracts": [
                    "0x1572d48a52906b834fb236aa77831d669f6d87a1",
                    "0x2dad3a13ef0c6366220f989157009e501e7938f8",
                    "0xf544251d25f3d243a36b07e7e7962a678f952691",
                    "0xd722e55c1d9d9fa0021a5215cbb904b92b3dc5d4",
                    "0xba0dda8762c24da9487f5fa026a9b64b695a07ea",
                    "0x3055913c90fcc1a6ce9a358911721eeb942013a1",
                    "0xbfd5206962267c7b4b4a8b3d76ac2e1b2a5c4d5e",
                    "0x1509706a6c66ca549ff0cb464de88231ddbe213b",
                    "0x64b88c73a5dfa78d1713fe1b4c69a22d7e0faaa7",
                    "0xc48e605c7b722a57277e087a6170b9e227e5ac0a",
                    "0xfa980ced6895ac314e7de34ef1bfae90a5add21b",
                    "0xd2012fc1b913ce50732ebcaa7e601fe37ac728c6",
                    "0x25ea98ac87a38142561ea70143fd44c4772a16b6",
                    "0x2b1d36f5b61addaf7da7ebbd11b35fd8cfb0de31",
                    "0x17de46760f4c18c26eec36117c23793299f564a8",
                    "0x9483ab65847a447e36d21af1cab8c87e9712ff93",
                    "0x4035957323fc05ad9704230e3dc1e7663091d262",
                    "0xc19669a405067927865b40ea045a2baabbbe57f5",
                ],
                "topics": [
                    "0xd81fc9b8523134ed613870ed029d6170cbb73aa6a6bc311b9a642689fb9df59a",  # SendToChain
                    "0xbf551ec93859b170f9b2141bd9298bf3f64322c6f7beb2543a0cb669834118bf",  # ReceiveFromChain
                ],
            },
            {
                "abi": "oft",
                "contracts": [
                    "0xdc181Bd607330aeeBEF6ea62e03e5e1Fb4B6F7C7",  # Stargate Pool Native
                    "0x27a16dc786820B16E5c9028b75B99F6f604b5d26",  # Stargate Pool USDC
                    "0x6985884c4392d348587b19cb9eaaf157f13271cd",  # Layer Zero OFT Token
                ],
                "topics": [
                    "0x85496b760a4b7f8d66384b9df21b381f5d1b1e79f229a47aaf4c232edc2fe59a",  # OFTSent
                    "0xefed6d3500546b29533b128a29e3a94d70788727f0507505ac12eaf2e578fd9c",  # OFTReceived
                ],
            },
            {
                "abi": "lptokenerc20",
                "contracts": [
                    "0x28fc411f9e1c480AD312b3d9C60c22b965015c6B",  # Stargate Finance: S*GETH Token-LP
                    "0x4c80E24119CFB836cdF0a6b53dc23F04F7e652CA",  # Stargate Finance: S*USDbC Token (LPTokenERC20)
                ],
                "topics": [
                    "0x34660fc8af304464529f48a778e03d03e4d34bcd5f9b6f0cfbf3cd238c642f7f",  # Swap
                    "0xfb2b592367452f1c437675bed47f5e1e6c25188c17d7ba01a12eb030bc41ccef",  # SwapRemote
                ],
            },
        ],
        "linea": [
            {
                "abi": "0x5f688f563dc16590e570f97b542fa87931af2fed",
                "contracts": [
                    "0x5f688f563dc16590e570f97b542fa87931af2fed",  # Stargate: Token Messaging
                ],
                "topics": [
                    "0x15955c5a4cc61b8fbb05301bce47fd31c0e6f935e1ab97fdac9b134c887bb074",  # BusRode
                    "0x1623f9ea59bd6f214c9571a892da012fc23534aa5906bef4ae8c5d15ee7d2d6e",  # BusDriven
                ],
            },
            {
                "abi": "0x1a44076050125825900e736c501f859c50fE728c",
                "contracts": [
                    "0x1a44076050125825900e736c501f859c50fE728c",  # EndpointV2
                ],
                "topics": [
                    "0x1ab700d4ced0c005b164c0f789fd09fcbb0156d4c2041b8a3bfbcd961cd1567f",  # PacketSent
                    "0x3cd5e48f9730b129dc7550f0fcea9c767b7be37837cd10e55eb35f734f4bca04",  # PacketDelivered
                    "0x0d87345f3d1c929caba93e1c3821b54ff3512e12b66aa3cfe54b6bcbc17e59b4",  # PacketVerified
                    "0x3d52ff888d033fd3dd1d8057da59e850c91d91a72c41dfa445b247dfedeb6dc1",  # ComposeSent
                    "0x0036c98efcf9e6641dfbc9051f66f405253e8e0c2ab4a24dccda15595b7378c8",  # ComposeDelivered
                ],
            },
            {
                "abi": "0x38de71124f7a447a01d67945a51edce9ff491251",
                "contracts": [
                    "0x38de71124f7a447a01d67945a51edce9ff491251",  # Layer Zero: Ultra Light Node v2
                ],
                "topics": [
                    "0xe9bded5f24a4168e4f3bf44e00298c993b22376aad8c58c7dda9718a54cbea82",  # Packet
                    "0x2bd2d8a84b748439fd50d79a49502b4eb5faa25b864da6a9ab5c150704be9a4d",  # PacketReceived
                ],
            },
            {
                "abi": "0x32042142DD551b4EbE17B6FEd53131dd4b4eEa06",
                "contracts": [
                    "0x32042142DD551b4EbE17B6FEd53131dd4b4eEa06",  # SendUln302
                ],
                "topics": [
                    "0x61ed099e74a97a1d7f8bb0952a88ca8b7b8ebd00c126ea04671f92a81213318a",  # ExecutorFeePaid
                    "0x07ea52d82345d6e838192107d8fd7123d9c2ec8e916cd0aad13fd2b60db24644",  # DVNFeePaid
                ],
            },
            # {
            #     "abi": "",
            #     "contracts": [
            #         "",  # ReceiveUln302
            #     ],
            #     "topics": [
            #         "0x82118522aa536ac0e96cc5c689407ae42b89d592aa133890a01f1509842f5081",  # UlnConfigSet
            #         "0x2cb0eed7538baeae4c6fde038c0fd0384d27de0dd55a228c65847bda6aa1ab56",  # PayloadVerified
            #     ],
            # },
            # {
            #     "abi": "0xD56e4eAb23cb81f43168F9F45211Eb027b9aC7cc",
            #     "contracts": [
            #         "0xD56e4eAb23cb81f43168F9F45211Eb027b9aC7cc",  # VerifierNetwork
            #     ],
            #     "topics": [
            #         "0x87e46b0a6199bc734632187269a103c05714ee0adae5b28f30723955724f37ef",  # VerifierFeePaid
            #     ],
            # },
            {
                "abi": "relayerv2",
                "contracts": [
                    "0xA658742d33ebd2ce2F0bdFf73515Aa797Fd161D9",  # Layer Zero: Relayer V2
                ],
                "topics": [
                    "0xdf21c415b78ed2552cc9971249e32a053abce6087a0ae0fbf3f78db5174a3493",  # AssignJob
                ],
            },
            {
                "abi": "oft",
                "contracts": [
                    "0x81F6138153d473E8c5EcebD3DC8Cd4903506B075",  # Stargate Pool Native
                ],
                "topics": [
                    "0x85496b760a4b7f8d66384b9df21b381f5d1b1e79f229a47aaf4c232edc2fe59a",  # OFTSent
                    "0xefed6d3500546b29533b128a29e3a94d70788727f0507505ac12eaf2e578fd9c",  # OFTReceived
                ],
            },
        ],
        "scroll": [
            {
                "abi": "0x4e422b0acb2bd7e3ac70b5c0e5eb806e86a94038",
                "contracts": [
                    "0x4e422b0acb2bd7e3ac70b5c0e5eb806e86a94038",  # Stargate: Token Messaging
                ],
                "topics": [
                    "0x15955c5a4cc61b8fbb05301bce47fd31c0e6f935e1ab97fdac9b134c887bb074",  # BusRode
                    "0x1623f9ea59bd6f214c9571a892da012fc23534aa5906bef4ae8c5d15ee7d2d6e",  # BusDriven
                ],
            },
            {
                "abi": "0x1a44076050125825900e736c501f859c50fE728c",
                "contracts": [
                    "0x1a44076050125825900e736c501f859c50fE728c",  # EndpointV2
                ],
                "topics": [
                    "0x1ab700d4ced0c005b164c0f789fd09fcbb0156d4c2041b8a3bfbcd961cd1567f",  # PacketSent
                    "0x3cd5e48f9730b129dc7550f0fcea9c767b7be37837cd10e55eb35f734f4bca04",  # PacketDelivered
                    "0x0d87345f3d1c929caba93e1c3821b54ff3512e12b66aa3cfe54b6bcbc17e59b4",  # PacketVerified
                    "0x3d52ff888d033fd3dd1d8057da59e850c91d91a72c41dfa445b247dfedeb6dc1",  # ComposeSent
                    "0x0036c98efcf9e6641dfbc9051f66f405253e8e0c2ab4a24dccda15595b7378c8",  # ComposeDelivered
                ],
            },
            {
                "abi": "0x38de71124f7a447a01d67945a51edce9ff491251",
                "contracts": [
                    "0x38de71124f7a447a01d67945a51edce9ff491251",  # Layer Zero: Ultra Light Node v2
                ],
                "topics": [
                    "0xe9bded5f24a4168e4f3bf44e00298c993b22376aad8c58c7dda9718a54cbea82",  # Packet
                    "0x2bd2d8a84b748439fd50d79a49502b4eb5faa25b864da6a9ab5c150704be9a4d",  # PacketReceived
                ],
            },
            {
                "abi": "0x9bbeb2b2184b9313cf5ed4a4ddfea2ef62a2a03b",
                "contracts": [
                    "0x9bbeb2b2184b9313cf5ed4a4ddfea2ef62a2a03b",  # SendUln302
                ],
                "topics": [
                    "0x61ed099e74a97a1d7f8bb0952a88ca8b7b8ebd00c126ea04671f92a81213318a",  # ExecutorFeePaid
                    "0x07ea52d82345d6e838192107d8fd7123d9c2ec8e916cd0aad13fd2b60db24644",  # DVNFeePaid
                ],
            },
            # {
            #     "abi": "",
            #     "contracts": [
            #         "",  # ReceiveUln302
            #     ],
            #     "topics": [
            #         "0x82118522aa536ac0e96cc5c689407ae42b89d592aa133890a01f1509842f5081",  # UlnConfigSet
            #         "0x2cb0eed7538baeae4c6fde038c0fd0384d27de0dd55a228c65847bda6aa1ab56",  # PayloadVerified
            #     ],
            # },
            # {
            #     "abi": "",
            #     "contracts": [
            #         "",  # VerifierNetwork
            #     ],
            #     "topics": [
            #         "0x87e46b0a6199bc734632187269a103c05714ee0adae5b28f30723955724f37ef",  # VerifierFeePaid
            #     ],
            # },
            {
                "abi": "relayerv2",
                "contracts": [
                    "0xa658742d33ebd2ce2f0bdff73515aa797fd161d9",  # Layer Zero: Relayer V2
                ],
                "topics": [
                    "0xdf21c415b78ed2552cc9971249e32a053abce6087a0ae0fbf3f78db5174a3493",  # AssignJob
                ],
            },
            {
                "abi": "oft",
                "contracts": [
                    "0xc2b638cb5042c1b3c5d5c969361fb50569840583",  # Stargate Pool Native
                    "0x3fc69cc4a842838bcdc9499178740226062b14e4",  # Stargate Pool USDC
                ],
                "topics": [
                    "0x85496b760a4b7f8d66384b9df21b381f5d1b1e79f229a47aaf4c232edc2fe59a",  # OFTSent
                    "0xefed6d3500546b29533b128a29e3a94d70788727f0507505ac12eaf2e578fd9c",  # OFTReceived
                ],
            },
        ],
    }
}

STARGATE_TOKEN_MESSAGING_CONTRACTS = {
    "ethereum": "0x6d6620efa72948c5f68a3c8646d58c00d3f4a980",
    "arbitrum": "0x19cfce47ed54a88614648dc3f19a5980097007dd",
    "bnb": "0x6e3d884c96d640526f273c61dfcf08915ebd7e2b",
    "polygon": "0x6ce9bf8cdab780416ad1fd87b318a077d2f50eac",
    "optimism": "0xf1fcb4cbd57b67d683972a59b6a7b1e2e8bf27e6",
    "avalanche": "0x17e450be3ba9557f2378e20d64ad417e59ef9a34",
    "base": "0x5634c4a5fed09819e3c46d86a965dd9447d86e47",
    "linea": "0x5f688f563dc16590e570f97b542fa87931af2fed",
    "scroll": "0x4e422b0acb2bd7e3ac70b5c0e5eb806e86a94038",
}

STARGATE_ENDPOINT_V2 = "0x1a44076050125825900e736c501f859c50fe728c"

BLOCKCHAIN_IDS = {
    "30184": {
        "nativeChainId": 8453,
        "name": "base",
    },
    "30111": {
        "nativeChainId": 10,
        "name": "optimism",
    },
    "30110": {
        "nativeChainId": 42161,
        "name": "arbitrum",
    },
    "30109": {
        "nativeChainId": 137,
        "name": "polygon",
    },
    "30106": {
        "nativeChainId": 43114,
        "name": "avalanche",
    },
    "30102": {
        "nativeChainId": 56,
        "name": "bnb",
    },
    "30101": {
        "nativeChainId": 1,
        "name": "ethereum",
    },
    "30183": {
        "nativeChainId": 59144,
        "name": "linea",
    },
    "30214": {
        "nativeChainId": 534352,
        "name": "scroll",
    },
}

STARGATE_POOL_TOKEN_MAPPING = {
    "ethereum": {
        "0x77b2043768d28e9c9ab44e1abfc95944bce57931": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",  # Stargate Pool Native
        "0xc026395860db2d07ee33e05fe50ed7bd583189c7": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",  # Stargate Pool USDC
        "0x933597a323eb81cae705c5bc29985172fd5a3973": "0xdac17f958d2ee523a2206206994597c13d831ec7",  # Stargate Pool USDT
        "0x6985884c4392d348587b19cb9eaaf157f13271cd": "0x6985884C4392D348587B19cb9eAAf157F13271cd",  # Layer Zero Token OFT
        "0x38ea452219524bb87e18de1c24d3bb59510bd783": "0xdac17f958d2ee523a2206206994597c13d831ec7",  # Stargate Finance: S*USDT Token (LPTokenERC20)
        "0xdf0770df86a8034b3efef0a1bb3c889b8332ff56": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",  # Stargate Finance: S*USDC Token (LPTokenERC20)
        "0x0Faf1d2d3CED330824de3B8200fc8dc6E397850d": "0x6b175474e89094c44da98b954eedeac495271d0f",  # Stargate Finance: S*DAI Token (LPTokenERC20)
        "0xfA0F307783AC21C39E939ACFF795e27b650F6e68": "0x853d955aCEf822Db058eb8505911ED77F175b99e",  # Stargate Finance: S*FRAX Token (LPTokenERC20)
        "0x692953e758c3669290cb1677180c64183cEe374e": "0x0C10bF8FcB7Bf5412187A595ab97a3609160b5c6",  # Stargate Finance: S*USDD Token (LPTokenERC20)
        "0x101816545f6bd2b1076434b54383a1e633390a2e": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",  # Stargate Finance: S*SGETH Token (LPTokenERC20)
    },
    "arbitrum": {
        "0xa45b5130f36cdca45667738e2a258ab09f4a5f7f": "0x82af49447d8a07e3bd95bd0d56f35241523fbab1",  # Stargate Pool Native
        "0xe8CDF27AcD73a434D661C84887215F7598e7d0d3": "0xaf88d065e77c8cC2239327C5EDb3A432268e5831",  # Stargate Pool USDC
        "0xce8cca271ebc0533920c83d39f417ed6a0abb7d0": "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9",  # Stargate Pool USDT
        "0x6985884c4392d348587b19cb9eaaf157f13271cd": "0x6985884c4392d348587b19cb9eaaf157f13271cd",  # Layer Zero Token OFT
        "0xB6CfcF89a7B22988bfC96632aC2A9D6daB60d641": "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9",  # Stargate Finance: S*USDT Token (LPTokenERC20)
        "0x892785f33cdee22a30aef750f285e18c18040c3e": "0xaf88d065e77c8cC2239327C5EDb3A432268e5831",  # Stargate Finance: S*USDC Token (LPTokenERC20)
        "0x600e576f9d853c95d58029093a16ee49646f3ca5": "0x93b346b6BC2548dA6A1E7d98E9a421B42541425b",  # Stargate Finance: S*LUSD Token (LPTokenERC20)
        "0x915A55e36A01285A14f05dE6e81ED9cE89772f8e": "0x82af49447d8a07e3bd95bd0d56f35241523fbab1",  # Stargate Finance: S*SGETH Token (LPTokenERC20)
    },
    "bnb": {
        "0x962Bd449E630b0d928f308Ce63f1A21F02576057": "0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d",  # Stargate Pool USDC
        "0x138EB30f73BC423c6455C53df6D89CB01d9eBc63": "0x55d398326f99059ff775485246999027b3197955",  # Stargate Pool USDT
        "0x6985884c4392d348587b19cb9eaaf157f13271cd": "0x6985884c4392d348587b19cb9eaaf157f13271cd",  # Layer Zero Token OFT
        "0x9aA83081AA06AF7208Dcc7A4cB72C94d057D2cda": "0x55d398326f99059ff775485246999027b3197955",  # Stargate Finance: S*USDT Token (LPTokenERC20)
        "0x98a5737749490856b401DB5Dc27F522fC314A4e1": "0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56",  # Stargate Finance: S*BUSD Token
        "0x4e145a589e4c03cBe3d28520e4BF3089834289Df": "0xd17479997F34dd9156Deef8F95A52D81D265be9c",  # Stargate Finance: S*USDD Token
    },
    "polygon": {
        "0x9aa02d4fae7f58b8e8f34c66e756cc734dac7fe4": "0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359",  # Stargate Pool USDC
        "0xd47b03ee6d86Cf251ee7860FB2ACf9f91B9fD4d7": "0xc2132d05d31c914a87c6611c10748aeb04b58e8f",  # Stargate Pool USDT
        "0x6985884c4392d348587b19cb9eaaf157f13271cd": "0x6985884c4392d348587b19cb9eaaf157f13271cd",  # Layer Zero Token OFT
        "0x29e38769f23701a2e4a8ef0492e19da4604be62c": "0xc2132d05d31c914a87c6611c10748aeb04b58e8f",  # Stargate Finance: S*USDT Token (LPTokenERC20)
        "0x1205f31718499dbf1fca446663b532ef87481fe1": "0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359",  # Stargate Finance: S*USDC Token (LPTokenERC20)
        "0x1c272232df0bb6225da87f4decd9d37c32f63eea": "0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063",  # Stargate Finance: S*DAI Token (LPTokenERC20)
    },
    "optimism": {
        "0xe8CDF27AcD73a434D661C84887215F7598e7d0d3": "0x4200000000000000000000000000000000000006",  # Stargate Pool Native
        "0xcE8CcA271Ebc0533920C83d39F417ED6A0abB7D0": "0x0b2C639c533813f4Aa9D7837CAf62653d097Ff85",  # Stargate Pool USDC
        "0x19cFCE47eD54a88614648DC3f19A5980097007dD": "0x94b008aa00579c1307b0ef2c499ad98a8ce58e58",  # Stargate Pool USDT
        "0x6985884c4392d348587b19cb9eaaf157f13271cd": "0x6985884c4392d348587b19cb9eaaf157f13271cd",  # Layer Zero Token OFT
        "0x368605d9c6243a80903b9e326f1cddde088b8924": "0x2E3D870790dC77A83DD1d18184Acc7439A53f475",  # Stargate Finance: S*FRAX Token (LPTokenERC20)
        "0x165137624f1f692e69659f944bf69de02874ee27": "0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1",  # Stargate Finance: S*DAI Token (LPTokenERC20)
        "0xDecC0c09c3B5f6e92EF4184125D5648a66E35298": "0x0b2C639c533813f4Aa9D7837CAf62653d097Ff85",  # Stargate Finance: S*USDC Token (LPTokenERC20)
        "0xd22363e3762cA7339569F3d33EADe20127D5F98C": "0x4200000000000000000000000000000000000006",  # Stargate Finance: S*GETH Token (LPTokenERC20)
        "0x3533f5e279bdbf550272a199a223da798d9eff78": "0xc40F949F8a4e094D1b49a23ea9241D289B7b2819",  # Stargate Finance: S*LUSD Token
    },
    "avalanche": {
        "0x5634c4a5FEd09819E3c46D86A965Dd9447d86e47": "0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E",  # Stargate Pool USDC
        "0x12dC9256Acc9895B076f6638D628382881e62CeE": "0x9702230A8Ea53601f5cD2dc00fDBc13d4dF4A8c7",  # Stargate Pool USDT
        "0x6985884C4392D348587B19cb9eAAf157F13271cd": "0x6985884c4392d348587b19cb9eaaf157f13271cd",  # Layer Zero OFT Token
        "0x29e38769f23701a2e4a8ef0492e19da4604be62c": "0x9702230A8Ea53601f5cD2dc00fDBc13d4dF4A8c7",  # Stargate Finance: S*USDT Token (LPTokenERC20)
        "0x1205f31718499dBf1fCa446663B532Ef87481fe1": "0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E",  # Stargate Finance: S*USDC Token (LPTokenERC20)
        "0xEAe5c2F6B25933deB62f754f239111413A0A25ef": "0x9702230A8Ea53601f5cD2dc00fDBc13d4dF4A8c7",  # Stargate Finance: Tether Token-LP
        "0x1c272232df0bb6225da87f4decd9d37c32f63eea": "0xD24C2Ad096400B6FBcd2ad8B24E7acBc21A1da64",  # Stargate Finance: S*FRAX Token (LPTokenERC20)
    },
    "base": {
        "0xdc181Bd607330aeeBEF6ea62e03e5e1Fb4B6F7C7": "0x4200000000000000000000000000000000000006",  # Stargate Pool Native
        "0x27a16dc786820B16E5c9028b75B99F6f604b5d26": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",  # Stargate Pool USDC
        "0x6985884c4392d348587b19cb9eaaf157f13271cd": "0x6985884c4392d348587b19cb9eaaf157f13271cd",  # Layer Zero OFT Token
        "0x28fc411f9e1c480AD312b3d9C60c22b965015c6B": "0x4200000000000000000000000000000000000006",  # Stargate Finance: S*GETH Token-LP
        "0x4c80E24119CFB836cdF0a6b53dc23F04F7e652CA": "0x4c80E24119CFB836cdF0a6b53dc23F04F7e652CA",  # Stargate Finance: S*USDbC Token (LPTokenERC20)
    },
    "linea": {
        "0x81F6138153d473E8c5EcebD3DC8Cd4903506B075": "0xe5D7C2a44FfDDf6b295A15c148167daaAf5Cf34f",  # Stargate Pool Native
    },
    "scroll": {
        "0xc2b638cb5042c1b3c5d5c969361fb50569840583": "0x5300000000000000000000000000000000000004",  # Stargate Pool Native
        "0x3fc69cc4a842838bcdc9499178740226062b14e4": "0x1d738a3436a8c49ceffbab7fbf04b660fb528cbd",  # Stargate Pool USDC
    },
}

STARGATE_OFT_TOKEN_MAPPING = {
    "ethereum": {
        "0x39b1f7c5b1ae6a3cb9bbbd616b44ced9f53882e0": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
        "0xaf5191b0de278c7286d6c7cc6ab6bb8a73ba2cd6": "0xaf5191b0de278c7286d6c7cc6ab6bb8a73ba2cd6",
        "0xe6828d65bf5023ae1851d90d8783cc821ba7eee1": "0xe6828d65bf5023ae1851d90d8783cc821ba7eee1",
        "0xb401f0cff9f05d10699c0e2c88a81dd923c1ffff": "0xC0c293ce456fF0ED870ADd98a0828Dd4d2903DBF",
        "0x7bb83ccb91aaee77f8e9bdcdd311e83aff6ff1f9": "0x62D0A8458eD7719FDAF978fe5929C6D342B0bFcE",
        "0x2297aebd383787a160dd0d9f71508148769342e3": "0x2297aebd383787a160dd0d9f71508148769342e3",
        "0x152649ea73beab28c5b49b26eb48f7ead6d4c898": "0x152649ea73beab28c5b49b26eb48f7ead6d4c898",
        "0x0b7f0e51cd1739d6c96982d55ad8fa634dd43a9c": "0x0b7f0e51cd1739d6c96982d55ad8fa634dd43a9c",
        "0xf8173a39c56a554837c4c7f104153a005d284d11": "0xf8173a39c56a554837c4c7f104153a005d284d11",
        "0x39d5313c3750140e5042887413ba8aa6145a9bd2": "0x39d5313c3750140e5042887413ba8aa6145a9bd2",
        "0x6ae382814e24b6ddf588901c597f26a9e945c577": "0x22Fc5A29bd3d6CCe19a06f844019fd506fCe4455",
        "0x580e933d90091b9ce380740e3a4a39c67eb85b4c": "0x580e933d90091b9ce380740e3a4a39c67eb85b4c",
        "0x8d279274789ccec8af94a430a5996eaace9609a9": "0x186eF81fd8E77EEC8BfFC3039e7eC41D5FC0b457",
        "0x8cfa44e930b7743123738eb2d7e78beaa964732e": "0x2b1D36f5B61AdDAf7DA7ebbd11B35FD8cfb0DE31",
        "0xc31813c38b32c0f826c2dbf3360d5899740c9669": "0x7138Eb0d563f3F6722500936A11DcAe99D738A2c",
        "0x439a5f0f5e8d149dda9a0ca367d4a8e4d6f83c10": "0x99D8a9C45b2ecA8864373A26D1459e3Dff1e17F3",
        "0x58ff71c056942600bc4acf8bdf48f82e6ad1f392": "0xa21Af1050F7B26e0cfF45ee51548254C41ED6b5c",
        "0x227dcc37d9a071d1a2adb7edc40b7ec38a2097b3": "0xba0Dda8762C24dA9487f5FA026a9B64b695A07Ea",
        "0x25d887ce7a35172c62febfd67a1856f20faebb00": "0x6982508145454ce325ddbe47a25d4ec3d2311933",
        "0x8aed0055d691e6d619acc96ad0fb3461f5774646": "0xb23d80f5FefcDDaa212212F028021B41DEd428CF",
        "0x137ddb47ee24eaa998a535ab00378d6bfa84f893": "0x137ddb47ee24eaa998a535ab00378d6bfa84f893",
        "0x98d4c2300b2916d56fb26308ee6870460c86859b": "0xBE03E60757f21f4b6fC8f16676AD9D5B1002E512",
        "0x560363bda52bc6a44ca6c8c9b4a5fadbda32fa60": "0x560363bda52bc6a44ca6c8c9b4a5fadbda32fa60",
        "0xdc402b5bb2725f8761c600aad79f06085fa5fbc4": "0x549020a9Cb845220D66d3E9c6D9F9eF61C981102",
        "0xf2a3300eb0574951e893ebff15089edb38fcfa3e": "0x73fBD93bFDa83B111DdC092aa3a4ca77fD30d380",
        "0x7122985656e38bdc0302db86685bb972b145bd3c": "0x7122985656e38bdc0302db86685bb972b145bd3c",
        "0x193f4a4a6ea24102f49b931deeeb931f6e32405d": "0x193f4a4a6ea24102f49b931deeeb931f6e32405d",
        "0x28a92dde19d9989f39a49905d7c9c2fac7799bdf": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        "0x888e317606b4c590bbad88653863e8b345702633": "0xd3CC9d8f3689B83c91b7B59cAB4946B063EB894A",
    },
    "arbitrum": {
        "0x6694340fc020c5e6b96567843da2df01b2ce1eb6": "0x6694340fc020c5e6b96567843da2df01b2ce1eb6",
        "0x9f018bda8f6b507a0c9e6f290b2f7c49c2f8daf8": "0x9f018bda8f6b507a0c9e6f290b2f7c49c2f8daf8",
        "0x1509706a6c66ca549ff0cb464de88231ddbe213b": "0x1509706a6c66ca549ff0cb464de88231ddbe213b",
        "0x2297aebd383787a160dd0d9f71508148769342e3": "0x2297aebd383787a160dd0d9f71508148769342e3",
        "0x1b896893dfc86bb67cf57767298b9073d2c1ba2c": "0x1b896893dfc86bb67cf57767298b9073d2c1ba2c",
        "0x1572d48a52906b834fb236aa77831d669f6d87a1": "0x82af49447d8a07e3bd95bd0d56f35241523fbab1",
        "0x04ac146cebd110adf4350df7ad029794a7528bd0": "0x8B0E6f19Ee57089F7649A455D89D7bC6314D04e8",
        "0x3b58a4c865b568a2f6a957c264f6b50cba35d8ce": "0x3b58a4c865b568a2f6a957c264f6b50cba35d8ce",
        "0xbdfdb3665c7d8374d86d54203e31f5c46c9f1712": "0x580E933D90091b9cE380740E3a4A39c67eB85B4c",
        "0x6db8b088c4d41d622b44cd81b900ba690f2d496c": "0x6db8b088c4d41d622b44cd81b900ba690f2d496c",
        "0x2b1d36f5b61addaf7da7ebbd11b35fd8cfb0de31": "0x2b1d36f5b61addaf7da7ebbd11b35fd8cfb0de31",
        "0x371c7ec6d8039ff7933a2aa28eb827ffe1f52f07": "0x371c7ec6d8039ff7933a2aa28eb827ffe1f52f07",
        "0x7448c7456a97769f6cd04f1e83a4a23ccdc46abd": "0x7448c7456a97769f6cd04f1e83a4a23ccdc46abd",
        "0x957a8af7894e76e16db17c2a913496a4e60b7090": "0xFEa7a6a0B346362BF88A9e4A88416B77a57D6c2A",
        "0x66e535e8d2ebf13f49f3d49e5c50395a97c137b1": "0x66e535e8d2ebf13f49f3d49e5c50395a97c137b1",
        "0xb688ba096b7bb75d7841e47163cd12d18b36a5bf": "0xb688ba096b7bb75d7841e47163cd12d18b36a5bf",
        "0x188fb5f5ae5bbe4154d5778f2bbb2fb985c94d25": "0x188fb5f5ae5bbe4154d5778f2bbb2fb985c94d25",
        "0x7be5dd337cc6ce3e474f64e2a92a566445290864": "0x7be5dd337cc6ce3e474f64e2a92a566445290864",
        "0x9e20461bc2c4c980f62f1b279d71734207a6a356": "0x9e20461bc2c4c980f62f1b279d71734207a6a356",
        "0xbfd5206962267c7b4b4a8b3d76ac2e1b2a5c4d5e": "0xbfd5206962267c7b4b4a8b3d76ac2e1b2a5c4d5e",
        "0xba0dda8762c24da9487f5fa026a9b64b695a07ea": "0xba0dda8762c24da9487f5fa026a9b64b695a07ea",
        "0x25d887ce7a35172c62febfd67a1856f20faebb00": "0x25d887ce7a35172c62febfd67a1856f20faebb00",
        "0x2ac2b254bc18cd4999f64773a966e4f4869c34ee": "0x2ac2b254bc18cd4999f64773a966e4f4869c34ee",
        "0x3de81ce90f5a27c5e6a5adb04b54aba488a6d14e": "0x3de81ce90f5a27c5e6a5adb04b54aba488a6d14e",
        "0x3082cc23568ea640225c2467653db90e9250aaa0": "0x3082cc23568ea640225c2467653db90e9250aaa0",
        "0xe71bdfe1df69284f00ee185cf0d95d0c7680c0d4": "0xe71bdfe1df69284f00ee185cf0d95d0c7680c0d4",
        "0x560363bda52bc6a44ca6c8c9b4a5fadbda32fa60": "0x560363bda52bc6a44ca6c8c9b4a5fadbda32fa60",
        "0xddbfbd5dc3ba0feb96cb513b689966b2176d4c09": "0xddbfbd5dc3ba0feb96cb513b689966b2176d4c09",
        "0xa9004a5421372e1d83fb1f85b0fc986c912f91f3": "0xa9004a5421372e1d83fb1f85b0fc986c912f91f3",
        "0x20cea49b5f7a6dbd78cae772ca5973ef360aa1e6": "0xc1Eb7689147C81aC840d4FF0D298489fc7986d52",
        "0x7f4db37d7beb31f445307782bc3da0f18df13696": "0x7f4db37d7beb31f445307782bc3da0f18df13696",
    },
    "bnb": {
        "0xb0d502e938ed5f4df2e681fe6e419ff29631d62b": "0xb0d502e938ed5f4df2e681fe6e419ff29631d62b",
        "0xe6828d65bf5023ae1851d90d8783cc821ba7eee1": "0x34294AfABCbaFfc616ac6614F6d2e17260b78BEd",
        "0x2297aebd383787a160dd0d9f71508148769342e3": "0x2297aebd383787a160dd0d9f71508148769342e3",
        "0xb274202daba6ae180c665b4fbe59857b7c3a8091": "0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82",
        "0x67fb304001ad03c282266b965b51e97aa54a2fab": "0xBdEAe1cA48894A1759A8374D63925f21f2Ee2639",
        "0xcf7d4b692c478b77aff32bb1493c54c84f27f85a": "0x0b15Ddf19D47E6a86A56148fb4aFFFc6929BcB89",
        "0x8d279274789ccec8af94a430a5996eaace9609a9": "0x8d279274789ccec8af94a430a5996eaace9609a9",
        "0x371c7ec6d8039ff7933a2aa28eb827ffe1f52f07": "0x371c7ec6d8039ff7933a2aa28eb827ffe1f52f07",
        "0x336f374198c872ba760e85af9c6331c3c5a535d3": "0x336f374198c872ba760e85af9c6331c3c5a535d3",
        "0xcecb301c2e2a04dd631428c386dd21db70716f8a": "0xcecb301c2e2a04dd631428c386dd21db70716f8a",
        "0x25ea98ac87a38142561ea70143fd44c4772a16b6": "0x25ea98ac87a38142561ea70143fd44c4772a16b6",
        "0x0465aad9da170798433f4ab7fa7ec8b9b9bf0bb1": "0x0465aad9da170798433f4ab7fa7ec8b9b9bf0bb1",
        "0xb7e2713cf55cf4b469b5a8421ae6fc0ed18f1467": "0xb7e2713cf55cf4b469b5a8421ae6fc0ed18f1467",
        "0x9e20461bc2c4c980f62f1b279d71734207a6a356": "0x9e20461bc2c4c980f62f1b279d71734207a6a356",
        "0x11cd72f7a4b699c67f225ca8abb20bc9f8db90c7": "0x11cd72f7a4b699c67f225ca8abb20bc9f8db90c7",
        "0x25d887ce7a35172c62febfd67a1856f20faebb00": "0x25d887ce7a35172c62febfd67a1856f20faebb00",
        "0x5012c90f14d190607662ca8344120812aaa2639d": "0x5012c90f14d190607662ca8344120812aaa2639d",
        "0xf7de7e8a6bd59ed41a4b5fe50278b3b7f31384df": "0xf7de7e8a6bd59ed41a4b5fe50278b3b7f31384df",
        "0x560363bda52bc6a44ca6c8c9b4a5fadbda32fa60": "0x477bC8d23c634C154061869478bce96BE6045D12",
        "0xe62b7c22484f8b031930275d31f42b9a517fe038": "0xe62b7c22484f8b031930275d31f42b9a517fe038",
        "0x0e446faad63e344167489b5cf1111f4cc305cbd3": "0x73fBD93bFDa83B111DdC092aa3a4ca77fD30d380",
        "0x80137510979822322193fc997d400d5a6c747bf7": "0x80137510979822322193fc997d400d5a6c747bf7",
        "0x982e609643794a31a07f5c5b142dd3a9cf0690be": "0x982e609643794a31a07f5c5b142dd3a9cf0690be",
        "0x193f4a4a6ea24102f49b931deeeb931f6e32405d": "0x193f4a4a6ea24102f49b931deeeb931f6e32405d",
        "0xa9004a5421372e1d83fb1f85b0fc986c912f91f3": "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c",
        "0xf8f46791e3db29a029ec6c9d946226f3c613e854": "0xcF6BB5389c92Bdda8a3747Ddb454cB7a64626C63",
    },
    "polygon": {
        "0x2f6f07cdcf3588944bf4c42ac74ff24bf56e7590": "0x2f6f07cdcf3588944bf4c42ac74ff24bf56e7590",
        "0xe6828d65bf5023ae1851d90d8783cc821ba7eee1": "0xe6828d65bf5023ae1851d90d8783cc821ba7eee1",
        "0xdef87c507ef911fd99c118c53171510eb7967738": "0x0169eC1f8f639B32Eec6D923e24C2A2ff45B9DD6",
        "0x1509706a6c66ca549ff0cb464de88231ddbe213b": "0x1509706a6c66ca549ff0cb464de88231ddbe213b",
        "0x2297aebd383787a160dd0d9f71508148769342e3": "0x2297aebd383787a160dd0d9f71508148769342e3",
        "0xfe0855903e32953de8e63ff6585f3fb5a2b4deff": "0x7ceb23fd6bc0add59e62ac25578270cff1b9f619",
        "0x110b25d2b21ee73eb401f3ae7833f7072912a0bf": "0x110b25d2b21ee73eb401f3ae7833f7072912a0bf",
        "0x9e20461bc2c4c980f62f1b279d71734207a6a356": "0x9e20461bc2c4c980f62f1b279d71734207a6a356",
        "0x11cd72f7a4b699c67f225ca8abb20bc9f8db90c7": "0x11cd72f7a4b699c67f225ca8abb20bc9f8db90c7",
        "0xc19669a405067927865b40ea045a2baabbbe57f5": "0xc19669a405067927865b40ea045a2baabbbe57f5",
        "0x00e8c0e92eb3ad88189e7125ec8825edc03ab265": "0x00e8c0e92eb3ad88189e7125ec8825edc03ab265",
    },
    "optimism": {
        "0x296f55f8fb28e498b858d0bcda06d955b2cb3f97": "0x296f55f8fb28e498b858d0bcda06d955b2cb3f97",
        "0x2297aebd383787a160dd0d9f71508148769342e3": "0x2297aebd383787a160dd0d9f71508148769342e3",
        "0xe2510aa4b019af3eb835d3ac9c800382109a4631": "0x4200000000000000000000000000000000000006",
        "0x0c9d44f5a573f6cfc9e8264a5ca72a1184616ef4": "0x2dAD3a13ef0C6366220f989157009e501e7938F8",
        "0x66e535e8d2ebf13f49f3d49e5c50395a97c137b1": "0x66e535e8d2ebf13f49f3d49e5c50395a97c137b1",
        "0xbfd5206962267c7b4b4a8b3d76ac2e1b2a5c4d5e": "0xbfd5206962267c7b4b4a8b3d76ac2e1b2a5c4d5e",
        "0xe71bdfe1df69284f00ee185cf0d95d0c7680c0d4": "0xe71bdfe1df69284f00ee185cf0d95d0c7680c0d4",
        "0x1f514a61bcde34f94bc39731235690ab9da737f7": "0x1f514a61bcde34f94bc39731235690ab9da737f7",
    },
    "avalanche": {
        "0x2f6f07cdcf3588944bf4c42ac74ff24bf56e7590": "0x2f6f07cdcf3588944bf4c42ac74ff24bf56e7590",
        "0x62d0a8458ed7719fdaf978fe5929c6d342b0bfce": "0x62d0a8458ed7719fdaf978fe5929c6d342b0bfce",
        "0x2297aebd383787a160dd0d9f71508148769342e3": "0x152b9d0FdC40C096757F570A51E494bd4b943E50",
        "0x371c7ec6d8039ff7933a2aa28eb827ffe1f52f07": "0x6e84a6216eA6dACC71eE8E6b0a5B7322EEbC0fDd",
        "0x188fb5f5ae5bbe4154d5778f2bbb2fb985c94d25": "0xcCf719c44e2C36E919335692E89d22Cf13D6aaEB",
        "0x96e1056a8814de39c8c3cd0176042d6cecd807d7": "0x96e1056a8814de39c8c3cd0176042d6cecd807d7",
        "0x35643752f4ea0ba70456f0ca1e2778f783206a20": "0x33C8036E99082B0C395374832FECF70c42C7F298",
        "0xb2c659255f3428824d03f7410058476d6e820580": "0x23675Ba5d0A8075DA5Ba18756554e7633cEA2C85",
        "0x2ec2fceffea8bca4e60c2c813f81f9ade7d323d2": "0xb279f8DD152B99Ec1D84A489D32c35bC0C7F5674",
        "0x656d33bfb74863e7ab1f5496a7a86a717a18a8d9": "0x59414b3089ce2AF0010e7523Dea7E2b35d776ec7",
    },
    "base": {
        "0xE3B53AF74a4BF62Ae5511055290838050bf764Df": "0xE3B53AF74a4BF62Ae5511055290838050bf764Df",
        "0x1509706a6c66ca549ff0cb464de88231ddbe213b": "0x1509706a6c66ca549ff0cb464de88231ddbe213b",
        "0x3055913c90fcc1a6ce9a358911721eeb942013a1": "0x3055913c90fcc1a6ce9a358911721eeb942013a1",
        "0x1572d48a52906b834fb236aa77831d669f6d87a1": "0x4200000000000000000000000000000000000006",
        "0x2dad3a13ef0c6366220f989157009e501e7938f8": "0x2dad3a13ef0c6366220f989157009e501e7938f8",
        "0x2b1d36f5b61addaf7da7ebbd11b35fd8cfb0de31": "0x2b1d36f5b61addaf7da7ebbd11b35fd8cfb0de31",
        "0x64b88c73a5dfa78d1713fe1b4c69a22d7e0faaa7": "0x64b88c73a5dfa78d1713fe1b4c69a22d7e0faaa7",
        "0x4035957323fc05ad9704230e3dc1e7663091d262": "0x4A3A6Dd60A34bB2Aba60D73B4C88315E9CeB6A3D",
        "0x25ea98ac87a38142561ea70143fd44c4772a16b6": "0x25ea98ac87a38142561ea70143fd44c4772a16b6",
        "0xc48e605c7b722a57277e087a6170b9e227e5ac0a": "0xc48e605c7b722a57277e087a6170b9e227e5ac0a",
        "0xbfd5206962267c7b4b4a8b3d76ac2e1b2a5c4d5e": "0xbfd5206962267c7b4b4a8b3d76ac2e1b2a5c4d5e",
        "0xba0dda8762c24da9487f5fa026a9b64b695a07ea": "0xba0dda8762c24da9487f5fa026a9b64b695a07ea",
        "0xfa980ced6895ac314e7de34ef1bfae90a5add21b": "0xfa980ced6895ac314e7de34ef1bfae90a5add21b",
        "0xd722e55c1d9d9fa0021a5215cbb904b92b3dc5d4": "0xd722e55c1d9d9fa0021a5215cbb904b92b3dc5d4",
        "0x17de46760f4c18c26eec36117c23793299f564a8": "0x73fBD93bFDa83B111DdC092aa3a4ca77fD30d380",
        "0xc19669a405067927865b40ea045a2baabbbe57f5": "0xc19669a405067927865b40ea045a2baabbbe57f5",
        "0xd2012fc1b913ce50732ebcaa7e601fe37ac728c6": "0xd2012fc1b913ce50732ebcaa7e601fe37ac728c6",
        "0xf544251d25f3d243a36b07e7e7962a678f952691": "0xf544251d25f3d243a36b07e7e7962a678f952691",
        "0x9483ab65847a447e36d21af1cab8c87e9712ff93": "0x9483ab65847a447e36d21af1cab8c87e9712ff93",
    },
}
