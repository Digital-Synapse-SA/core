"""The tests for Radarr binary sensor platform."""

import pytest

from smarthub.components.binary_sensor import BinarySensorDeviceClass
from smarthub.const import ATTR_DEVICE_CLASS, STATE_ON
from smarthub.core import SmartHub

from . import setup_integration

from tests.test_util.aiohttp import AiohttpClientMocker


@pytest.mark.freeze_time("2021-12-03 00:00:00+00:00")
async def test_binary_sensors(
    hass: SmartHub, aioclient_mock: AiohttpClientMocker
) -> None:
    """Test for binary sensor values."""
    await setup_integration(hass, aioclient_mock)

    state = hass.states.get("binary_sensor.mock_title_health")
    assert state.state == STATE_ON
    assert state.attributes.get(ATTR_DEVICE_CLASS) == BinarySensorDeviceClass.PROBLEM
