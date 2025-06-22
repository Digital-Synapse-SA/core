"""Tests for the IMGW-PIB integration."""

from smarthub.core import SmartHub

from tests.common import MockConfigEntry


async def init_integration(
    hass: SmartHub, config_entry: MockConfigEntry
) -> MockConfigEntry:
    """Set up the IMGW-PIB integration in SmartHub."""
    config_entry.add_to_hass(hass)

    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()
