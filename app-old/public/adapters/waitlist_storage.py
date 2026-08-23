from django.conf import settings
from django.utils import timezone

from typing import Dict, List

import json, os


class WaitlistStorage:
    """Handles persistent storage for the waitlist using a JSON file."""
    
    def __init__(self):
        self.file_path = os.path.join(settings.BASE_DIR, 'private_data', 'waitlist.json')
        self._ensure_storage_exists()

    def _ensure_storage_exists(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump([], f)

    def get_all(self) -> List[Dict[str, str]]:
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []

    def add_entry(self, new_data: Dict[str, str]) -> bool:
        existing_data = self.get_all()
        email = new_data.get("email")
        
        if any(entry['email'] == email for entry in existing_data):
            return False

        existing_data.append(new_data)

        with open(self.file_path, 'w') as f:
            json.dump(existing_data, f, indent=4)
        
        return True