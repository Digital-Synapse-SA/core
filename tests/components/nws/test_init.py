"""Tests for init module."""

from smarthub.components.nws.const import DOMAIN
from smarthub.config_entries import ConfigEntryState
from smarthub.core import SmartHub

from .const import NWS_CONFIG

from tests.common import MockConfigEntry


async def test_unload_entry(hass: SmartHub, mock_simple_nws) -> None:
    """Test that nws setup with config yaml."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data=NWS_CONFIG,
    )
    entry.add_to_hass(hass)

    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    assert len(hass.config_entries.async_entries(DOMAIN)) == 1
    assert entry.state is ConfigEntryState.LOADED

    assert await hass.config_entries.async_unload(entry.entry_id)
    await hass.async_block_till_done()

    assert entry.state is ConfigEntryState.NOT_LOADED
