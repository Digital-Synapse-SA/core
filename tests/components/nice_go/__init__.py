"""Tests for the Nice G.O. integration."""

from unittest.mock import patch

from smarthub.const import Platform
from smarthub.core import SmartHub

from tests.common import MockConfigEntry


async def setup_integration(
    hass: SmartHub, config_entry: MockConfigEntry, platforms: list[Platform]
) -> None:
    """Fixture for setting up the component."""
    config_entry.add_to_hass(hass)

    with patch(
        "smarthub.components.nice_go.PLATFORMS",
        platforms,
    ):
        await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()
