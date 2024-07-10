# In droid/test_runner.py

import importlib
import os
import logging
from typing import List, Type
from .device_controller import DeviceController
from .app_analyzer import AppAnalyzer
from droid.types import Configuration
from droid.plugins import BasePlugin
from droid.test_cases import BaseTest

class TestRunner:
    def __init__(self, config: Configuration) -> None:
        self.config = config
        self._setup_logging()
        self.device = self._initialize_device_controller()
        self.plugins = self._load_plugins()
        self.analyzer = AppAnalyzer(self.device, self.plugins)
        self.test_cases = self._load_test_cases()

    def _setup_logging(self):
        log_file = os.path.join(self.config.run_dir, "test_run.log")
        logging.basicConfig(filename=log_file, level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

    def _initialize_device_controller(self) -> DeviceController:
        return DeviceController(self.config)

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
        self.logger.info(f"Starting test run on device: {self.device.get_device_info()}")
        
        results = {}
        for test_case in self.test_cases:
            test_name = test_case.__class__.__name__
            self.logger.info(f"Running test case: {test_name}")
            test_result = test_case.run(self.device, self.analyzer)
            results[test_name] = test_result
            
            self._save_artifacts(test_name, test_result)

        self._generate_report(results)

    def _save_artifacts(self, test_name: str, test_result: dict) -> None:
        artifacts = []
        objs = []
        for key, val in test_result.items():
            if isinstance(val, str) and os.path.isfile(val):
                artifacts.append((key, val))
            elif isinstance(val, dict):
                objs.append(val)
        if len(artifacts) > 0:
            artifact_dir = os.path.join(self.config.run_dir, test_name)
            os.makedirs(artifact_dir, exist_ok=True)
        for key, value in artifacts:
            new_path = os.path.join(artifact_dir, os.path.basename(value))
            os.rename(value, new_path)
            test_result[key] = new_path
        for obj in objs:
            self._save_artifacts(test_name, obj)

    def _generate_report(self, results: dict) -> None:
        report_path = os.path.join(self.config.run_dir, "test_report.txt")
        with open(report_path, 'w') as f:
            f.write("=== Test Results ===\n")
            for test_name, test_result in results.items():
                f.write(f"\n{test_name}:\n")
                for key, value in test_result.items():
                    f.write(f"  {key}: {value}\n")
        self.logger.info(f"Test report generated: {report_path}")