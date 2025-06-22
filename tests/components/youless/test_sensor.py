"""Test the sensor classes for youless."""

from unittest.mock import patch

from syrupy.assertion import SnapshotAssertion

from smarthub.const import Platform
from smarthub.core import SmartHub
from smarthub.helpers import entity_registry as er

from . import init_component

from tests.common import snapshot_platform


async def test_sensors(
    hass: SmartHub, entity_registry: er.EntityRegistry, snapshot: SnapshotAssertion
) -> None:
    """Test the sensor classes for youless."""
    with patch("smarthub.components.youless.PLATFORMS", [Platform.SENSOR]):
        entry = await init_component(hass)

    await snapshot_platform(hass, entity_registry, snapshot, entry.entry_id)
