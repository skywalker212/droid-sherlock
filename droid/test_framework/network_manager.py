from .device_controller import DeviceController

class NetworkManager:
    def __init__(self, device: DeviceController) -> None:
        self.device = device

    def disable_network(self) -> None:
        self.device.execute_command("shell svc wifi disable")
        self.device.execute_command("shell svc data disable")

    def enable_network(self) -> None:
        self.device.execute_command("shell svc wifi enable")
        self.device.execute_command("shell svc data enable")

    def get_network_state(self) -> str:
        wifi_state = self.device.execute_command("shell settings get global wifi_on")
        data_state = self.device.execute_command("shell settings get global mobile_data")
        return f"WiFi: {wifi_state.strip()}, Mobile Data: {data_state.strip()}"