"""Tests for the Streamlabs Water sensor platform."""

from unittest.mock import AsyncMock, patch

from syrupy.assertion import SnapshotAssertion

from smarthub.const import Platform
from smarthub.core import SmartHub
from smarthub.helpers import entity_registry as er

from . import setup_integration

from tests.common import MockConfigEntry


async def test_all_entities(
    hass: SmartHub,
    snapshot: SnapshotAssertion,
    streamlabswater: AsyncMock,
    mock_config_entry: MockConfigEntry,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test all entities."""
    with patch("smarthub.components.streamlabswater.PLATFORMS", [Platform.SENSOR]):
        await setup_integration(hass, mock_config_entry)
        entity_entries = er.async_entries_for_config_entry(
            entity_registry, mock_config_entry.entry_id
        )

        assert entity_entries
        for entity_entry in entity_entries:
            assert entity_entry == snapshot(name=f"{entity_entry.entity_id}-entry")
            assert hass.states.get(entity_entry.entity_id) == snapshot(
                name=f"{entity_entry.entity_id}-state"
            )
