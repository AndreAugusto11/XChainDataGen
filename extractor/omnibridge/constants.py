# Mapping of bridges to their supported blockchains and contracts
BRIDGE_CONFIG = {
    "blockchains": {
        "ethereum": [
            {
                "abi": "0x88ad09518695c6c3712AC10a214bE5109a655671",
                "contracts": [
                    "0x88ad09518695c6c3712AC10a214bE5109a655671",  # Gnosis Chain: ETH-xDAI Omni Bridge
                ],
                "topics": [
                    "0x59a9a8027b9c87b961e254899821c9a276b5efc35d1f7409ea4f291470f1629a",  # TokensBridgingInitiated (index_topic_1 address token, index_topic_2 address sender, uint256 value, index_topic_3 bytes32 messageId)
                    "0x9afd47907e25028cdaca89d193518c302bbb128617d5a992c5abd45815526593",  # TokensBridged (index_topic_1 address token, index_topic_2 address recipient, uint256 value, index_topic_3 bytes32 messageId)
                ],
            },
            {
                "abi": "0x4c36d2919e407f0cc2ee3c993ccf8ac26d9ce64e",
                "contracts": [
                    "0x4c36d2919e407f0cc2ee3c993ccf8ac26d9ce64e",  # POA Network: AMB-ETH-XDAI
                ],
                "topics": [
                    "0x482515ce3d9494a37ce83f18b72b363449458435fafdd7a53ddea7460fe01b58",  # UserRequestForAffirmation (index_topic_1 bytes32 messageId, bytes encodedData)
                ],
            },
            {
                # xDAI bridge
                "abi": "0x4aa42145aa6ebf72e164c9bbc74fbd3788045016",
                "contracts": [
                    "0x4aa42145aa6ebf72e164c9bbc74fbd3788045016",  # Gnosis Chain: xDai Bridge
                ],
                "topics": [
                    "0x1d491a427d1f8cc0d447496f300fac39f7306122481d8e663451eb268274146b",  # UserRequestForAffirmation (address recipient, uint256 value)
                    "0x4ab7d581336d92edbea22636a613e8e76c99ac7f91137c1523db38dbfb3bf329",  # RelayedMessage (address recipient, uint256 value, bytes32 transactionHash)
                ],
            },
        ],
        "gnosis": [
            {
                "abi": "0xf6a78083ca3e2a662d6dd1703c939c8ace2e268d",
                "contracts": [
                    "0xf6a78083ca3e2a662d6dd1703c939c8ace2e268d",  # Gnosis: xDai Bridge
                ],
                "topics": [
                    "0x59a9a8027b9c87b961e254899821c9a276b5efc35d1f7409ea4f291470f1629a",  # TokensBridgingInitiated (index_topic_1 address token, index_topic_2 address sender, uint256 value, index_topic_3 bytes32 messageId)
                    "0x9afd47907e25028cdaca89d193518c302bbb128617d5a992c5abd45815526593",  # TokensBridged (index_topic_1 address token, index_topic_2 address recipient, uint256 value, index_topic_3 bytes32 messageId)
                ],
            },
            {
                "abi": "0x75df5af045d91108662d8080fd1fefad6aa0bb59",
                "contracts": [
                    "0x75df5af045d91108662d8080fd1fefad6aa0bb59",  # Gnosis: ETH-xDAI Omni Bridge
                ],
                "topics": [
                    "0x520d2afde79cbd5db58755ac9480f81bc658e5c517fcae7365a3d832590b0183",  # UserRequestForSignature (index_topic_1 bytes32 messageId, bytes encodedData)
                    "0xbf06885f40778f5ccfb64497d3f92ce568ddaedb7e2fb4487f72690418cf8e4c",  # SignedForUserRequest (index_topic_1 address signer, bytes32 messageHash)
                    "0x5df9cc3eb93d8a9a481857a3b70a8ca966e6b80b25cf0ee2cce180ec5afa80a1",  # SignedForAffirmation (index_topic_1 address signer, bytes32 messageHash)
                ],
            },
            {
                # xDAI bridge
                "abi": "0x7301cfa0e1756b71869e93d4e4dca5c7d0eb0aa6",
                "contracts": [
                    "0x7301cfa0e1756b71869e93d4e4dca5c7d0eb0aa6",  # Gnosis: xDai Bridge 2
                ],
                "topics": [
                    "0x6fc115a803b8703117d9a3956c5a15401cb42401f91630f015eb6b043fa76253",  # AffirmationCompleted (address recipient, uint256 value, bytes32 transactionHash)
                    "0x5df9cc3eb93d8a9a481857a3b70a8ca966e6b80b25cf0ee2cce180ec5afa80a1",  # SignedForAffirmation (index_topic_1 address signer, bytes32 transactionHash)
                    "0x127650bcfb0ba017401abe4931453a405140a8fd36fece67bae2db174d3fdd63",  # UserRequestForSignature (address recipient, uint256 value)
                ],
            },
        ],
    }
}
