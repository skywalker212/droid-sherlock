from abc import ABC, abstractmethod
import logging

from droid.test_framework import DeviceController

class PluginError(Exception):
    pass

class BasePlugin(ABC):
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)

    @abstractmethod
    def run(self, device: DeviceController) -> dict:
        pass