"""The Mopeka integration."""

from __future__ import annotations

import logging

from mopeka_iot_ble import MediumType, MopekaIOTBluetoothDeviceData

from smarthub.components.bluetooth import BluetoothScanningMode
from smarthub.components.bluetooth.passive_update_processor import (
    PassiveBluetoothProcessorCoordinator,
)
from smarthub.config_entries import ConfigEntry
from smarthub.const import Platform
from smarthub.core import SmartHub

from .const import CONF_MEDIUM_TYPE, DEFAULT_MEDIUM_TYPE

PLATFORMS: list[Platform] = [Platform.SENSOR]

_LOGGER = logging.getLogger(__name__)


type MopekaConfigEntry = ConfigEntry[PassiveBluetoothProcessorCoordinator]


async def async_setup_entry(hass: SmartHub, entry: MopekaConfigEntry) -> bool:
    """Set up Mopeka BLE device from a config entry."""
    address = entry.unique_id
    assert address is not None

    # Default sensors configured prior to the introduction of MediumType
    medium_type_str = entry.data.get(CONF_MEDIUM_TYPE, DEFAULT_MEDIUM_TYPE)
    data = MopekaIOTBluetoothDeviceData(MediumType(medium_type_str))
    coordinator = entry.runtime_data = PassiveBluetoothProcessorCoordinator(
        hass,
        _LOGGER,
        address=address,
        mode=BluetoothScanningMode.PASSIVE,
        update_method=data.update,
    )
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    # only start after all platforms have had a chance to subscribe
    entry.async_on_unload(coordinator.async_start())
    entry.async_on_unload(entry.add_update_listener(update_listener))
    return True


async def update_listener(hass: SmartHub, entry: MopekaConfigEntry) -> None:
    """Handle options update."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: SmartHub, entry: MopekaConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
