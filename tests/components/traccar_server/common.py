"""Common test tools for Traccar Server."""

from smarthub.core import SmartHub

from tests.common import MockConfigEntry


async def setup_integration(hass: SmartHub, config_entry: MockConfigEntry) -> None:
    """Set up the integration."""
    config_entry.add_to_hass(hass)

    await hass.config_entries.async_setup(config_entry.entry_id)
