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
    MAYAN = "mayan"


BLOCKCHAIN_IDS = {
    "8453": {
        "name": "base",
        "native_token": "WETH",
        "native_token_contract": "0x4200000000000000000000000000000000000006",
    },
    "10": {
        "name": "optimism",
        "native_token": "WETH",
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
    },
    "5eykt4UsFv8P8NJdTREpY1vzqKqZKvdpKuc147dw2N9d": { # genesis hash for Solana
        "name": "solana",
        "native_token": "SOL",
    },
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
    "gnosis": "gnosis",
}


# Mapping of bridges to their respective RPC methods
# The majority of bridges work fine using the 'eth_getTransactionReceipt' RPC method to
# retrieve transaction data. This method is generally sufficient because most contracts
# emit events that include the native token value when it is transferred, allowing us to
# calculate the relevant amounts directly from event data. As a result, the 'tx.value'
# field, which is not exported by 'eth_getTransactionReceipt', can typically be ignored.

# However, there are exceptions where the event data does not provide all necessary
# information, and in those cases, alternative methods (such as 'eth_getTransactionByHash')
# must be used to obtain the full transaction details, including 'tx.value'. This is the
# case for Mayan Bridge,

BRIDGE_NEEDS_TRANSACTION_BY_HASH_RPC_METHOD = {
    Bridge.STARGATE: False,
    Bridge.CCTP: False,
    Bridge.CCIP: False,
    Bridge.ACROSS: False,
    Bridge.POLYGON: False,
    Bridge.RONIN: False,
    Bridge.OMNIBRIDGE: False,
    Bridge.DEBRIDGE: True,
    Bridge.MAYAN: True,
}

RPCS_CONFIG_FILE = "config/rpcs_config.yaml"

MAX_NUM_THREADS_EXTRACTOR = 10
