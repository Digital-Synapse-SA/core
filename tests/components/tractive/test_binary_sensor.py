"""Test the Tractive binary sensor platform."""

from unittest.mock import AsyncMock, patch

from syrupy.assertion import SnapshotAssertion

from smarthub.const import Platform
from smarthub.core import SmartHub
from smarthub.helpers import entity_registry as er

from . import init_integration

from tests.common import MockConfigEntry, snapshot_platform


async def test_binary_sensor(
    hass: SmartHub,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
    mock_tractive_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test states of the binary sensor."""
    with patch("smarthub.components.tractive.PLATFORMS", [Platform.BINARY_SENSOR]):
        await init_integration(hass, mock_config_entry)

        mock_tractive_client.send_hardware_event(mock_config_entry)
        await hass.async_block_till_done()
    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)
