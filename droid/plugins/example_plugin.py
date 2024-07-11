from .base_plugin import BasePlugin, PluginError
from droid.test_framework import DeviceController

class ExamplePlugin(BasePlugin):
    def run(self, _: DeviceController) -> dict:
        try:
            # Perform plugin checks
            self.logger.info("Example plugin check passed")
            return {"example_check": "passed"}
        except Exception as e:
            self.logger.error(f"Example plugin check failed: {str(e)}")
            raise PluginError(f"Example plugin check failed: {str(e)}")