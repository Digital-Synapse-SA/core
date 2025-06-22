"""Test the Tesla Fleet device tracker platform."""

from unittest.mock import AsyncMock

from syrupy.assertion import SnapshotAssertion
from tesla_fleet_api.exceptions import VehicleOffline

from smarthub.const import STATE_UNKNOWN, Platform
from smarthub.core import SmartHub
from smarthub.helpers import entity_registry as er

from . import assert_entities, setup_platform

from tests.common import MockConfigEntry


async def test_device_tracker(
    hass: SmartHub,
    snapshot: SnapshotAssertion,
    entity_registry: er.EntityRegistry,
    normal_config_entry: MockConfigEntry,
) -> None:
    """Tests that the device tracker entities are correct."""

    await setup_platform(hass, normal_config_entry, [Platform.DEVICE_TRACKER])
    assert_entities(hass, normal_config_entry.entry_id, entity_registry, snapshot)


async def test_device_tracker_offline(
    hass: SmartHub,
    mock_vehicle_data: AsyncMock,
    normal_config_entry: MockConfigEntry,
) -> None:
    """Tests that the device tracker entities are correct when offline."""

    mock_vehicle_data.side_effect = VehicleOffline
    await setup_platform(hass, normal_config_entry, [Platform.DEVICE_TRACKER])
    state = hass.states.get("device_tracker.test_location")
    assert state.state == STATE_UNKNOWN
