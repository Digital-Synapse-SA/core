"""Stub switch platform for translation tests."""

from smarthub.core import SmartHub
from smarthub.helpers.entity_platform import AddEntitiesCallback
from smarthub.helpers.typing import ConfigType, DiscoveryInfoType


async def async_setup_platform(
    hass: SmartHub,
    config: ConfigType,
    async_add_entities_callback: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Stub setup for translation tests."""
    async_add_entities_callback([])
