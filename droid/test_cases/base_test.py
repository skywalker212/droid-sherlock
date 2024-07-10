from abc import ABC, abstractmethod
import logging

from droid.test_framework import DeviceController, AppAnalyzer

class BaseTest(ABC):
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)

    @abstractmethod
    def run(self, device: DeviceController, analyzer: AppAnalyzer) -> dict:
        pass