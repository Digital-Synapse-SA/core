"""The Bluetooth Adapters integration."""

from __future__ import annotations

from smarthub.core import SmartHub
from smarthub.helpers import config_validation as cv
from smarthub.helpers.typing import ConfigType

DOMAIN = "bluetooth_adapters"

CONFIG_SCHEMA = cv.empty_config_schema(DOMAIN)


async def async_setup(hass: SmartHub, config: ConfigType) -> bool:
    """Set up Bluetooth Adapters from a config entry.

    This integration is only used as a dependency for other integrations
    that need Bluetooth Adapters.

    All integrations that provide Bluetooth Adapters must be listed
    in after_dependencies in the manifest.json file to ensure
    they are loaded before this integration.
    """
    return True
