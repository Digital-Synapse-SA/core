"""Test the Kodi integration init."""

from unittest.mock import patch

from smarthub.components.kodi.const import DOMAIN
from smarthub.config_entries import ConfigEntryState
from smarthub.core import SmartHub

from . import init_integration


async def test_unload_entry(hass: SmartHub) -> None:
    """Test successful unload of entry."""
    with patch(
        "smarthub.components.kodi.media_player.async_setup_entry",
        return_value=True,
    ):
        entry = await init_integration(hass)

    assert len(hass.config_entries.async_entries(DOMAIN)) == 1
    assert entry.state is ConfigEntryState.LOADED

    assert await hass.config_entries.async_unload(entry.entry_id)
    await hass.async_block_till_done()

    assert entry.state is ConfigEntryState.NOT_LOADED
    assert not hass.data.get(DOMAIN)
