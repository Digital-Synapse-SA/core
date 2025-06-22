"""Sensor platform for CoolMasterNet integration."""

from __future__ import annotations

from smarthub.components.sensor import SensorEntity, SensorEntityDescription
from smarthub.const import EntityCategory
from smarthub.core import SmartHub
from smarthub.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .coordinator import CoolmasterConfigEntry
from .entity import CoolmasterEntity


async def async_setup_entry(
    hass: SmartHub,
    config_entry: CoolmasterConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the CoolMasterNet sensor platform."""
    coordinator = config_entry.runtime_data
    async_add_entities(
        CoolmasterCleanFilter(coordinator, unit_id) for unit_id in coordinator.data
    )


class CoolmasterCleanFilter(CoolmasterEntity, SensorEntity):
    """Representation of a unit's error code."""

    entity_description = SensorEntityDescription(
        key="error_code",
        translation_key="error_code",
        entity_category=EntityCategory.DIAGNOSTIC,
    )

    @property
    def native_value(self) -> str:
        """Return the error code or OK."""
        return self._unit.error_code or "OK"
