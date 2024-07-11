from .base_test import BaseTest, TestError
from droid.test_framework import DeviceController, AppAnalyzer

class ExampleTest(BaseTest):
    def run(self, device: DeviceController, analyzer: AppAnalyzer):
        try:
            self.logger.info("Example test successful")
            return {"example_test": "passed"}
        except Exception as e:
            self.logger.error(f"Example test failed: {str(e)}")
            raise TestError(f"Example test failed: {str(e)}")