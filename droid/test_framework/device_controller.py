import subprocess

class DeviceController:
    def __init__(self, device_id: str) -> None:
        self.device_id = device_id

    def execute_command(self, command: str) -> str:
        full_command = f"adb -s {self.device_id} {command}"
        try:
            result = subprocess.run(full_command, shell=True, check=True, capture_output=True, text=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            err = "Error executing command: {}\nError message: {}".format(full_command, e.stderr)
            return err

    def launch_app(self, package_name: str) -> str:
        return self.execute_command(f"shell am start -n {package_name}")

    def get_current_activity(self) -> str:
        return self.execute_command("shell dumpsys activity activities | grep mResumedActivity")

    def capture_screenshot(self, filename: str) -> None:
        self.execute_command(f"shell screencap -p /sdcard/{filename}")
        self.execute_command(f"pull /sdcard/{filename}")
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

    def get_device_info(self) -> str:
        manufacturer = self.execute_command("shell getprop ro.product.manufacturer").strip()
        model = self.execute_command("shell getprop ro.product.model").strip()
        android_version = self.execute_command("shell getprop ro.build.version.release").strip()
        return f"{manufacturer} {model} (Android {android_version})"