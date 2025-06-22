"""Component with embedded platforms."""

from smarthub.core import SmartHub
from smarthub.helpers.typing import ConfigType

DOMAIN = "test_embedded"


async def async_setup(hass: SmartHub, config: ConfigType) -> bool:
    """Mock config."""
    return True
