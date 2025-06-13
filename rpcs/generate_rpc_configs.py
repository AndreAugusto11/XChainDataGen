import yaml

from utils.rpc_utils import RPCClient

final_configs = []


def generate_rpc_configs(blockchain: list):
    print(f"Generating RPC configurations for {blockchain}...")
    with open("./config/rpcs_base_config.yaml") as f:
        configs = yaml.safe_load(f)

    test_rpcs(configs, blockchain)


def test_rpcs(configs, blockchains):
    """
    Tests the RPC endpoints for each blockchain configuration provided and removes the ones that are not available.

    The function iterates through the list of blockchain configurations, sends a request to each RPC endpoint, 
    and checks if logs are returned. If no logs are found, the RPC endpoint is considered unavailable and is removed 
    from the list. The final configurations with available RPCs are then written to a YAML file.

    Args:
        configs (dict): A dictionary containing blockchain configurations. Each configuration should include:
            - name (str): The name of the blockchain.
            - contract (str): The contract address.
            - topics (list): The list of topics to filter logs.
            - start_block (str): The starting block number.
            - end_block (str): The ending block number.
            - rpcs (list): The list of RPC endpoints to test.

    Raises:
        Exception: If no logs are found for a given RPC endpoint.

    Outputs:
        Writes the final configurations with available RPCs to a YAML file at './config/rpcs_config.yaml'.
    """
    for config in configs["blockchains"]:

        if config["name"] not in blockchains:
            continue

        rpcs = []

        for rpc in config["rpcs"]:
            try:
                response = RPCClient.plain_request(
                    rpc,
                    "eth_getLogs",
                    [
                        {
                            "fromBlock": config["start_block"],
                            "toBlock": config["end_block"],
                            "topics": config["topics"],
                            "address": config["contract"],
                        }
                    ],
                )

                if "result" not in response:
                    raise Exception(f"Invalid RPC response: {response}")
                
                if "error" in response:
                    raise Exception(f"Error in RPC response: {response['error']}")

                if len(response["result"]) == 0:
                    raise Exception("Something is going on here... no logs found...")
                
                rpcs.append(rpc)

            except Exception as e:
                print("Removing RPC: ", rpc, e)

        final_configs.append(
            {
                "name": config["name"],
                "contract": config["contract"],
                "topics": config["topics"],
                "start_block": config["start_block"],
                "end_block": config["end_block"],
                "rpcs": rpcs,
            }
        )

    outfile = "./config/rpcs_config.yaml"
    with open(outfile, "w") as f:
        yaml.dump({"blockchains": final_configs}, f, default_flow_style=False, indent=2)
        print(f"RPC configurations generated and written to {outfile}.")
