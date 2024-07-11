import time
import os
from typing import List
import logging

from .device_controller import DeviceController
from droid.plugins import BasePlugin

class AppAnalyzerError(Exception):
    pass

class AppAnalyzer:
    def __init__(self, device: DeviceController, plugins: List[BasePlugin]) -> None:
        self.device = device
        self.plugins = plugins
        self.logger = logging.getLogger(__name__)

    def analyze_behavior(self) -> dict:
        try:
            self.logger.info("Starting app behavior analysis")
            self.device.wait_for_device()
            
            screenshot_file = self._capture_screenshot()
            
            results = {
                "screenshot": screenshot_file
            }

            plugin_results = self._run_plugins()
            results.update(plugin_results)

            self.logger.info("App behavior analysis completed successfully")
            return results

        except Exception as e:
            self.logger.error(f"App behavior analysis failed: {str(e)}")
            raise AppAnalyzerError(f"App behavior analysis failed: {str(e)}")

    def _capture_screenshot(self) -> str:
        try:
            screenshot_file = f"screenshot_{int(time.time())}.png"
            self.device.capture_screenshot(screenshot_file)
            full_path = os.path.join(self.device.config.run_dir, screenshot_file)
            self.logger.info(f"Screenshot captured: {full_path}")
            return full_path
        except Exception as e:
            self.logger.error(f"Failed to capture screenshot: {str(e)}")
            raise AppAnalyzerError(f"Failed to capture screenshot: {str(e)}")

    def _run_plugins(self) -> dict:
        plugin_results = {}
        for plugin in self.plugins:
            try:
                self.logger.info(f"Running plugin: {plugin.__class__.__name__}")
                result = plugin.run(self.device)
                plugin_results[plugin.__class__.__name__] = result
                self.logger.info(f"Plugin {plugin.__class__.__name__} completed successfully")
            except Exception as e:
                self.logger.error(f"Plugin {plugin.__class__.__name__} failed: {str(e)}")
                plugin_results[plugin.__class__.__name__] = {"error": str(e)}
        return plugin_results