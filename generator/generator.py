from config.constants import Bridge
from utils.utils import CustomException, load_module


class Generator:
    CLASS_NAME = "Generator"

    def __init__(self, bridge: Bridge):
        self.bridge = bridge
        self.generator = self.load_generator()

    def load_generator(self):
        """Dynamically loads the generator for the specified bridge."""
        func_name = "load_generator"
        bridge_name = self.bridge.value

        try:
            module = load_module(f"generator.{bridge_name}.generator")
            decoder_class_name = f"{bridge_name.capitalize()}Generator"
            decoder_class = getattr(module, decoder_class_name)

            return decoder_class()
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME, func_name, f"Bridge {bridge_name} not supported"
            ) from e

    def generate_data(self):
        """Main generation logic."""

        self.generator.generate_cross_chain_data()
