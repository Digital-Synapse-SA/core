"""Tests for the OneDrive integration."""

from smarthub.core import SmartHub

from tests.common import MockConfigEntry


async def setup_integration(
    hass: SmartHub, mock_config_entry: MockConfigEntry
) -> None:
    """Set up the OneDrive integration for testing."""
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()
