import json
import os
import logging
from typing import Dict, Any

class ConfigManager:
    def __init__(self, config_dir: str):
        self.config_dir = config_dir
        self.configs = {}

    def load_config(self, filename: str) -> Dict[str, Any]:
        path = os.path.join(self.config_dir, filename)
        if not os.path.exists(path):
            logging.error(f"Config file {filename} not found in {self.config_dir}")
            raise FileNotFoundError(f"Config file {filename} not found in {self.config_dir}")
        try:
            with open(path, 'r') as f:
                config = json.load(f)
                self.validate_config(config)
                self.configs[filename] = config
                return config
        except json.JSONDecodeError as e:
            logging.error(f"Invalid JSON in config file {filename}: {e}")
            raise

    def validate_config(self, config: Dict[str, Any]):
        # Basic validation example: check required keys
        required_keys = ['connector_type', 'settings']
        for key in required_keys:
            if key not in config:
                raise ValueError(f"Config missing required key: {key}")

    def get_config(self, filename: str) -> Dict[str, Any]:
        return self.configs.get(filename)

    def list_configs(self) -> list:
        return list(self.configs.keys())
