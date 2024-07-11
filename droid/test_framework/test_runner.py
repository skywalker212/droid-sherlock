import importlib
import os
import logging
import sys
from typing import List, Type
from .device_controller import DeviceController, DeviceControllerError
from .app_analyzer import AppAnalyzer, AppAnalyzerError
from droid.types import Configuration
from droid.plugins import BasePlugin
from droid.test_cases import BaseTest

class TestRunnerError(Exception):
    pass

class TestRunner:
    def __init__(self, config: Configuration, verbose: bool) -> None:
        self.config = config
        self._setup_logging(verbose)
        try:
            self.device = self._initialize_device_controller()
            self.device.wait_for_device()
            self.plugins = self._load_plugins()
            self.analyzer = AppAnalyzer(self.device, self.plugins)
            self.test_cases = self._load_test_cases()
        except Exception as e:
            self.logger.error(f"Error during TestRunner initialization: {str(e)}")
            raise TestRunnerError(f"TestRunner initialization failed: {str(e)}")

    def _setup_logging(self, verbose: bool) -> None:
        log_file = os.path.join(self.config.run_dir, "test_run.log")
        file_handler = logging.FileHandler(filename=log_file)
        handlers = [file_handler]
        if verbose:
            stdout_handler = logging.StreamHandler(stream=sys.stdout)
            handlers.append(stdout_handler)
        logging.basicConfig(
            level=logging.INFO, 
            format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
            handlers=handlers
        )
        self.logger = logging.getLogger(__name__)

    def _initialize_device_controller(self) -> DeviceController:
        try:
            return DeviceController(self.config)
        except Exception as e:
            raise TestRunnerError(f"Failed to initialize DeviceController: {str(e)}")

    def _load_plugins(self) -> List[BasePlugin]:
        return self._load_classes('plugins', BasePlugin)

    def _load_test_cases(self) -> List[BaseTest]:
        return self._load_classes('test_cases', BaseTest)

    def _load_classes(self, module_type: str, base_class: Type) -> List:
        classes = []
        for name in getattr(self.config, module_type):
            try:
                module = importlib.import_module(f"droid.{module_type}.{name}")
                class_objects = [
                    obj for obj in module.__dict__.values()
                    if isinstance(obj, type) and issubclass(obj, base_class) and obj != base_class
                ]
                if class_objects:
                    classes.append(class_objects[-1]())
                    self.logger.info(f"Loaded {module_type[:-1]}: {class_objects[-1].__name__}")
                else:
                    self.logger.warning(f"No {module_type[:-1]} class found in {name}")
            except ImportError as e:
                self.logger.error(f"Failed to load {module_type[:-1]} {name}: {str(e)}")
        return classes

    def run(self) -> None:
        try:
            self.logger.info(f"Starting test run {self.config.run_id}")
            self.logger.info(f"Device info: {self.device.get_device_info()}")
            
            results = {}
            for test_case in self.test_cases:
                test_name = test_case.__class__.__name__
                self.logger.info(f"Running test case: {test_name}")
                try:
                    self.device.wait_for_device()
                    test_result = test_case.run(self.device, self.analyzer)
                    results[test_name] = test_result
                    self._save_artifacts(test_name, test_result)
                except (DeviceControllerError, AppAnalyzerError) as e:
                    self.logger.error(f"Error in test case {test_name}: {str(e)}")
                    results[test_name] = {"error": str(e)}
                except Exception as e:
                    self.logger.error(f"Unexpected error in test case {test_name}: {str(e)}")
                    results[test_name] = {"error": f"Unexpected error: {str(e)}"}

            self._generate_report(results)
            self.logger.info(f"Test run {self.config.run_id} completed. Results saved in {self.config.run_dir}")
        except Exception as e:
            self.logger.error(f"Test run failed: {str(e)}")
            raise TestRunnerError(f"Test run failed: {str(e)}")
        finally:
            self.cleanup()

    def _save_artifacts(self, test_name: str, test_result: dict) -> None:
        artifacts_to_save = []
        
        def collect_artifacts(result: dict):
            for key, value in result.items():
                if isinstance(value, str) and os.path.isfile(value):
                    artifacts_to_save.append((key, value))
                elif isinstance(value, dict):
                    collect_artifacts(value)

        collect_artifacts(test_result)

        if artifacts_to_save:
            artifact_dir = os.path.join(self.config.run_dir, test_name)
            os.makedirs(artifact_dir, exist_ok=True)
            
            for key, value in artifacts_to_save:
                new_path = os.path.join(artifact_dir, os.path.basename(value))
                os.rename(value, new_path)
                *path, last_key = key.split('.')
                current = test_result
                for k in path:
                    current = current[k]
                current[last_key] = new_path

            self.logger.info(f"Saved {len(artifacts_to_save)} artifacts for test case: {test_name}")
        else:
            self.logger.info(f"No artifacts to save for test case: {test_name}")

    def _generate_report(self, results: dict) -> None:
        report_path = os.path.join(self.config.run_dir, "test_report.txt")
        with open(report_path, 'w') as f:
            f.write(f"=== Test Results for Run {self.config.run_id} ===\n")
            f.write(f"Device: {self.device.get_device_info()}\n")
            f.write(f"App Package: {self.config.app_package}\n")
            f.write(f"App Activity: {self.config.app_activity}\n\n")
            for test_name, test_result in results.items():
                f.write(f"\n{test_name}:\n")
                for key, value in test_result.items():
                    f.write(f"  {key}: {value}\n")
        self.logger.info(f"Test report generated: {report_path}")

    def cleanup(self) -> None:
        try:
            self.logger.info("Performing test run cleanup")
            self.device.enable_network()
            self.device.force_stop_app(self.config.app_package)
        except Exception as e:
            self.logger.error(f"Error during cleanup: {str(e)}")