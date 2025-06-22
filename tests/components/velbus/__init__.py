"""Tests for the Velbus component."""

from smarthub.components.velbus import VelbusConfigEntry
from smarthub.core import SmartHub


async def init_integration(
    hass: SmartHub,
    config_entry: VelbusConfigEntry,
) -> None:
    """Load the Velbus integration."""
    assert await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()
