"""Provide a mock standalone component."""

from smarthub.core import SmartHub
from smarthub.helpers.typing import ConfigType

DOMAIN = "test_standalone"


async def async_setup(hass: SmartHub, config: ConfigType) -> bool:
    """Mock a successful setup."""
    return True
