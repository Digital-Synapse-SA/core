"""Tests for Srp Energy component Init."""

from smarthub.config_entries import ConfigEntryState
from smarthub.core import SmartHub


async def test_setup_entry(hass: SmartHub, init_integration) -> None:
    """Test setup entry."""
    assert init_integration.state is ConfigEntryState.LOADED


async def test_unload_entry(hass: SmartHub, init_integration) -> None:
    """Test being able to unload an entry."""
    assert init_integration.state is ConfigEntryState.LOADED

    assert await hass.config_entries.async_unload(init_integration.entry_id)
    await hass.async_block_till_done()
