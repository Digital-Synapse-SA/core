"""Tests for the tractive integration."""

from unittest.mock import patch

from smarthub.core import SmartHub

from tests.common import MockConfigEntry


async def init_integration(
    hass: SmartHub, entry: MockConfigEntry
) -> MockConfigEntry:
    """Set up the Tractive integration in SmartHub."""
    entry.add_to_hass(hass)

    with patch("smarthub.components.tractive.TractiveClient._listen"):
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()
