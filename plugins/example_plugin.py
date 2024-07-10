from .base_plugin import BasePlugin

class ExamplePlugin(BasePlugin):
    def run_checks(self, device):
        # Implement app-specific checks here
        return {"example_check": "passed"}