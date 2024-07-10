import time
from typing import List
from .device_controller import DeviceController
from droid.plugins import BasePlugin

class AppAnalyzer:
    def __init__(self, device: DeviceController, plugins: List[BasePlugin]) -> None:
        self.device = device
        self.plugins = plugins

    def analyze_behavior(self) -> dict:
        time.sleep(5)  # Wait for app to stabilize
        screenshot_file = f"screenshot_{int(time.time())}.png"
        self.device.capture_screenshot(screenshot_file)

        results = {
            "screenshot": f"{self.device.config.run_dir}/{screenshot_file}"
        }

        for plugin in self.plugins:
            plugin_results = plugin.run(self.device)
            results.update(plugin_results)

        return results