import subprocess
import logging
import time
from typing import Optional

from droid.types import Configuration

class DeviceControllerError(Exception):
    pass

class DeviceController:
    def __init__(self, config: Configuration) -> None:
        self.device_id = config.device_id
        self.config = config
        self.logger = logging.getLogger(__name__)

    def execute_command(self, command: str) -> str:
        full_command = f"adb -s {self.device_id} {command}"
        try:
            self.logger.debug(f"Executing command: {full_command}")
            result = subprocess.run(full_command, shell=True, check=True, capture_output=True, text=True)
            self.logger.debug(f"Command output: {result.stdout}")
            return result.stdout
        except subprocess.CalledProcessError as e:
            error_msg = f"Error executing command: {full_command}\nError message: {e.stderr}"
            self.logger.error(error_msg)
            raise DeviceControllerError(error_msg)

    def launch_app(self, package_name: str, activity_name: str) -> None:
        try:
            self.execute_command(f"shell am start -n {package_name}/{activity_name}")
            self.logger.info(f"Launched app: {package_name}/{activity_name}")
        except DeviceControllerError as e:
            raise DeviceControllerError(f"Failed to launch app: {str(e)}")

    def force_stop_app(self, package_name: str) -> None:
        try:
            self.execute_command(f"shell am force-stop {package_name}")
            self.logger.info(f"Force stopped app: {package_name}")
        except DeviceControllerError as e:
            raise DeviceControllerError(f"Failed to force stop app: {str(e)}")

    def get_current_activity(self) -> str:
        try:
            return self.execute_command("shell dumpsys activity activities | grep mResumedActivity")
        except DeviceControllerError as e:
            raise DeviceControllerError(f"Failed to get current activity: {str(e)}")

    def capture_screenshot(self, filename: str) -> None:
        try:
            self.execute_command(f"shell screencap -p /sdcard/{filename}")
            self.execute_command(f"pull /sdcard/{filename} {self.config.run_dir}")
            self.execute_command(f"shell rm /sdcard/{filename}")
            self.logger.info(f"Captured screenshot: {filename}")
        except DeviceControllerError as e:
            raise DeviceControllerError(f"Failed to capture screenshot: {str(e)}")

    def is_screen_on(self) -> bool:
        try:
            result = self.execute_command("shell dumpsys power | grep 'Display Power: state='")
            return "ON" in result
        except DeviceControllerError as e:
            raise DeviceControllerError(f"Failed to check screen state: {str(e)}")

    def unlock_screen(self) -> None:
        try:
            if not self.is_screen_on():
                self.execute_command("shell input keyevent 26")  # Power button
            self.execute_command("shell input keyevent 82")  # Menu button to unlock
            self.logger.info("Unlocked device screen")
        except DeviceControllerError as e:
            raise DeviceControllerError(f"Failed to unlock screen: {str(e)}")

    def clear_app_data(self, package_name: str) -> None:
        try:
            self.execute_command(f"shell pm clear {package_name}")
            self.logger.info(f"Cleared app data: {package_name}")
        except DeviceControllerError as e:
            raise DeviceControllerError(f"Failed to clear app data: {str(e)}")

    def install_app(self, apk_path: str) -> None:
        try:
            self.execute_command(f"install {apk_path}")
            self.logger.info(f"Installed app from: {apk_path}")
        except DeviceControllerError as e:
            raise DeviceControllerError(f"Failed to install app: {str(e)}")

    def uninstall_app(self, package_name: str) -> None:
        try:
            self.execute_command(f"uninstall {package_name}")
            self.logger.info(f"Uninstalled app: {package_name}")
        except DeviceControllerError as e:
            raise DeviceControllerError(f"Failed to uninstall app: {str(e)}")

    def disable_network(self) -> None:
        try:
            self.execute_command("shell svc wifi disable")
            self.execute_command("shell svc data disable")
            self.logger.info("Disabled network connections")
        except DeviceControllerError as e:
            raise DeviceControllerError(f"Failed to disable network: {str(e)}")

    def enable_network(self) -> None:
        try:
            self.execute_command("shell svc wifi enable")
            self.execute_command("shell svc data enable")
            self.logger.info("Enabled network connections")
        except DeviceControllerError as e:
            raise DeviceControllerError(f"Failed to enable network: {str(e)}")

    def get_network_state(self) -> str:
        try:
            wifi_state = self.execute_command("shell settings get global wifi_on").strip()
            data_state = self.execute_command("shell settings get global mobile_data").strip()
            return f"WiFi: {wifi_state}, Mobile Data: {data_state}"
        except DeviceControllerError as e:
            raise DeviceControllerError(f"Failed to get network state: {str(e)}")

    def get_device_info(self) -> str:
        try:
            manufacturer = self.execute_command("shell getprop ro.product.manufacturer").strip()
            model = self.execute_command("shell getprop ro.product.model").strip()
            android_version = self.execute_command("shell getprop ro.build.version.release").strip()
            return f"{manufacturer} {model} (Android {android_version})"
        except DeviceControllerError as e:
            raise DeviceControllerError(f"Failed to get device info: {str(e)}")

    def wait_for_device(self, timeout: int = 60) -> None:
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                self.execute_command("shell echo 'Device ready'")
                self.logger.info("Device is ready")
                return
            except DeviceControllerError:
                time.sleep(1)
        raise DeviceControllerError(f"Device not ready after {timeout} seconds")