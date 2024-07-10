import time

class AppAnalyzer:
    def __init__(self, device, plugins):
        self.device = device
        self.plugins = plugins

    def analyze_behavior(self):
        time.sleep(5)  # Wait for app to stabilize
        current_activity = self.device.get_current_activity()
        screenshot_file = f"screenshot_{int(time.time())}.png"
        self.device.capture_screenshot(screenshot_file)

        results = {
            "current_activity": current_activity.strip(),
            "screenshot": screenshot_file
        }

        for plugin in self.plugins:
            plugin_results = plugin.run_checks(self.device)
            results.update(plugin_results)

        return results