"""Tests for the StreamLabs integration."""

from smarthub.core import SmartHub
from smarthub.util.unit_system import US_CUSTOMARY_SYSTEM

from tests.common import MockConfigEntry


async def setup_integration(hass: SmartHub, config_entry: MockConfigEntry) -> None:
    """Fixture for setting up the component."""
    config_entry.add_to_hass(hass)

    hass.config.units = US_CUSTOMARY_SYSTEM

    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()
