"""The Recovery Mode integration."""

from smarthub.components import persistent_notification
from smarthub.core import SmartHub
from smarthub.helpers import config_validation as cv
from smarthub.helpers.typing import ConfigType

DOMAIN = "recovery_mode"

CONFIG_SCHEMA = cv.empty_config_schema(DOMAIN)


async def async_setup(hass: SmartHub, config: ConfigType) -> bool:
    """Set up the Recovery Mode component."""
    persistent_notification.async_create(
        hass,
        (
            "SmartHub is running in recovery mode. Check [the error"
            " log](/config/logs) to see what went wrong."
        ),
        "Recovery Mode",
    )
    return True
