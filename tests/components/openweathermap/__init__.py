"""Shared utilities for OpenWeatherMap tests."""

from unittest.mock import patch

from smarthub.config_entries import ConfigEntryState
from smarthub.const import Platform
from smarthub.core import SmartHub

from tests.common import MockConfigEntry


async def setup_platform(
    hass: SmartHub,
    config_entry: MockConfigEntry,
    platforms: list[Platform],
):
    """Set up the OpenWeatherMap platform."""
    config_entry.add_to_hass(hass)
    with (
        patch("smarthub.components.openweathermap.PLATFORMS", platforms),
    ):
        assert await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()
        assert config_entry.state is ConfigEntryState.LOADED
