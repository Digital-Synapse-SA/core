"""Button entity to set the time of the Alpha2 base."""

from smarthub.components.button import ButtonEntity
from smarthub.config_entries import ConfigEntry
from smarthub.const import EntityCategory
from smarthub.core import SmartHub
from smarthub.helpers.entity_platform import AddConfigEntryEntitiesCallback
from smarthub.helpers.update_coordinator import CoordinatorEntity
from smarthub.util import dt as dt_util

from .const import DOMAIN
from .coordinator import Alpha2BaseCoordinator


async def async_setup_entry(
    hass: SmartHub,
    config_entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Add Alpha2 button entities."""

    coordinator: Alpha2BaseCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    async_add_entities([Alpha2TimeSyncButton(coordinator, config_entry.entry_id)])


class Alpha2TimeSyncButton(CoordinatorEntity[Alpha2BaseCoordinator], ButtonEntity):
    """Alpha2 virtual time sync button."""

    _attr_name = "Sync time"
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, coordinator: Alpha2BaseCoordinator, entry_id: str) -> None:
        """Initialize Alpha2TimeSyncButton."""
        super().__init__(coordinator)

        self._attr_unique_id = f"{entry_id}:sync_time"

    async def async_press(self) -> None:
        """Synchronize current local time from HA instance to base station."""
        await self.coordinator.base.set_datetime(dt_util.now())
