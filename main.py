import argparse
import yaml
from droid.test_framework.test_runner import TestRunner
from droid.types import Configuration

def load_config(config_file: str) -> Configuration:
    with open(config_file, 'r') as f:
        config_dict = yaml.safe_load(f)
    return Configuration(**config_dict)

def main() -> None:
    parser = argparse.ArgumentParser(description="Android App Network Behavior Test")
    parser.add_argument("--config", default="configs/default_config.yaml", help="Path to the configuration file")
    args = parser.parse_args()

    config = load_config(args.config)
    runner = TestRunner(config)
    runner.run()

if __name__ == "__main__":
    main()