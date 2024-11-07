# project_forge/core/config.py
import os
import yaml
from typing import Dict, Any
from ..cli.colors import Colors
from ..constants.defaults import DEFAULT_CONFIG

class ConfigManager:
    """Configuration management for project settings"""
    
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file or create default"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    config = yaml.safe_load(f)
                    # Merge with defaults to ensure all required settings exist
                    return {**DEFAULT_CONFIG, **config}
            return DEFAULT_CONFIG.copy()
        except Exception as e:
            print(Colors.error(f"Error loading config: {e}"))
            return DEFAULT_CONFIG.copy()

    def save_config(self) -> None:
        """Save current configuration to file"""
        try:
            with open(self.config_path, 'w') as f:
                yaml.dump(self.config, f, default_flow_style=False)
        except Exception as e:
            print(Colors.error(f"Error saving configuration: {e}"))
