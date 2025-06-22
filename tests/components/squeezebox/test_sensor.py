"""Test squeezebox sensors."""

from copy import deepcopy
from unittest.mock import patch

from smarthub.const import Platform
from smarthub.core import SmartHub

from .conftest import FAKE_QUERY_RESPONSE

from tests.common import MockConfigEntry


async def test_sensor(hass: SmartHub, config_entry: MockConfigEntry) -> None:
    """Test sensor states and attributes."""

    # Setup component
    with (
        patch(
            "smarthub.components.squeezebox.PLATFORMS",
            [Platform.SENSOR],
        ),
        patch(
            "smarthub.components.squeezebox.Server.async_query",
            return_value=deepcopy(FAKE_QUERY_RESPONSE),
        ),
    ):
        await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done(wait_background_tasks=True)

    state = hass.states.get("sensor.fakelib_player_count")

    assert state is not None
    assert state.state == "10"
