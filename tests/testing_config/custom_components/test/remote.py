"""Provide a mock remote platform.

Call init before using it in your tests to ensure clean test data.
"""

from smarthub.components.remote import RemoteEntity
from smarthub.const import STATE_OFF, STATE_ON
from smarthub.core import SmartHub
from smarthub.helpers.entity_platform import AddEntitiesCallback
from smarthub.helpers.typing import ConfigType, DiscoveryInfoType

from tests.common import MockToggleEntity

ENTITIES = []


def init(empty=False):
    """Initialize the platform with entities."""
    # pylint: disable-next=global-statement
    global ENTITIES  # noqa: PLW0603

    ENTITIES = (
        []
        if empty
        else [
            MockRemote("TV", STATE_ON),
            MockRemote("DVD", STATE_OFF),
            MockRemote(None, STATE_OFF),
        ]
    )


async def async_setup_platform(
    hass: SmartHub,
    config: ConfigType,
    async_add_entities_callback: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Return mock entities."""
    async_add_entities_callback(ENTITIES)


class MockRemote(MockToggleEntity, RemoteEntity):
    """Mock remote class."""

    supported_features = 0
