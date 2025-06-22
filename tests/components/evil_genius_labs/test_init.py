"""Test evil genius labs init."""

import pytest

from smarthub.components.evil_genius_labs import PLATFORMS
from smarthub.config_entries import ConfigEntryState
from smarthub.core import SmartHub


@pytest.mark.parametrize("platforms", [PLATFORMS])
async def test_setup_unload_entry(
    hass: SmartHub, setup_evil_genius_labs, config_entry
) -> None:
    """Test setting up and unloading a config entry."""
    assert len(hass.states.async_entity_ids()) == 1
    assert await hass.config_entries.async_unload(config_entry.entry_id)
    assert config_entry.state is ConfigEntryState.NOT_LOADED
