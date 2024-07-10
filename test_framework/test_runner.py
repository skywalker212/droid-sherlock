from .emulator_controller import EmulatorController
from .network_manager import NetworkManager
from .app_analyzer import AppAnalyzer
import importlib

class TestRunner:
    def __init__(self, config):
        self.config = config
        self.device = EmulatorController(config['device_id'])
        self.network = NetworkManager(self.device)
        self.plugins = self.load_plugins()
        self.analyzer = AppAnalyzer(self.device, self.plugins)

    def load_plugins(self):
        plugins = []
        for plugin_name in self.config.get('plugins', []):
            module = importlib.import_module(f"plugins.{plugin_name}")
            plugin_class = getattr(module, f"{plugin_name.capitalize()}Plugin")
            plugins.append(plugin_class())
        return plugins

    def run(self):
        # Test offline launch
        self.network.disable_network()
        self.device.launch_app(self.config['app_package'])
        offline_results = self.analyzer.analyze_behavior()

        # Test online behavior
        self.network.enable_network()
        online_results = self.analyzer.analyze_behavior()

        # Generate report
        print("Offline behavior:")
        print(offline_results)
        print("\nOnline behavior:")
        print(online_results)