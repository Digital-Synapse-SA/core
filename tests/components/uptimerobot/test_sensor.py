"""Test UptimeRobot sensor."""

from unittest.mock import patch

from pyuptimerobot import UptimeRobotAuthenticationException

from smarthub.components.sensor import SensorDeviceClass
from smarthub.components.uptimerobot.const import COORDINATOR_UPDATE_INTERVAL
from smarthub.const import STATE_UNAVAILABLE
from smarthub.core import SmartHub
from smarthub.util import dt as dt_util

from .common import (
    MOCK_UPTIMEROBOT_MONITOR,
    STATE_UP,
    UPTIMEROBOT_SENSOR_TEST_ENTITY,
    setup_uptimerobot_integration,
)

from tests.common import async_fire_time_changed


async def test_presentation(hass: SmartHub) -> None:
    """Test the presentation of UptimeRobot sensors."""
    await setup_uptimerobot_integration(hass)

    entity = hass.states.get(UPTIMEROBOT_SENSOR_TEST_ENTITY)

    assert entity.state == STATE_UP
    assert entity.attributes["target"] == MOCK_UPTIMEROBOT_MONITOR["url"]
    assert entity.attributes["device_class"] == SensorDeviceClass.ENUM
    assert entity.attributes["options"] == [
        "down",
        "not_checked_yet",
        "pause",
        "seems_down",
        "up",
    ]


async def test_unavailable_on_update_failure(hass: SmartHub) -> None:
    """Test entity unavailable on update failure."""
    await setup_uptimerobot_integration(hass)

    entity = hass.states.get(UPTIMEROBOT_SENSOR_TEST_ENTITY)
    assert entity.state == STATE_UP

    with patch(
        "pyuptimerobot.UptimeRobot.async_get_monitors",
        side_effect=UptimeRobotAuthenticationException,
    ):
        async_fire_time_changed(hass, dt_util.utcnow() + COORDINATOR_UPDATE_INTERVAL)
        await hass.async_block_till_done()

    entity = hass.states.get(UPTIMEROBOT_SENSOR_TEST_ENTITY)
    assert entity.state == STATE_UNAVAILABLE
