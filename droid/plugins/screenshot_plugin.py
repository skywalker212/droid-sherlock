from abc import ABC, abstractmethod
import logging
import time
import os

from droid.plugins.base_plugin import BasePlugin, PluginError
from droid.test_framework import DeviceController

class ScreenShotError(PluginError):
    pass

class ScreenShotPlugin(BasePlugin):
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)

    def run(self, device: DeviceController) -> dict:
        try:
            result = {}
            path = self._capture_screenshot(device)
            result['screenshot'] = path
            return result
        except Exception as e:
            self.logger.error(f"Failed to capture screenshot: {str(e)}")
            raise ScreenShotError(f"Failed to capture screenshot: {str(e)}")

    def _capture_screenshot(self, device: DeviceController) -> str:
        screenshot_file = f"screenshot_{int(time.time())}.png"
        device.capture_screenshot(screenshot_file)
        full_path = os.path.join(device.config.run_dir, screenshot_file)
        self.logger.info(f"Screenshot captured: {full_path}")
        return full_path
