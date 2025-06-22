"""The Duke Energy integration."""

from __future__ import annotations

from smarthub.core import SmartHub

from .coordinator import DukeEnergyConfigEntry, DukeEnergyCoordinator


async def async_setup_entry(hass: SmartHub, entry: DukeEnergyConfigEntry) -> bool:
    """Set up Duke Energy from a config entry."""

    coordinator = DukeEnergyCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data = coordinator

    return True


async def async_unload_entry(hass: SmartHub, entry: DukeEnergyConfigEntry) -> bool:
    """Unload a config entry."""
    return True
