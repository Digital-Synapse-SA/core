"""Test squeezebox binary sensors."""

from copy import deepcopy
from unittest.mock import patch

from smarthub.const import Platform
from smarthub.core import SmartHub

from .conftest import FAKE_QUERY_RESPONSE

from tests.common import MockConfigEntry


async def test_binary_sensor(
    hass: SmartHub,
    config_entry: MockConfigEntry,
) -> None:
    """Test binary sensor states and attributes."""
    with (
        patch(
            "smarthub.components.squeezebox.PLATFORMS",
            [Platform.BINARY_SENSOR],
        ),
        patch(
            "smarthub.components.squeezebox.Server.async_query",
            return_value=deepcopy(FAKE_QUERY_RESPONSE),
        ),
    ):
        await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done(wait_background_tasks=True)

    state = hass.states.get("binary_sensor.fakelib_needs_restart")

    assert state is not None
    assert state.state == "off"
