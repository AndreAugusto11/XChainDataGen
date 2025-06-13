"""
This module tests a list of RPC endpoints for multiple blockchains and writes the valid
configurations to a JSON file. The test is made using the eth_getLogs RPC method, with a
dummy (but valid) contract address, topics, and block range.

Functions:
    test_rpcs(configs):
        Tests the provided RPC endpoints and writes the valid configurations to 'configs.json'.

    __main__:
        Loads the base configurations from 'base_configs.json' and calls the test_rpcs function.

Function Details:
    test_rpcs(configs):
        Args:
            configs (list): A list of configuration dictionaries. Each dictionary should contain:
                - name (str): The name of the configuration.
                - contract (str): The contract address to filter logs.
                - topics (list): The topics to filter logs.
                - start_block (str): The starting block number.
                - end_block (str): The ending block number.
                - rpcs (list): A list of RPC endpoint URLs.

        Returns:
            None. Writes the valid configurations to 'configs.json'.

        Raises:
            None. Catches and prints exceptions during RPC testing.
"""

from .generate_rpc_configs import generate_rpc_configs

__all__ = ["generate_rpc_configs"]
