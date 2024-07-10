from abc import ABC, abstractmethod
from droid.test_framework import DeviceController

class BasePlugin(ABC):
    @abstractmethod
    def run_checks(self, device: DeviceController) -> dict:
        pass