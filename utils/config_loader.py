import yaml
from pathlib import Path
from typing import Any, Dict, Optional

class Config:
    """ 
        Making container to access configuration easily 
    """

    def __init__(self, config_dict):
        self.config_dict = config_dict

    def get(self, key_path, default=None):
        """ Get config values from dot notation """

        keys = key_path.split(".")
        value = self._config

        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        return value
    
    def __get_item__(self, key):
        return self._config[key]

    def __contains__(self, key):
        return key in self._config

    def raw(self):
        return self._config


_config = None


def load_config(config_path=None):
    """Load configuration from config.yaml file"""

    global _config

    if config_path is None:
        utils_dir = Path(__file__).parent
        project_root = utils_dir.parent
        config_path = project_root / 'config' / 'config.yaml'
    else:
        config_path = Path(config_path)
        
        # When the provided fie path not exist
        if not config_path.exists():
            utils_dir = Path(__file__).parent
            project_root = utils_dir.parent
            config_path = project_root / config_path

    if not config_path.exists():
        raise FileNotFoundError(
            f"Config file not found : {config_path} \n"
            f"Current working directory  : {Path.pwd} "
        )

    with open(config_path, "r") as f:
        config_dict = yaml.safe_load(f)
    _config = Config(config_dict)

    return _config


def get_config():
    """
        This function goes to 
        - Get the global config instance
        - Load config on first call
        - Return config instance
    """
    global _config
    if _config is None:
        _config = load_config()

    return _config


def reload_config(config_path):
    global _config
    _config = None
    return load_config(config_path)
