import yaml
import os
from pathlib import Path
import warnings


def load_settings(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            settings_dict = yaml.safe_load(f)
    else:
        raise FileNotFoundError(f"Settings file '{file_path}' not found.")
    
    return settings_dict

class Map(dict):
    """A dictionary that supports dot notation recursively."""
    def __init__(self, data):
        # Convert nested dicts to Maps
        for key, value in data.items():
            if isinstance(value, dict):
                value = Map(value)
            self[key] = value

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(f"No setting named '{name}'")

# Initialize immediately
current_dir = Path(__file__).parent
filepath = current_dir.parent / "settings.yaml"
settings_dict = load_settings(filepath)
SETTINGS = Map(settings_dict)
