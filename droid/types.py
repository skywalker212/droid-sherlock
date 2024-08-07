# In droid/types.py

from dataclasses import dataclass, field
from typing import List, Dict
import datetime
import os

@dataclass
class Configuration:
    device_id: str
    app_package: str
    app_activity: str
    plugins: List[str] = field(default_factory=list)
    test_cases: List[str] = field(default_factory=list)
    run_id: str = field(init=False)
    run_dir: str = field(init=False)
    start_time: datetime.datetime = field(init=False)
    metadata: Dict[str, str] = field(default_factory=dict)

    def __post_init__(self):
        self.start_time = datetime.datetime.now()
        self.run_id = self.start_time.strftime("%Y%m%d_%H%M%S")
        self.run_dir = os.path.join("test_results", self.run_id)
        if not self.device_id or not self.app_package or not self.app_activity:
            raise ValueError("device_id, app_package, and app_activity are required fields")
        os.makedirs(self.run_dir, exist_ok=True)