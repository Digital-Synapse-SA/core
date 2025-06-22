"""The test for the Coolmaster binary sensor platform."""

from __future__ import annotations

from smarthub.config_entries import ConfigEntry
from smarthub.core import SmartHub


async def test_binary_sensor(
    hass: SmartHub,
    load_int: ConfigEntry,
) -> None:
    """Test the Coolmaster binary sensor."""
    assert hass.states.get("binary_sensor.l1_100_clean_filter").state == "off"
    assert hass.states.get("binary_sensor.l1_101_clean_filter").state == "on"
