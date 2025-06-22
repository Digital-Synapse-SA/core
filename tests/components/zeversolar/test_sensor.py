"""Test the sensor classes."""

from unittest.mock import patch

from syrupy.assertion import SnapshotAssertion

from smarthub.const import Platform
from smarthub.core import SmartHub
from smarthub.helpers import entity_registry as er

from . import init_integration

from tests.common import snapshot_platform


async def test_sensors(
    hass: SmartHub, entity_registry: er.EntityRegistry, snapshot: SnapshotAssertion
) -> None:
    """Test sensors."""

    with patch(
        "smarthub.components.zeversolar.PLATFORMS",
        [Platform.SENSOR],
    ):
        entry = await init_integration(hass)

        await snapshot_platform(hass, entity_registry, snapshot, entry.entry_id)
