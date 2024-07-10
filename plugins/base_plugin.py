from abc import ABC, abstractmethod

class BasePlugin(ABC):
    @abstractmethod
    def run_checks(self, device):
        pass