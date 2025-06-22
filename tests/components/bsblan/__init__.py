"""Tests for the bsblan integration."""

from unittest.mock import patch

from smarthub.const import Platform
from smarthub.core import SmartHub

from tests.common import MockConfigEntry


async def setup_with_selected_platforms(
    hass: SmartHub, config_entry: MockConfigEntry, platforms: list[Platform]
) -> None:
    """Set up the BSBLAN integration with the selected platforms."""
    config_entry.add_to_hass(hass)
    with patch("smarthub.components.bsblan.PLATFORMS", platforms):
        assert await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()
