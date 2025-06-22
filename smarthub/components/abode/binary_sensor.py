"""Support for Abode Security System binary sensors."""

from __future__ import annotations

from typing import cast

from jaraco.abode.devices.binary_sensor import BinarySensor

from smarthub.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from smarthub.config_entries import ConfigEntry
from smarthub.core import SmartHub
from smarthub.helpers.entity_platform import AddConfigEntryEntitiesCallback
from smarthub.util.enum import try_parse_enum

from . import AbodeSystem
from .const import DOMAIN
from .entity import AbodeDevice


async def async_setup_entry(
    hass: SmartHub,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Abode binary sensor devices."""
    data: AbodeSystem = hass.data[DOMAIN]

    device_types = [
        "connectivity",
        "moisture",
        "motion",
        "occupancy",
        "door",
    ]

    async_add_entities(
        AbodeBinarySensor(data, device)
        for device in data.abode.get_devices(generic_type=device_types)
    )


class AbodeBinarySensor(AbodeDevice, BinarySensorEntity):
    """A binary sensor implementation for Abode device."""

    _attr_name = None
    _device: BinarySensor

    @property
    def is_on(self) -> bool:
        """Return True if the binary sensor is on."""
        return cast(bool, self._device.is_on)

    @property
    def device_class(self) -> BinarySensorDeviceClass | None:
        """Return the class of the binary sensor."""
        if self._device.get_value("is_window") == "1":
            return BinarySensorDeviceClass.WINDOW
        return try_parse_enum(BinarySensorDeviceClass, self._device.generic_type)
