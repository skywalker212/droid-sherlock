import subprocess
import logging

from droid.types import Configuration

class DeviceController:
    def __init__(self, config: Configuration) -> None:
        self.device_id = config.device_id
        self.config = config
        self.logger = logging.getLogger(__name__)

    def execute_command(self, command: str) -> str:
        full_command = f"adb -s {self.device_id} {command}"
        try:
            result = subprocess.run(full_command, shell=True, check=True, capture_output=True, text=True)
            logging.info(result.stdout)
            return result.stdout
        except subprocess.CalledProcessError as e:
            err = "Error executing command: {}\nError message: {}".format(full_command, e.stderr)
            logging.error(err)
            raise e

    def launch_app(self, package_name: str) -> bool:
        return self.execute_command(f"shell am start -n {package_name}")

    def force_stop_app(self, package_name: str) -> bool:
        return self.execute_command(f"shell am force-stop {package_name}")

    def get_current_activity(self) -> bool:
        return self.execute_command("shell dumpsys activity activities | grep mResumedActivity")

    def capture_screenshot(self, filename: str) -> None:
        self.execute_command(f"shell screencap -p /sdcard/{filename}")
        self.execute_command(f"pull /sdcard/{filename} {self.config.run_dir}")
        self.execute_command(f"shell rm /sdcard/{filename}")

    def is_screen_on(self) -> bool:
        result = self.execute_command("shell dumpsys power | grep 'Display Power: state='")
        return "ON" in result if result else False

    def unlock_screen(self) -> None:
        if not self.is_screen_on():
            self.execute_command("shell input keyevent 26")  # Power button
        self.execute_command("shell input keyevent 82")  # Menu button to unlock

    def clear_app_data(self, package_name: str) -> str:
        return self.execute_command(f"shell pm clear {package_name}")

    def install_app(self, apk_path: str) -> str:
        return self.execute_command(f"install {apk_path}")

    def uninstall_app(self, package_name: str) -> str:
        return self.execute_command(f"uninstall {package_name}")

    def disable_network(self) -> None:
        self.execute_command("shell svc wifi disable")
        self.execute_command("shell svc data disable")

    def enable_network(self) -> None:
        self.execute_command("shell svc wifi enable")
        self.execute_command("shell svc data enable")

    def get_network_state(self) -> str:
        wifi_state = self.execute_command("shell settings get global wifi_on")
        data_state = self.execute_command("shell settings get global mobile_data")
        return f"WiFi: {wifi_state.strip()}, Mobile Data: {data_state.strip()}"

    def get_device_info(self) -> str:
        manufacturer = self.execute_command("shell getprop ro.product.manufacturer").strip()
        model = self.execute_command("shell getprop ro.product.model").strip()
        android_version = self.execute_command("shell getprop ro.build.version.release").strip()
        return f"{manufacturer} {model} (Android {android_version})"