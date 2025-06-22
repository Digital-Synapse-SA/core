"""The OralB integration."""

from __future__ import annotations

import logging

from oralb_ble import OralBBluetoothDeviceData, SensorUpdate

from smarthub.components.bluetooth import (
    BluetoothScanningMode,
    BluetoothServiceInfoBleak,
    async_ble_device_from_address,
)
from smarthub.components.bluetooth.active_update_processor import (
    ActiveBluetoothProcessorCoordinator,
)
from smarthub.config_entries import ConfigEntry
from smarthub.const import Platform
from smarthub.core import CoreState, SmartHub

PLATFORMS: list[Platform] = [Platform.SENSOR]

_LOGGER = logging.getLogger(__name__)


type OralBConfigEntry = ConfigEntry[ActiveBluetoothProcessorCoordinator]


async def async_setup_entry(hass: SmartHub, entry: OralBConfigEntry) -> bool:
    """Set up OralB BLE device from a config entry."""
    address = entry.unique_id
    assert address is not None
    data = OralBBluetoothDeviceData()

    def _needs_poll(
        service_info: BluetoothServiceInfoBleak, last_poll: float | None
    ) -> bool:
        # Only poll if hass is running, we need to poll,
        # and we actually have a way to connect to the device
        return (
            hass.state is CoreState.running
            and data.poll_needed(service_info, last_poll)
            and bool(
                async_ble_device_from_address(
                    hass, service_info.device.address, connectable=True
                )
            )
        )

    async def _async_poll(service_info: BluetoothServiceInfoBleak) -> SensorUpdate:
        # BluetoothServiceInfoBleak is defined in HA, otherwise would just pass it
        # directly to the oralb code
        # Make sure the device we have is one that we can connect with
        # in case its coming from a passive scanner
        if service_info.connectable:
            connectable_device = service_info.device
        elif device := async_ble_device_from_address(
            hass, service_info.device.address, True
        ):
            connectable_device = device
        else:
            # We have no bluetooth controller that is in range of
            # the device to poll it
            raise RuntimeError(
                f"No connectable device found for {service_info.device.address}"
            )
        return await data.async_poll(connectable_device)

    coordinator = entry.runtime_data = ActiveBluetoothProcessorCoordinator(
        hass,
        _LOGGER,
        address=address,
        mode=BluetoothScanningMode.PASSIVE,
        update_method=data.update,
        needs_poll_method=_needs_poll,
        poll_method=_async_poll,
        # We will take advertisements from non-connectable devices
        # since we will trade the BLEDevice for a connectable one
        # if we need to poll it
        connectable=False,
    )
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    # only start after all platforms have had a chance to subscribe
    entry.async_on_unload(coordinator.async_start())
    return True


async def async_unload_entry(hass: SmartHub, entry: OralBConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
