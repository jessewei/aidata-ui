"""Configuration library, AS

Modules:
    Description: Configuration module for odplib
    Last update: Jesse Wei, 2025/02/13
    Depenedencies: toml, pathlib, dotenv
    cfg_apps: Configuration from application.toml
"""

import toml
from pathlib import Path

# Load config
CONFIG_PATH = Path(__file__).parent.parent.parent
CONFIG_FILE = Path(CONFIG_PATH) / "application.toml"


def merge_toml_includes(base_config, base_path):
    for include in base_config.get("application", {}).get("include", []):
        for filename in include.get("cfg_filename", []):
            include_path = base_path / filename
            try:
                include_config = toml.load(include_path)
                base_config.update(include_config)  # Merge included config
            except FileNotFoundError:
                raise RuntimeError(f"Included configuration file not found: {include_path}")
            except toml.TomlDecodeError as e:
                raise RuntimeError(f"Error parsing included TOML file {include_path}: {e}")
    return base_config


try:
    cfg_apps = toml.load(CONFIG_FILE)
except FileNotFoundError:
    raise RuntimeError(f"Configuration file not found: {CONFIG_FILE}")
except toml.TomlDecodeError as e:
    raise RuntimeError(f"Error parsing TOML file: {e}")

cfg_apps = merge_toml_includes(cfg_apps, CONFIG_PATH)
