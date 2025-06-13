import argparse

from config.constants import Bridge
from extractor.extractor import Extractor
from generator.generator import Generator
from repository.database import create_tables
from rpcs import generate_rpc_configs
from utils.utils import (CliColor, CustomException, build_log_message_2,
                         get_block_by_timestamp, get_enum_instance,
                         load_module, log_to_cli)


class Cli():
    CLASS_NAME = "Cli"

    def extract_data(args):
        blockchains = args.blockchains

        size = len(blockchains)
        bridge = get_enum_instance(Bridge, args.bridge)

        Cli.load_db_models(bridge)
        
        for idx, blockchain in enumerate(blockchains):
            start_block = get_block_by_timestamp(args.start_ts, blockchain)
            end_block = get_block_by_timestamp(args.end_ts, blockchain)

            generate_rpc_configs(blockchain)

            log_to_cli(
                build_log_message_2(
                    start_block,
                    end_block,
                    bridge,
                    blockchain,
                    f"{idx + 1}/{size} Starting extraction... ",
                )
            )

            try:
                log_to_cli(
                    build_log_message_2(
                        start_block,
                        end_block,
                        bridge,
                        blockchain,
                        "Loading contracts and ABIs...",
                    )
                )
                extractor = Extractor(bridge, blockchain, blockchains)
            except Exception as e:
                log_to_cli(
                    build_log_message_2(
                        start_block,
                        end_block,
                        bridge,
                        blockchain,
                        f"{idx + 1}/{size} Error: {e}",
                    ),
                    CliColor.ERROR,
                )
                return

            extractor.extract_data(
                start_block,
                end_block,
            )


    def generate_data(args):
        bridge = get_enum_instance(Bridge, args.bridge)

        Cli.load_db_models(bridge)

        generator = Generator(bridge)

        generator.generate_data()


    def cli():
        parser = argparse.ArgumentParser(description="Cross-chain Data Extraction Tool")
        subparsers = parser.add_subparsers(
            title="Actions", description="Available actions", dest="action"
        )

        # Extract action
        extract_parser = subparsers.add_parser(
            "extract", help="Extract data from blockchains"
        )
        extract_parser.add_argument(
            "--bridge",
            choices=[bridge.value for bridge in Bridge],
            required=True,
            help="Name of the bridge to analyze"
        )
        extract_parser.add_argument(
            "--start_ts", required=True, help="Start timestamp for extraction"
        )
        extract_parser.add_argument(
            "--end_ts", required=True, help="End timestamp for extraction"
        )
        extract_parser.add_argument(
            "--blockchains",
            choices=["ethereum", "arbitrum", "polygon", "avalanche", "base", "optimism", "bnb", "scroll", "linea", "gnosis", "ronin"],
            nargs="+",
            help="List of blockchains to extract data from"
        )

        extract_parser.set_defaults(func=Cli.extract_data)

        # Generate action
        generate_parser = subparsers.add_parser(
            "generate", help="Generate cross-chain transactions"
        )
        generate_parser.add_argument(
            "--bridge",
            choices=[bridge.value for bridge in Bridge],
            required=True,
            help="Name of the bridge"
        )
        generate_parser.set_defaults(func=Cli.generate_data)

        args = parser.parse_args()
        if args.action:
            args.func(args)
        else:
            parser.print_help()


    def load_db_models(bridge: Bridge):
        """Dynamically loads the database models for the specified bridge."""
        func_name = "load_db_models"
        bridge_name = bridge.value

        try:
            load_module(f"repository.common")
            load_module(f"repository.{bridge_name}")
            create_tables()
        except Exception as e:
            raise CustomException(
                Cli.CLASS_NAME, func_name, f"Bridge {bridge_name} not supported"
            )