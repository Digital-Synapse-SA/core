"""Tests for the Flexit Nordic (BACnet) integration."""

from unittest.mock import patch

from smarthub.const import Platform
from smarthub.core import SmartHub

from tests.common import MockConfigEntry


async def setup_with_selected_platforms(
    hass: SmartHub, entry: MockConfigEntry, platforms: list[Platform]
) -> None:
    """Set up the Flexit Nordic (BACnet) integration with the selected platforms."""
    entry.add_to_hass(hass)
    with patch("smarthub.components.flexit_bacnet.PLATFORMS", platforms):
        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()
