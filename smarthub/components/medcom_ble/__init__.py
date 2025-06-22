"""The Medcom BLE integration."""

from __future__ import annotations

from datetime import timedelta
import logging

from bleak import BleakError
from medcom_ble import MedcomBleDeviceData

from smarthub.components import bluetooth
from smarthub.config_entries import ConfigEntry
from smarthub.const import Platform
from smarthub.core import SmartHub
from smarthub.exceptions import ConfigEntryNotReady
from smarthub.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from smarthub.util.unit_system import METRIC_SYSTEM

from .const import DEFAULT_SCAN_INTERVAL, DOMAIN

# Supported platforms
PLATFORMS: list[Platform] = [Platform.SENSOR]

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: SmartHub, entry: ConfigEntry) -> bool:
    """Set up Medcom BLE radiation monitor from a config entry."""

    address = entry.unique_id
    elevation = hass.config.elevation
    is_metric = hass.config.units is METRIC_SYSTEM
    assert address is not None

    ble_device = bluetooth.async_ble_device_from_address(hass, address)
    if not ble_device:
        raise ConfigEntryNotReady(
            f"Could not find Medcom BLE device with address {address}"
        )

    async def _async_update_method():
        """Get data from Medcom BLE radiation monitor."""
        ble_device = bluetooth.async_ble_device_from_address(hass, address)
        inspector = MedcomBleDeviceData(_LOGGER, elevation, is_metric)

        try:
            data = await inspector.update_device(ble_device)
        except BleakError as err:
            raise UpdateFailed(f"Unable to fetch data: {err}") from err

        return data

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        config_entry=entry,
        name=DOMAIN,
        update_method=_async_update_method,
        update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: SmartHub, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
