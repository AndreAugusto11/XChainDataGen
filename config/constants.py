from enum import Enum


# Enum for Bridges
class Bridge(Enum):
    STARGATE = "stargate"
    CCTP = "cctp"
    CCIP = "ccip"
    ACROSS = "across"
    POLYGON = "polygon"
    RONIN = "ronin"
    OMNIBRIDGE = "omnibridge"
    DEBRIDGE = "debridge"

BLOCKCHAIN_IDS = {
    "8453": {
        "name": "base",
        "native_token": "WETH",
        "native_token_contract": "0x4200000000000000000000000000000000000006",
    },
    "10": {
        "name": "optimism",
        "native_token": "OP",
        "native_token_contract": "0x4200000000000000000000000000000000000006",
    },
    "42161": {
        "name": "arbitrum",
        "native_token": "WETH",
        "native_token_contract": "0x82af49447d8a07e3bd95bd0d56f35241523fbab1",
    },
    "137": {
        "name": "polygon",
        "native_token": "MATIC",
        "native_token_contract": "0x0000000000000000000000000000000000001010",
    },
    "1": {
        "name": "ethereum",
        "native_token": "WETH",
        "native_token_contract": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
    },
    "534352": {
        "name": "scroll",
        "native_token": "WETH",
        "native_token_contract": "0x5300000000000000000000000000000000000004",
    },
    "59144": {
        "name": "linea",
        "native_token": "WETH",
        "native_token_contract": "0xe5d7c2a44ffddf6b295a15c148167daaaf5cf34f",
    },
    "56": {
        "name": "bnb",
        "native_token": "WBNB",
        "native_token_contract": "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c",
    },
    "43114": {
        "name": "avalanche",
        "native_token": "WAVAX",
        "native_token_contract": "0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7",
    },
    "100": {
        "name": "gnosis",
        "native_token": "WXDAI",
        "native_token_contract": "0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d",
    },
    "2020": {
        "name": "ronin",
        "native_token": "AXS",
    }
}

# the list of blockchains supported by Alchemy to retrieve token
# prices and metadata based on the contract address
# Each blockchain is mapped to a unique identifier used by Alchemy
TOKEN_PRICING_SUPPORTED_BLOCKCHAINS = {
    "ethereum": "eth",
    "optimism": "opt",
    "polygon": "polygon",
    "base": "base",
    "bnb": "bnb",
    "avalanche": "avax",
    "arbitrum": "arb",
    "scroll": "scroll",
    "linea": "linea",
    "gnosis": "gnosis"
}


RPCS_CONFIG_FILE = "config/rpcs_config.yaml"

MAX_NUM_THREADS_EXTRACTOR = 10
