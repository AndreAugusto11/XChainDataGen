# Mapping of bridges to their supported blockchains and contracts
BRIDGE_CONFIG = {
    "blockchains": {
        "ethereum": [
            {
                "abi": "dln_source",
                "contracts": [
                    "0xef4fb24ad0916217251f553c0596f8edc630eb66",
                ],
                "topics": [
                    "0xfc8703fd57380f9dd234a89dce51333782d49c5902f307b02f03e014d18fe471",  # CreatedOrder
                    "0x33fff3d864e92b6e1ef9e830196fc019c946104ea621b833aaebd3c3e84b2f6f",  # ClaimedUnlock
                ],
            },
            {
                "abi": "dln_destination",
                "contracts": [
                    "0xe7351fd770a37282b91d153ee690b63579d6dd7f",
                ],
                "topics": [
                    # "0x37a01d7dc38e924008cf4f2fa3d2ec1f45e7ae3c8292eb3e7d9314b7ad10e2fc",  # SentOrderUnlock
                    "0xd281ee92bab1446041582480d2c0a9dc91f855386bb27ea295faac1e992f7fe4",  # FulfilledOrder
                ],
            },
        ],
        "optimism": [
            {
                "abi": "dln_source",
                "contracts": [
                    "0xef4fb24ad0916217251f553c0596f8edc630eb66",
                ],
                "topics": [
                    "0xfc8703fd57380f9dd234a89dce51333782d49c5902f307b02f03e014d18fe471",  # CreatedOrder
                    "0x33fff3d864e92b6e1ef9e830196fc019c946104ea621b833aaebd3c3e84b2f6f",  # ClaimedUnlock
                ],
            },
            {
                "abi": "dln_destination",
                "contracts": [
                    "0xe7351fd770a37282b91d153ee690b63579d6dd7f",
                ],
                "topics": [
                    # "0x37a01d7dc38e924008cf4f2fa3d2ec1f45e7ae3c8292eb3e7d9314b7ad10e2fc",  # SentOrderUnlock
                    "0xd281ee92bab1446041582480d2c0a9dc91f855386bb27ea295faac1e992f7fe4",  # FulfilledOrder
                ],
            },
        ],
        "arbitrum": [
            {
                "abi": "dln_source",
                "contracts": [
                    "0xef4fb24ad0916217251f553c0596f8edc630eb66",
                ],
                "topics": [
                    "0xfc8703fd57380f9dd234a89dce51333782d49c5902f307b02f03e014d18fe471",  # CreatedOrder
                    "0x33fff3d864e92b6e1ef9e830196fc019c946104ea621b833aaebd3c3e84b2f6f",  # ClaimedUnlock
                ],
            },
            {
                "abi": "dln_destination",
                "contracts": [
                    "0xe7351fd770a37282b91d153ee690b63579d6dd7f",
                ],
                "topics": [
                    # "0x37a01d7dc38e924008cf4f2fa3d2ec1f45e7ae3c8292eb3e7d9314b7ad10e2fc",  # SentOrderUnlock
                    "0xd281ee92bab1446041582480d2c0a9dc91f855386bb27ea295faac1e992f7fe4",  # FulfilledOrder
                ],
            },
        ],
        "avalanche": [
            {
                "abi": "dln_source",
                "contracts": [
                    "0xef4fb24ad0916217251f553c0596f8edc630eb66",
                ],
                "topics": [
                    "0xfc8703fd57380f9dd234a89dce51333782d49c5902f307b02f03e014d18fe471",  # CreatedOrder
                    "0x33fff3d864e92b6e1ef9e830196fc019c946104ea621b833aaebd3c3e84b2f6f",  # ClaimedUnlock
                ],
            },
            {
                "abi": "dln_destination",
                "contracts": [
                    "0xe7351fd770a37282b91d153ee690b63579d6dd7f",
                ],
                "topics": [
                    # "0x37a01d7dc38e924008cf4f2fa3d2ec1f45e7ae3c8292eb3e7d9314b7ad10e2fc",  # SentOrderUnlock
                    "0xd281ee92bab1446041582480d2c0a9dc91f855386bb27ea295faac1e992f7fe4",  # FulfilledOrder
                ],
            },
        ],
        "base": [
            {
                "abi": "dln_source",
                "contracts": [
                    "0xef4fb24ad0916217251f553c0596f8edc630eb66",
                ],
                "topics": [
                    "0xfc8703fd57380f9dd234a89dce51333782d49c5902f307b02f03e014d18fe471",  # CreatedOrder
                    "0x33fff3d864e92b6e1ef9e830196fc019c946104ea621b833aaebd3c3e84b2f6f",  # ClaimedUnlock
                ],
            },
            {
                "abi": "dln_destination",
                "contracts": [
                    "0xe7351fd770a37282b91d153ee690b63579d6dd7f",
                ],
                "topics": [
                    # "0x37a01d7dc38e924008cf4f2fa3d2ec1f45e7ae3c8292eb3e7d9314b7ad10e2fc",  # SentOrderUnlock
                    "0xd281ee92bab1446041582480d2c0a9dc91f855386bb27ea295faac1e992f7fe4",  # FulfilledOrder
                ],
            },
        ],
        "bnb": [
            {
                "abi": "dln_source",
                "contracts": [
                    "0xef4fb24ad0916217251f553c0596f8edc630eb66",
                ],
                "topics": [
                    "0xfc8703fd57380f9dd234a89dce51333782d49c5902f307b02f03e014d18fe471",  # CreatedOrder
                    "0x33fff3d864e92b6e1ef9e830196fc019c946104ea621b833aaebd3c3e84b2f6f",  # ClaimedUnlock
                ],
            },
            {
                "abi": "dln_destination",
                "contracts": [
                    "0xe7351fd770a37282b91d153ee690b63579d6dd7f",
                ],
                "topics": [
                    # "0x37a01d7dc38e924008cf4f2fa3d2ec1f45e7ae3c8292eb3e7d9314b7ad10e2fc",  # SentOrderUnlock
                    "0xd281ee92bab1446041582480d2c0a9dc91f855386bb27ea295faac1e992f7fe4",  # FulfilledOrder
                ],
            },
        ],
        "polygon": [
            {
                "abi": "dln_source",
                "contracts": [
                    "0xef4fb24ad0916217251f553c0596f8edc630eb66",
                ],
                "topics": [
                    "0xfc8703fd57380f9dd234a89dce51333782d49c5902f307b02f03e014d18fe471",  # CreatedOrder
                    "0x33fff3d864e92b6e1ef9e830196fc019c946104ea621b833aaebd3c3e84b2f6f",  # ClaimedUnlock
                ],
            },
            {
                "abi": "dln_destination",
                "contracts": [
                    "0xe7351fd770a37282b91d153ee690b63579d6dd7f",
                ],
                "topics": [
                    # "0x37a01d7dc38e924008cf4f2fa3d2ec1f45e7ae3c8292eb3e7d9314b7ad10e2fc",  # SentOrderUnlock
                    "0xd281ee92bab1446041582480d2c0a9dc91f855386bb27ea295faac1e992f7fe4",  # FulfilledOrder
                ],
            },
        ],
        "linea": [
            {
                "abi": "dln_source",
                "contracts": [
                    "0xef4fb24ad0916217251f553c0596f8edc630eb66",
                ],
                "topics": [
                    "0xfc8703fd57380f9dd234a89dce51333782d49c5902f307b02f03e014d18fe471",  # CreatedOrder
                    "0x33fff3d864e92b6e1ef9e830196fc019c946104ea621b833aaebd3c3e84b2f6f",  # ClaimedUnlock
                ],
            },
            {
                "abi": "dln_destination",
                "contracts": [
                    "0xe7351fd770a37282b91d153ee690b63579d6dd7f",
                ],
                "topics": [
                    # "0x37a01d7dc38e924008cf4f2fa3d2ec1f45e7ae3c8292eb3e7d9314b7ad10e2fc",  # SentOrderUnlock
                    "0xd281ee92bab1446041582480d2c0a9dc91f855386bb27ea295faac1e992f7fe4",  # FulfilledOrder
                ],
            },
        ],
    }
}

BLOCKCHAIN_IDS = {
    "8453": {
        "name": "base",
    },
    "10": {
        "name": "optimism",
    },
    "42161": {
        "name": "arbitrum",
    },
    "137": {
        "name": "polygon",
    },
    "1": {
        "name": "ethereum",
    },
    "59144": {
        "name": "linea",
    },
    "56": {
        "name": "bnb",
    },
    "43114": {
        "name": "avalanche",
    },
    "7565164": { # genesis hash for Solana
        "name": "solana",
    },
}

SOLANA_PROGRAM_ADDRESSES = [
    "src5qyZHqTqecJV4aY6Cb6zDZLMDzrDKKezs22MPHr4",
    "dst5MGcFPoBeREFAA5E3tU5ij8m5uVYwkzkSAbsLbNo",
]
