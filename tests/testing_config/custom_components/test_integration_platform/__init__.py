"""Provide a mock package component."""

from smarthub.core import SmartHub
from smarthub.helpers.typing import ConfigType

from .const import TEST  # noqa: F401

DOMAIN = "test_integration_platform"


async def async_setup(hass: SmartHub, config: ConfigType) -> bool:
    """Mock a successful setup."""
    return True
