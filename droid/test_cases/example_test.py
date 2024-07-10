from .base_test import BaseTest
from droid.test_framework import DeviceController, AppAnalyzer

class ExampleTest(BaseTest):
    def run(self, device: DeviceController, analyzer: AppAnalyzer):
        self.logger.info("Example test successful")
        return {"example_test": "passed"}