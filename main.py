import argparse
import yaml
from test_framework.test_runner import TestRunner

def load_config(config_file):
    with open(config_file, 'r') as file:
        return yaml.safe_load(file)

def main():
    parser = argparse.ArgumentParser(description="Android App Network Behavior Test")
    parser.add_argument("--config", default="configs/default_config.yaml", help="Path to the configuration file")
    args = parser.parse_args()

    config = load_config(args.config)
    runner = TestRunner(config)
    runner.run()

if __name__ == "__main__":
    main()