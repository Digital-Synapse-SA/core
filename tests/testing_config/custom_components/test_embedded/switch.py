"""Switch platform for the embedded component."""

from smarthub.core import SmartHub
from smarthub.helpers.entity_platform import AddEntitiesCallback
from smarthub.helpers.typing import ConfigType, DiscoveryInfoType


async def async_setup_platform(
    hass: SmartHub,
    config: ConfigType,
    async_add_entities_callback: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Find and return test switches."""
