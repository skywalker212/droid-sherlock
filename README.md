# DroidSherlock

Android app behavior detective.

## Features

- Automated testing of Android apps in online and offline scenarios
- AI-powered image analysis for UI consistency checks
- Natural Language Processing for text and error message analysis
- Anomaly detection to identify unusual app behaviors
- Extensible plugin system for custom app-specific checks
- Support for both emulators and real Android devices

## Prerequisites

- macOS, Linux, or Windows
- Python 3.7+
- Android SDK and ADB
- Android Emulator or physical Android device

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
   - Enable Developer Options on your Android device:
     - Go to Settings > About Phone
     - Tap "Build Number" 7 times to enable Developer Options
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

### Finding the App Package Name

1. If you know the app's name but not its package name:
   - Install the app on your device
   - Run the following command:
     ```
     adb shell pm list packages | grep "app_name"
     ```
     Replace "app_name" with part of your app's name.

2. If the app is currently open on the device:
   - Run the following command:
     ```
     adb shell dumpsys window | grep -E 'mCurrentFocus|mFocusedApp'
     ```
   - Look for a line like:
     ```
     mCurrentFocus=Window{12345 u0 com.example.app/com.example.app.MainActivity}
     ```
     Here, `com.example.app` is the package name.

3. For pre-installed system apps:
   ```
   adb shell pm list packages -s
   ```

4. For third-party installed apps:
   ```
   adb shell pm list packages -3
   ```

### Configuration

Copy `configs/default_config.yaml` to `configs/your_app_config.yaml`. Once you have the device ID and app package name, update your configuration file (`configs/your_app_config.yaml`) with these values:

```yaml
device_id: "your_device_id_here"
app_package: "com.example.app/com.example.app.MainActivity"
```

Replace `your_device_id_here` with the actual device ID, and update the `app_package` with your app's package name and main activity.

## Running Tests

1. Start your Android emulator or connect a physical device

2. Run the test suite:
   ```
   python main.py --config configs/your_app_config.yaml
   ```

## Extending droid-sherlock

### Adding Custom Plugins

1. Create a new file in the `plugins/` directory, e.g., `my_custom_plugin.py`
2. Implement your plugin class, extending `BasePlugin`
3. Add your plugin to the configuration file

Example:
```python
from plugins.base_plugin import BasePlugin

class MyCustomPlugin(BasePlugin):
    def run_checks(self, device):
        # Implement your custom checks here
        return {"my_custom_check": "result"}
```

## Interpreting Results

droid-sherlock provides a comprehensive report including:
- Screenshot analysis
- Text sentiment analysis
- Custom plugin results
- Anomaly detection findings

Review the console output for detailed insights into your app's behavior.