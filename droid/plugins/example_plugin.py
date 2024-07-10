from .base_plugin import BasePlugin

class ExamplePlugin(BasePlugin):
    def run(self, _) -> dict:
        self.logger.info("Example plugin check passed")
        return {"example_check": "passed"}