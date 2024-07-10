from typing import List, TypedDict

Config = TypedDict('Config', {'device_id': str, 'app_package': str, 'plugins': List[str]})