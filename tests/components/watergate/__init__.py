"""Tests for the Watergate integration."""

from smarthub.core import SmartHub


async def init_integration(hass: SmartHub, mock_entry) -> None:
    """Set up the Watergate integration in SmartHub."""
    mock_entry.add_to_hass(hass)

    await hass.config_entries.async_setup(mock_entry.entry_id)
    await hass.async_block_till_done()
