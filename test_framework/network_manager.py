class NetworkManager:
    def __init__(self, device):
        self.device = device

    def disable_network(self):
        self.device.execute_command("shell svc wifi disable")
        self.device.execute_command("shell svc data disable")

    def enable_network(self):
        self.device.execute_command("shell svc wifi enable")
        self.device.execute_command("shell svc data enable")

    def get_network_state(self):
        wifi_state = self.device.execute_command("shell settings get global wifi_on")
        data_state = self.device.execute_command("shell settings get global mobile_data")
        return f"WiFi: {wifi_state.strip()}, Mobile Data: {data_state.strip()}"