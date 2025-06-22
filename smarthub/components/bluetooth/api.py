"""The bluetooth integration apis.

These APIs are the only documented way to interact with the bluetooth integration.
"""

from __future__ import annotations

import asyncio
from asyncio import Future
from collections.abc import Callable, Iterable
from typing import TYPE_CHECKING, cast

from habluetooth import (
    BaseHaScanner,
    BluetoothScannerDevice,
    BluetoothScanningMode,
    HaBleakScannerWrapper,
    get_manager,
)
from home_assistant_bluetooth import BluetoothServiceInfoBleak

from smarthub.core import CALLBACK_TYPE, SmartHub, callback as hass_callback
from smarthub.helpers.singleton import singleton

from .const import DATA_MANAGER
from .manager import SmartHubBluetoothManager
from .match import BluetoothCallbackMatcher
from .models import BluetoothCallback, BluetoothChange, ProcessAdvertisementCallback

if TYPE_CHECKING:
    from bleak.backends.device import BLEDevice


@singleton(DATA_MANAGER)
def _get_manager(hass: SmartHub) -> SmartHubBluetoothManager:
    """Get the bluetooth manager."""
    return cast(SmartHubBluetoothManager, get_manager())


@hass_callback
def async_get_scanner(hass: SmartHub) -> HaBleakScannerWrapper:
    """Return a HaBleakScannerWrapper.

    This is a wrapper around our BleakScanner singleton that allows
    multiple integrations to share the same BleakScanner.
    """
    return HaBleakScannerWrapper()


@hass_callback
def async_scanner_by_source(hass: SmartHub, source: str) -> BaseHaScanner | None:
    """Return a scanner for a given source.

    This method is only intended to be used by integrations that implement
    a bluetooth client and need to interact with a scanner directly.

    It is not intended to be used by integrations that need to interact
    with a device.
    """
    return _get_manager(hass).async_scanner_by_source(source)


@hass_callback
def async_scanner_count(hass: SmartHub, connectable: bool = True) -> int:
    """Return the number of scanners currently in use."""
    return _get_manager(hass).async_scanner_count(connectable)


@hass_callback
def async_discovered_service_info(
    hass: SmartHub, connectable: bool = True
) -> Iterable[BluetoothServiceInfoBleak]:
    """Return the discovered devices list."""
    return _get_manager(hass).async_discovered_service_info(connectable)


@hass_callback
def async_last_service_info(
    hass: SmartHub, address: str, connectable: bool = True
) -> BluetoothServiceInfoBleak | None:
    """Return the last service info for an address."""
    return _get_manager(hass).async_last_service_info(address, connectable)


@hass_callback
def async_ble_device_from_address(
    hass: SmartHub, address: str, connectable: bool = True
) -> BLEDevice | None:
    """Return BLEDevice for an address if its present."""
    return _get_manager(hass).async_ble_device_from_address(address, connectable)


@hass_callback
def async_scanner_devices_by_address(
    hass: SmartHub, address: str, connectable: bool = True
) -> list[BluetoothScannerDevice]:
    """Return all discovered BluetoothScannerDevice for an address."""
    return _get_manager(hass).async_scanner_devices_by_address(address, connectable)


@hass_callback
def async_address_present(
    hass: SmartHub, address: str, connectable: bool = True
) -> bool:
    """Check if an address is present in the bluetooth device list."""
    return _get_manager(hass).async_address_present(address, connectable)


@hass_callback
def async_register_callback(
    hass: SmartHub,
    callback: BluetoothCallback,
    match_dict: BluetoothCallbackMatcher | None,
    mode: BluetoothScanningMode,
) -> Callable[[], None]:
    """Register to receive a callback on bluetooth change.

    mode is currently not used as we only support active scanning.
    Passive scanning will be available in the future. The flag
    is required to be present to avoid a future breaking change
    when we support passive scanning.

    Returns a callback that can be used to cancel the registration.
    """
    return _get_manager(hass).async_register_callback(callback, match_dict)


async def async_process_advertisements(
    hass: SmartHub,
    callback: ProcessAdvertisementCallback,
    match_dict: BluetoothCallbackMatcher,
    mode: BluetoothScanningMode,
    timeout: int,
) -> BluetoothServiceInfoBleak:
    """Process advertisements until callback returns true or timeout expires."""
    done: Future[BluetoothServiceInfoBleak] = hass.loop.create_future()

    @hass_callback
    def _async_discovered_device(
        service_info: BluetoothServiceInfoBleak, change: BluetoothChange
    ) -> None:
        if not done.done() and callback(service_info):
            done.set_result(service_info)

    unload = _get_manager(hass).async_register_callback(
        _async_discovered_device, match_dict
    )

    try:
        async with asyncio.timeout(timeout):
            return await done
    finally:
        unload()


@hass_callback
def async_track_unavailable(
    hass: SmartHub,
    callback: Callable[[BluetoothServiceInfoBleak], None],
    address: str,
    connectable: bool = True,
) -> Callable[[], None]:
    """Register to receive a callback when an address is unavailable.

    Returns a callback that can be used to cancel the registration.
    """
    return _get_manager(hass).async_track_unavailable(callback, address, connectable)


@hass_callback
def async_rediscover_address(hass: SmartHub, address: str) -> None:
    """Trigger discovery of devices which have already been seen."""
    _get_manager(hass).async_rediscover_address(address)


@hass_callback
def async_register_scanner(
    hass: SmartHub,
    scanner: BaseHaScanner,
    connection_slots: int | None = None,
    source_domain: str | None = None,
    source_model: str | None = None,
    source_config_entry_id: str | None = None,
    source_device_id: str | None = None,
) -> CALLBACK_TYPE:
    """Register a BleakScanner."""
    return _get_manager(hass).async_register_hass_scanner(
        scanner,
        connection_slots,
        source_domain,
        source_model,
        source_config_entry_id,
        source_device_id,
    )


@hass_callback
def async_remove_scanner(hass: SmartHub, source: str) -> None:
    """Permanently remove a BleakScanner by source address."""
    return _get_manager(hass).async_remove_scanner(source)


@hass_callback
def async_get_advertisement_callback(
    hass: SmartHub,
) -> Callable[[BluetoothServiceInfoBleak], None]:
    """Get the advertisement callback."""
    return _get_manager(hass).scanner_adv_received


@hass_callback
def async_get_learned_advertising_interval(
    hass: SmartHub, address: str
) -> float | None:
    """Get the learned advertising interval for a MAC address."""
    return _get_manager(hass).async_get_learned_advertising_interval(address)


@hass_callback
def async_get_fallback_availability_interval(
    hass: SmartHub, address: str
) -> float | None:
    """Get the fallback availability timeout for a MAC address."""
    return _get_manager(hass).async_get_fallback_availability_interval(address)


@hass_callback
def async_set_fallback_availability_interval(
    hass: SmartHub, address: str, interval: float
) -> None:
    """Override the fallback availability timeout for a MAC address."""
    _get_manager(hass).async_set_fallback_availability_interval(address, interval)
