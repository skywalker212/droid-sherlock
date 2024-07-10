import importlib

from .device_controller import DeviceController
from .network_manager import NetworkManager
from .app_analyzer import AppAnalyzer
from droid.types import Config
from droid.plugins import BasePlugin

class TestRunner:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.device = self._initialize_device_controller()
        self.network = NetworkManager(self.device)
        self.plugins = self._load_plugins()
        self.analyzer = AppAnalyzer(self.device, self.plugins)

    def _initialize_device_controller(self) -> DeviceController:
        device_id = self.config['device_id']
        return DeviceController(device_id)

    def _load_plugins(self) -> BasePlugin:
        plugins = []
        for plugin_name in self.config.get('plugins', []):
            try:
                module = importlib.import_module(f"plugins.{plugin_name}")
                # Look for any class that ends with 'Plugin'
                plugin_classes = [obj for name, obj in module.__dict__.items() if name.endswith('Plugin') and isinstance(obj, type)]
                if plugin_classes:
                    plugins.append(plugin_classes[-1]())
                    print(f"Loaded plugin: {plugin_classes[-1].__name__}")
                else:
                    print(f"No plugin class found in {plugin_name}")
            except ImportError as e:
                print(f"Failed to load plugin {plugin_name}: {str(e)}")
        return plugins

    def run(self) -> None:
        print(f"Starting test run on device: {self.device.get_device_info()}")

        # Test offline launch
        print("Testing offline behavior...")
        self.network.disable_network()
        self.device.launch_app(self.config['app_package'])
        offline_results = self.analyzer.analyze_behavior()

        # Test online behavior
        print("Testing online behavior...")
        self.network.enable_network()
        online_results = self.analyzer.analyze_behavior()

        # Generate report
        self._generate_report(offline_results, online_results)

    def _generate_report(self, offline_results: dict, online_results: dict) -> None:
        print("\n=== Test Results ===")
        print("\nOffline behavior:")
        self._print_results(offline_results)
        print("\nOnline behavior:")
        self._print_results(online_results)

    def _print_results(self, results: dict) -> None:
        for key, value in results.items():
            print(f"{key}: {value}")