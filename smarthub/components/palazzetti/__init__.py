"""The Palazzetti integration."""

from __future__ import annotations

from smarthub.const import Platform
from smarthub.core import SmartHub

from .coordinator import PalazzettiConfigEntry, PalazzettiDataUpdateCoordinator

PLATFORMS: list[Platform] = [
    Platform.BUTTON,
    Platform.CLIMATE,
    Platform.NUMBER,
    Platform.SENSOR,
]


async def async_setup_entry(hass: SmartHub, entry: PalazzettiConfigEntry) -> bool:
    """Set up Palazzetti from a config entry."""

    coordinator = PalazzettiDataUpdateCoordinator(hass, entry)

    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: SmartHub, entry: PalazzettiConfigEntry) -> bool:
    """Unload a config entry."""

    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
