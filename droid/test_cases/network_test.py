import time 

from .base_test import BaseTest
from droid.test_framework import DeviceController, AppAnalyzer

class NetworkTest(BaseTest):
    def run(self, device: DeviceController, analyzer: AppAnalyzer):
        results = {}
        app_package = device.config.app_package

        self.logger.info("Testing offline behavior...")
        device.disable_network()
        time.sleep(2)  # Wait for network to fully disable
        
        self.logger.info("Launching app in offline mode...")
        device.launch_app(app_package)
        time.sleep(5)  # Wait for app to stabilize
        
        results['offline'] = analyzer.analyze_behavior()
        
        self.logger.info("Closing app...")
        device.force_stop_app(app_package)
        time.sleep(2)  # Wait for app to fully close

        self.logger.info("Enabling network...")
        device.enable_network()
        time.sleep(5)  # Wait for network to fully enable and stabilize
        
        self.logger.info("Launching app in online mode...")
        device.launch_app(app_package)
        time.sleep(5)  # Wait for app to stabilize
        
        results['online'] = analyzer.analyze_behavior()

        return results