"""Sensor tests for the Sabnzbd component."""

from unittest.mock import patch

import pytest
from syrupy.assertion import SnapshotAssertion

from smarthub.const import Platform
from smarthub.core import SmartHub
from smarthub.helpers import entity_registry as er

from tests.common import MockConfigEntry, snapshot_platform


@patch("smarthub.components.sabnzbd.PLATFORMS", [Platform.SENSOR])
@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_sensor(
    hass: SmartHub,
    entity_registry: er.EntityRegistry,
    config_entry: MockConfigEntry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test sensor setup."""
    await hass.config_entries.async_setup(config_entry.entry_id)
    await snapshot_platform(hass, entity_registry, snapshot, config_entry.entry_id)
