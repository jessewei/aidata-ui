"""Common library, AS

Modules:
    Description: Common module for AI data lib
    Last update: Jesse Wei, 2025/06/19
    is_in_container: Check if the code is running in a container
    AiDataApp: AiData Application class
    main: Entry point test for the odplib application
"""

import os
from odplib.cfg_lib import cfg_apps
from odplib import log_config


def is_in_container():
    """
    Check if the current environment is a container.

    This function determines if the current environment is a container by checking
    for the presence of the "container" keyword in the environment variables.

    Returns:
      bool: True if the environment is a container, False otherwise.
    """
    # path = '/proc/self/cgroup'
    # return (
    #     os.path.exists('/.dockerenv') or
    #     os.path.isfile(path) and any('docker' in line for line in open(path))
    # )
    return True if "container" in os.environ else False


class AiDataApp:
    """AI Data Application class

    Attributes:
        name (str): application name
        logger (logging.Logger): application logger
        version (str): application version
        description (str): application description
        list (list): list of applications
        include (list): list of included applications
    """

    def __init__(self, name):
        self.name = name
        self.app_cfg = self.get_app_cfg()
        self.app_log_cfg = self.app_cfg.get("logging", {})

        # initialize the logger by apps.cfg
        level = self.app_log_cfg.get("level", None)
        format = self.app_log_cfg.get("format", None)
        base_log_folder = self.app_log_cfg.get("base_log_folder", None)
        self.logger = log_config.setup_logger(name, level, format, base_log_folder)
        self.logger.debug(f"ODPLIB:: Initializing {name} application")

    def get_name(self):
        return self.name

    def get_logger(self):
        return self.logger

    def get_version(self):
        return cfg_apps["application"]["version"]

    def get_description(self):
        return cfg_apps["application"]["description"]

    def get_list(self):
        return cfg_apps["application"]["list"]

    def get_include(self):
        return cfg_apps["application"]["include"]

    def get_include_name(self, idx):
        return cfg_apps["application"]["include"][idx]["name"]

    def get_include_cfg_filename(self, idx):
        return cfg_apps["application"]["include"][idx]["cfg_filename"]

    def get_app_cfg(self):
        return cfg_apps.get(self.name, {})


def main() -> None:
    """Entry point test for the ailib application.
    Usage: uv run hi
    """
    ai_app = AiDataApp("ailib")
    print(f"Hello from {ai_app.get_name()}!")
