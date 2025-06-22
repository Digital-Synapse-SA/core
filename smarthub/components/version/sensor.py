"""Sensor that can display the current SmartHub versions."""

from __future__ import annotations

from typing import Any

from smarthub.components.sensor import SensorEntity, SensorEntityDescription
from smarthub.const import CONF_NAME
from smarthub.core import SmartHub
from smarthub.helpers.entity_platform import AddConfigEntryEntitiesCallback
from smarthub.helpers.typing import StateType

from .const import CONF_SOURCE, DEFAULT_NAME
from .coordinator import VersionConfigEntry
from .entity import VersionEntity


async def async_setup_entry(
    hass: SmartHub,
    entry: VersionConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up version sensors."""
    coordinator = entry.runtime_data
    if (entity_name := entry.data[CONF_NAME]) == DEFAULT_NAME:
        entity_name = entry.title

    version_sensor_entities: list[VersionSensorEntity] = [
        VersionSensorEntity(
            coordinator=coordinator,
            entity_description=SensorEntityDescription(
                key=str(entry.data[CONF_SOURCE]),
                name=entity_name,
                translation_key="version",
            ),
        )
    ]

    async_add_entities(version_sensor_entities)


class VersionSensorEntity(VersionEntity, SensorEntity):
    """Version sensor entity class."""

    @property
    def native_value(self) -> StateType:
        """Return the native value of this sensor."""
        return self.coordinator.version

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Return extra state attributes of this sensor."""
        return self.coordinator.version_data
