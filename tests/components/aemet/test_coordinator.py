"""Define tests for the AEMET OpenData coordinator."""

from unittest.mock import patch

from aemet_opendata.exceptions import AemetError
from freezegun.api import FrozenDateTimeFactory

from smarthub.components.aemet.coordinator import WEATHER_UPDATE_INTERVAL
from smarthub.const import STATE_UNAVAILABLE
from smarthub.core import SmartHub

from .util import async_init_integration

from tests.common import async_fire_time_changed


async def test_coordinator_error(
    hass: SmartHub,
    freezer: FrozenDateTimeFactory,
) -> None:
    """Test error on coordinator update."""

    await hass.config.async_set_time_zone("UTC")
    freezer.move_to("2021-01-09 12:00:00+00:00")
    await async_init_integration(hass)

    with patch(
        "smarthub.components.aemet.AEMET.api_call",
        side_effect=AemetError,
    ):
        freezer.tick(WEATHER_UPDATE_INTERVAL)
        async_fire_time_changed(hass)
        await hass.async_block_till_done(wait_background_tasks=True)

        state = hass.states.get("weather.aemet")
        assert state.state == STATE_UNAVAILABLE
