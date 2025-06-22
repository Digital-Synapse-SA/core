"""Tests for the IOmeter integration."""

from unittest.mock import patch

from smarthub.const import Platform
from smarthub.core import SmartHub

from tests.common import MockConfigEntry


async def setup_platform(
    hass: SmartHub, config_entry: MockConfigEntry, platforms: list[Platform]
) -> MockConfigEntry:
    """Fixture for setting up the IOmeter platform."""
    config_entry.add_to_hass(hass)

    with patch("smarthub.components.iometer.PLATFORMS", platforms):
        await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()
