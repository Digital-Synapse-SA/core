"""The test for the Trafikverket binary sensor platform."""

from __future__ import annotations

import pytest
from pytrafikverket import CameraInfoModel

from smarthub.config_entries import ConfigEntry
from smarthub.const import STATE_ON
from smarthub.core import SmartHub


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_sensor(
    hass: SmartHub,
    load_int: ConfigEntry,
    get_camera: CameraInfoModel,
) -> None:
    """Test the Trafikverket Camera binary sensor."""

    state = hass.states.get("binary_sensor.test_camera_active")
    assert state.state == STATE_ON
