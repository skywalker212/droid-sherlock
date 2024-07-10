import subprocess
from .device_controller import DeviceController

class EmulatorController(DeviceController):
    def __init__(self, device_id):
        self.device_id = device_id

    def execute_command(self, command):
        full_command = f"adb -s {self.device_id} {command}"
        return subprocess.check_output(full_command, shell=True).decode('utf-8')

    def launch_app(self, package_name):
        self.execute_command(f"shell am start -n {package_name}")

    def get_current_activity(self):
        return self.execute_command("shell dumpsys activity activities | grep mResumedActivity")

    def capture_screenshot(self, filename):
        self.execute_command(f"shell screencap -p /sdcard/{filename}")
        self.execute_command(f"pull /sdcard/{filename}")