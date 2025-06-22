"""Support for WLED."""

from __future__ import annotations

from smarthub.config_entries import ConfigEntry
from smarthub.const import Platform
from smarthub.core import SmartHub
from smarthub.helpers import config_validation as cv
from smarthub.helpers.typing import ConfigType
from smarthub.util.hass_dict import HassKey

from .const import DOMAIN
from .coordinator import WLEDDataUpdateCoordinator, WLEDReleasesDataUpdateCoordinator

PLATFORMS = (
    Platform.BUTTON,
    Platform.LIGHT,
    Platform.NUMBER,
    Platform.SELECT,
    Platform.SENSOR,
    Platform.SWITCH,
    Platform.UPDATE,
)

type WLEDConfigEntry = ConfigEntry[WLEDDataUpdateCoordinator]

WLED_KEY: HassKey[WLEDReleasesDataUpdateCoordinator] = HassKey(DOMAIN)
CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup(hass: SmartHub, config: ConfigType) -> bool:
    """Set up the WLED integration.

    We set up a single coordinator for fetching WLED releases, which
    is used across all WLED devices (and config entries) to avoid
    fetching the same data multiple times for each.
    """
    hass.data[WLED_KEY] = WLEDReleasesDataUpdateCoordinator(hass)
    await hass.data[WLED_KEY].async_request_refresh()
    return True


async def async_setup_entry(hass: SmartHub, entry: WLEDConfigEntry) -> bool:
    """Set up WLED from a config entry."""
    entry.runtime_data = WLEDDataUpdateCoordinator(hass, entry=entry)
    await entry.runtime_data.async_config_entry_first_refresh()

    # Set up all platforms for this device/entry.
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Reload entry when its updated.
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(hass: SmartHub, entry: WLEDConfigEntry) -> bool:
    """Unload WLED config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        coordinator = entry.runtime_data

        # Ensure disconnected and cleanup stop sub
        await coordinator.wled.disconnect()
        if coordinator.unsub:
            coordinator.unsub()

    return unload_ok


async def async_reload_entry(hass: SmartHub, entry: ConfigEntry) -> None:
    """Reload the config entry when it changed."""
    await hass.config_entries.async_reload(entry.entry_id)
