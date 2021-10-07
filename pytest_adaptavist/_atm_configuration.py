"""Read config parameters."""

from __future__ import annotations

import json
import os
from typing import Any

from adaptavist import Adaptavist


class ATMConfiguration:
    """Configuration class to read config parameters (either from env or from "global_config.json")."""

    def __init__(self):
        self.config = {}
        config_file_name = os.path.join("config", "global_config.json")
        if os.path.exists(os.path.abspath(config_file_name)):
            with open(config_file_name, "r", encoding="utf-8") as config_file:
                try:
                    self.config.update(json.load(config_file))
                except Exception as ex:
                    raise ValueError(f'Failed to load config from file "{config_file}"!', ex) from ex

    def get(self, key: str, default: Any = None) -> Any:
        """Get value either from environment or from config file."""

        if key.lower().startswith("cfg_"):
            return self.config.get(key) or default
        return os.environ.get(key) or os.environ.get(key.upper()) or self.config.get("cfg_" + key) or self.config.get(key) or default

    def get_bool(self, key: str, default: Any = None) -> bool | None:
        """Get boolean value either from environment or from config file."""

        result = self.get(key=key, default=default)

        if isinstance(result, bool) or result is None:
            return result

        if result.lower() in ["true", "1", "yes"]:
            return True

        if result.lower() in ["false", "0", "no"]:
            return False

        raise ValueError(f"Invalid bool result: {result}")


def atm_user_is_valid(user: str) -> bool:
    """Check if user is known to Adaptavist/Jira."""
    cfg = ATMConfiguration()
    return user in Adaptavist(cfg.get("jira_server", ""), cfg.get("jira_username", ""), cfg.get("jira_password", "")).get_users()
