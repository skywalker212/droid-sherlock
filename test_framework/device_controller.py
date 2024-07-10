from abc import ABC, abstractmethod

class DeviceController(ABC):
    @abstractmethod
    def execute_command(self, command):
        pass

    @abstractmethod
    def launch_app(self, package_name):
        pass

    @abstractmethod
    def get_current_activity(self):
        pass

    @abstractmethod
    def capture_screenshot(self, filename):
        pass