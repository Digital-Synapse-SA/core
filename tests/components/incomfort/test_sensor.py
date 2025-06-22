"""Sensor tests for Intergas InComfort integration."""

from unittest.mock import MagicMock, patch

import pytest
from syrupy.assertion import SnapshotAssertion

from smarthub.config_entries import ConfigEntry
from smarthub.const import Platform
from smarthub.core import SmartHub
from smarthub.helpers import entity_registry as er

from tests.common import snapshot_platform


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
@patch("smarthub.components.incomfort.PLATFORMS", [Platform.SENSOR])
async def test_setup_platform(
    hass: SmartHub,
    mock_incomfort: MagicMock,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
    mock_config_entry: ConfigEntry,
) -> None:
    """Test the incomfort entities are set up correctly."""
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)
