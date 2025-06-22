"""Tests for the Chacon Dio integration."""

from smarthub.core import SmartHub

from tests.common import MockConfigEntry


async def setup_integration(hass: SmartHub, config_entry: MockConfigEntry) -> None:
    """Fixture for setting up the component."""
    config_entry.add_to_hass(hass)

    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()
