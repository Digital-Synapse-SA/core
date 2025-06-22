"""Binary sensor tests for the Dremel 3D Printer integration."""

import pytest

from smarthub.components.binary_sensor import BinarySensorDeviceClass
from smarthub.components.dremel_3d_printer.const import DOMAIN
from smarthub.const import ATTR_DEVICE_CLASS, STATE_OFF, STATE_ON
from smarthub.core import SmartHub
from smarthub.setup import async_setup_component

from tests.common import MockConfigEntry


@pytest.mark.usefixtures("connection", "entity_registry_enabled_by_default")
async def test_binary_sensors(
    hass: SmartHub, config_entry: MockConfigEntry
) -> None:
    """Test we get binary sensor data."""
    await hass.config_entries.async_setup(config_entry.entry_id)
    assert await async_setup_component(hass, DOMAIN, {})
    state = hass.states.get("binary_sensor.dremel_3d45_door")
    assert state.attributes.get(ATTR_DEVICE_CLASS) == BinarySensorDeviceClass.DOOR
    assert state.state == STATE_OFF
    state = hass.states.get("binary_sensor.dremel_3d45_running")
    assert state.state == STATE_ON
    assert state.attributes.get(ATTR_DEVICE_CLASS) == BinarySensorDeviceClass.RUNNING
