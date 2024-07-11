import argparse
import yaml
import sys
from typing import Any
from droid.test_framework.test_runner import TestRunner, TestRunnerError
from droid.types import Configuration

def load_config(config_file: str) -> Configuration:
    try:
        with open(config_file, 'r') as f:
            config_dict = yaml.safe_load(f)
        return Configuration(**config_dict)
    except FileNotFoundError:
        print(f"Error: Configuration file '{config_file}' not found.")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error: Invalid YAML in configuration file: {e}")
        sys.exit(1)
    except TypeError as e:
        print(f"Error: Invalid configuration structure: {e}")
        sys.exit(1)

def main() -> None:
    parser = argparse.ArgumentParser(description="Android App Network Behavior Test")
    parser.add_argument("--config", default="configs/example_config.yaml", help="Path to the configuration file")
    parser.add_argument("--verbose", action="store_true", help="Increase output verbosity")
    parser.add_argument("--test-cases", nargs='+', help="Specify additional test cases to run")
    parser.add_argument("--plugins", nargs='+', help="Specify additional plugins to use")
    args: Any = parser.parse_args()

    try:
        config = load_config(args.config)
        
        # Add command-line specified test cases and plugins
        if args.test_cases:
            config.test_cases.extend(args.test_cases)
        if args.plugins:
            config.plugins.extend(args.plugins)
        
        runner = TestRunner(config, verbose=args.verbose)
        runner.run()
    except TestRunnerError as e:
        print(f"TestRunner error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()