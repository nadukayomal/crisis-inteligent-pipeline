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
    """
    Force reload configuration from file.
    
    Useful for picking up config changes without restarting.
    
    Args:
        config_path: Path to config file
    
    Returns:
        New Config instance
    """

    global _config
    _config = None
    return load_config(config_path)


# common configurattion files

def get_default_provider():
    return get_config().get("providers.default", "openai")

def get_enable_providers():
    return get_config().get("providers.enabled", ['openai'])

def get_backoff_base():
    return get_config().get("retry.backoff.base_seconds", 0.5)

def get_backoff_jitter():
    return get_config().get("retry.backoff.jitter_factor", 0.25)

def get_default_temperature(task_type):
    """
    Get default temperature for task type.
    
    Args:
        task_type: Optional task type (extraction, classification, etc.)
    
    Returns:
        Temperature value
    """
    if task_type:
        temp = get_config().get(f"defaults.by_task.{task_type}.temperature")
        if temp is not None:
            return temp

    return get_config().get("default.temperature", 0.2)

def get_default_max_tokens(task_type = None):
    """
    Get default max_tokens for task type.
    
    Args:
        task_type: Optional task type
    
    Returns:
        Max tokens value
    """
    if task_type:
        max_tok = get_config().get(f"defaults.by_task.{task_type}.max_tokens")
        if max_tok is not None:
            return max_tok
    
    return get_config().get("defaults.max_tokens", 1000)

def is_logging_enabled():
    """Check if logging is enabled."""
    return get_config().get("logging.enabled", True)

def get_log_path() :
    """Get full path to log file."""
    log_dir = get_config().get("logging.output_dir", "logs")
    log_file = get_config().get("logging.output_file", "runs.csv")
    return Path(log_dir) / log_file

def should_auto_route_reasoning():
    """Check if automatic reasoning model routing is enabled."""
    return get_config().get("models.auto_routing", True)

def get_reasoning_techniques():
    """Get list of techniques that trigger reasoning model routing."""
    return get_config().get("models.reasoning_techniques", ["cot", "tot"])