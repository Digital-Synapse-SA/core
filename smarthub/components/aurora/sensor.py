"""Support for Aurora Forecast sensor."""

from __future__ import annotations

from smarthub.components.sensor import SensorEntity, SensorStateClass
from smarthub.const import PERCENTAGE
from smarthub.core import SmartHub
from smarthub.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .coordinator import AuroraConfigEntry
from .entity import AuroraEntity


async def async_setup_entry(
    hass: SmartHub,
    entry: AuroraConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the sensor platform."""

    async_add_entities(
        [
            AuroraSensor(
                coordinator=entry.runtime_data,
                translation_key="visibility",
            )
        ]
    )


class AuroraSensor(AuroraEntity, SensorEntity):
    """Implementation of an aurora sensor."""

    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self) -> int:
        """Return % chance the aurora is visible."""
        return self.coordinator.data
