# DroidSherlock

Android app behavior detective. Uncover quirks and anomalies with in your app with automation.

## Features

- Automated testing of Android apps
- Extensible plugin system for custom app-specific checks
- Support for both emulators and real Android devices
- Comprehensive logging and reporting
- Efficient artifact management

## Prerequisites

- macOS, Linux, or Windows
- Python 3.7+
- Android SDK and ADB (Android Debug Bridge)
- Android Emulator or physical Android device

## Project Structure

```
droid-sherlock/
│
├── main.py                 # Entry point for the test framework
│
├── droid/
│   ├── __init__.py
│   ├── types.py            # Configuration and custom type definitions
│   │
│   ├── test_framework/     # Core framework components
│   │   ├── __init__.py
│   │   ├── device_controller.py
│   │   ├── app_analyzer.py
│   │   └── test_runner.py
│   │
│   ├── plugins/            # Custom app-specific plugins
│   │   ├── __init__.py
│   │   ├── base_plugin.py
│   │   └── example_plugin.py
│   │
│   └── test_cases/         # Test case definitions
│       ├── __init__.py
│       ├── base_test.py
│       ├── example_test.py
│       └── network_test.py
│
├── configs/                # Configuration files
│   ├── default_config.yaml
│   └── example_config.yaml
│
├── requirements.txt        # Python dependencies
│
├── .gitignore              # Git ignore file
│
└── README.md               # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/droid-sherlock.git
   cd droid-sherlock
   ```

2. Set up a virtual environment:
   ```
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install required packages:
   ```
   pip install -r requirements.txt
   ```

4. Ensure Android SDK platform-tools are in your PATH.

## Connecting Devices and Obtaining App Info

### Connecting to Emulator/Real Device

1. **For Emulator:**
   - Launch Android Studio
   - Open AVD Manager (Tools > AVD Manager)
   - Start your desired virtual device

2. **For Real Device:**
   - Enable Developer Options on your Android device
   - Enable USB Debugging in Developer Options
   - Connect your device to your computer via USB
   - Trust the computer if prompted on your device

### Getting the Device ID

1. Open a terminal/command prompt
2. Run the following command:
   ```
   adb devices
   ```
3. You should see output similar to:
   ```
   List of devices attached
   emulator-5554   device
   XXXXXXXX        device
   ```
   The alphanumeric string (e.g., `emulator-5554` or `XXXXXXXX`) is your device ID.

### Finding the App Package and Activity Names

1. If the app is currently open on the device:
   - Run the following command:
     ```
     adb shell dumpsys window | grep -E 'mCurrentFocus|mFocusedApp'
     ```
   - Look for a line like:
     ```
     mCurrentFocus=Window{12345 u0 com.example.app/com.example.app.MainActivity}
     ```
     Here, `com.example.app` is the package name and `com.example.app.MainActivity` is the activity name.

2. For more methods to find package names, refer to Android documentation or use tools like `aapt`.

## Configuration

1. Copy `configs/default_config.yaml` to `configs/your_app_config.yaml`.
2. Update your configuration file with the device ID, app package, and activity:

```yaml
device_id: "your_device_id_here"
app_package: "com.example.app"
app_activity: "com.example.app.MainActivity"
plugins:
  - example_plugin
test_cases:
  - example_test
metadata:
  version: "1.0"
```

## Running Tests

1. Ensure your Android emulator is running or physical device is connected.

2. Run the test suite:
   ```
   python main.py --config configs/your_app_config.yaml
   ```

3. Optional: Use the `--verbose` flag for more detailed output:
   ```
   python main.py --config configs/your_app_config.yaml --verbose
   ```

## Extending droid

### Adding Custom Plugins

1. Create a new file in the `droid/plugins/` directory, e.g., `my_custom_plugin.py`
2. Implement your plugin class, extending `BasePlugin`
3. Add your plugin to the configuration file

Example:
```python
from droid.plugins.base_plugin import BasePlugin

class MyCustomPlugin(BasePlugin):
    def run(self, device):
        # Implement your custom checks here
        self.logger.info("Running custom plugin")
        return {"my_custom_check": "result"}
```

### Adding Custom Test Cases

1. Create a new file in the `droid/test_cases/` directory, e.g., `my_custom_test.py`
2. Implement your test case class, extending `BaseTest`
3. Add your test case to the configuration file

Example:
```python
from droid.test_cases.base_test import BaseTest

class MyCustomTest(BaseTest):
    def run(self, device, analyzer):
        self.logger.info("Running custom test")
        # Implement your test logic here
        return {"custom_test_result": "passed"}
```

## Interpreting Results

After running the tests, droid will generate a test report in the `test_results` directory. This report includes:
- Test case results
- Plugin check results
- Screenshots and other artifacts

Review the generated log file and test report for detailed insights into your app's behavior.