"""Support for xiaomi ble."""

from typing import TYPE_CHECKING

from smarthub.config_entries import ConfigEntry

if TYPE_CHECKING:
    from .coordinator import XiaomiActiveBluetoothProcessorCoordinator

type XiaomiBLEConfigEntry = ConfigEntry[XiaomiActiveBluetoothProcessorCoordinator]
