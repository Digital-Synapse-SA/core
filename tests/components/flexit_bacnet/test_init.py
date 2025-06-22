"""Tests for the Flexit Nordic (BACnet) __init__."""

from flexit_bacnet import DecodingError

from smarthub.components.flexit_bacnet.const import DOMAIN
from smarthub.config_entries import ConfigEntryState
from smarthub.const import Platform
from smarthub.core import SmartHub

from . import setup_with_selected_platforms

from tests.common import MockConfigEntry


async def test_loading_and_unloading_config_entry(
    hass: SmartHub, mock_config_entry: MockConfigEntry, mock_flexit_bacnet
) -> None:
    """Test loading and unloading a config entry."""
    await setup_with_selected_platforms(hass, mock_config_entry, [Platform.CLIMATE])

    assert len(hass.config_entries.async_entries(DOMAIN)) == 1
    assert mock_config_entry.state is ConfigEntryState.LOADED

    assert await hass.config_entries.async_unload(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    assert mock_config_entry.state is ConfigEntryState.NOT_LOADED


async def test_failed_initialization(
    hass: SmartHub, mock_config_entry: MockConfigEntry, mock_flexit_bacnet
) -> None:
    """Test failed initialization."""
    mock_flexit_bacnet.update.side_effect = DecodingError
    mock_config_entry.add_to_hass(hass)
    assert not await hass.config_entries.async_setup(mock_config_entry.entry_id)
    assert mock_config_entry.state is ConfigEntryState.SETUP_RETRY
