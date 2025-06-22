"""Component for the Slide local API."""

from __future__ import annotations

from smarthub.const import Platform
from smarthub.core import SmartHub

from .coordinator import SlideConfigEntry, SlideCoordinator

PLATFORMS = [Platform.BUTTON, Platform.COVER, Platform.SWITCH]


async def async_setup_entry(hass: SmartHub, entry: SlideConfigEntry) -> bool:
    """Set up the slide_local integration."""

    coordinator = SlideCoordinator(hass, entry)

    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    entry.async_on_unload(entry.add_update_listener(update_listener))

    return True


async def update_listener(hass: SmartHub, entry: SlideConfigEntry) -> None:
    """Handle options update."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: SmartHub, entry: SlideConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
