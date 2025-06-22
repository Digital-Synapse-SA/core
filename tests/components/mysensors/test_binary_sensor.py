"""Provide tests for mysensors binary sensor platform."""

from __future__ import annotations

from collections.abc import Callable

from mysensors.sensor import Sensor

from smarthub.components.binary_sensor import BinarySensorDeviceClass
from smarthub.const import ATTR_BATTERY_LEVEL, ATTR_DEVICE_CLASS
from smarthub.core import SmartHub


async def test_door_sensor(
    hass: SmartHub,
    door_sensor: Sensor,
    receive_message: Callable[[str], None],
) -> None:
    """Test a door sensor."""
    entity_id = "binary_sensor.door_sensor_1_1"

    state = hass.states.get(entity_id)

    assert state
    assert state.state == "off"
    assert state.attributes[ATTR_DEVICE_CLASS] == BinarySensorDeviceClass.DOOR
    assert state.attributes[ATTR_BATTERY_LEVEL] == 0

    receive_message("1;1;1;0;16;1\n")
    await hass.async_block_till_done()

    state = hass.states.get(entity_id)

    assert state
    assert state.state == "on"

    receive_message("1;1;1;0;16;0\n")
    await hass.async_block_till_done()

    state = hass.states.get(entity_id)

    assert state
    assert state.state == "off"
