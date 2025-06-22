"""The SensorPush Bluetooth integration."""

from __future__ import annotations

import logging

from sensorpush_ble import SensorPushBluetoothDeviceData

from smarthub.components.bluetooth import BluetoothScanningMode
from smarthub.components.bluetooth.passive_update_processor import (
    PassiveBluetoothProcessorCoordinator,
)
from smarthub.config_entries import ConfigEntry
from smarthub.const import Platform
from smarthub.core import SmartHub

PLATFORMS: list[Platform] = [Platform.SENSOR]

_LOGGER = logging.getLogger(__name__)

type SensorPushConfigEntry = ConfigEntry[PassiveBluetoothProcessorCoordinator]


async def async_setup_entry(hass: SmartHub, entry: SensorPushConfigEntry) -> bool:
    """Set up SensorPush BLE device from a config entry."""
    address = entry.unique_id
    assert address is not None
    coordinator = PassiveBluetoothProcessorCoordinator(
        hass,
        _LOGGER,
        address=address,
        mode=BluetoothScanningMode.PASSIVE,
        update_method=SensorPushBluetoothDeviceData().update,
    )
    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    # only start after all platforms have had a chance to subscribe
    entry.async_on_unload(coordinator.async_start())
    return True


async def async_unload_entry(hass: SmartHub, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
