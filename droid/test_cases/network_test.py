import time 

from .base_test import BaseTest, TestError
from droid.test_framework import DeviceController, AppAnalyzer

class NetworkTest(BaseTest):
    def run(self, device: DeviceController, analyzer: AppAnalyzer):
        try:
            results = {}
            app_package = device.config.app_package
            app_activity = device.config.app_activity

            self.logger.info("Testing offline behavior...")
            device.wait_for_device()
            device.unlock_screen()
            device.disable_network()
            time.sleep(2)  
            
            self.logger.info("Launching app in offline mode...")
            device.launch_app(app_package, app_activity)
            time.sleep(5)  
            
            results['offline'] = analyzer.analyze_behavior()
            
            self.logger.info("Closing app...")
            device.force_stop_app(app_package)
            time.sleep(2)  

            self.logger.info("Enabling network...")
            device.wait_for_device()
            device.enable_network()
            time.sleep(5)  
            
            self.logger.info("Launching app in online mode...")
            device.launch_app(app_package, app_activity)
            time.sleep(5)  
            
            results['online'] = analyzer.analyze_behavior()

            self.logger.info("Closing app...")
            device.force_stop_app(app_package)

            return results
        except Exception as e:
            self.logger.error(f"Network test failed: {str(e)}")
            raise TestError(f"Network test failed: {str(e)}")