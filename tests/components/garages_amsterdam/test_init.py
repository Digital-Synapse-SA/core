"""Tests for the Garages Amsterdam integration."""

from unittest.mock import AsyncMock

from smarthub.config_entries import ConfigEntryState
from smarthub.core import SmartHub

from tests.common import MockConfigEntry


async def test_load_unload_config_entry(
    hass: SmartHub,
    mock_config_entry: MockConfigEntry,
    mock_garages_amsterdam: AsyncMock,
) -> None:
    """Test the Garages Amsterdam integration loads and unloads correctly."""
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    assert mock_config_entry.state is ConfigEntryState.LOADED

    await hass.config_entries.async_unload(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    assert mock_config_entry.state is ConfigEntryState.NOT_LOADED
