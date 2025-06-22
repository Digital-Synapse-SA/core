"""Button platform for CoolMasterNet integration."""

from __future__ import annotations

from smarthub.components.button import ButtonEntity, ButtonEntityDescription
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
    """Set up the CoolMasterNet button platform."""
    coordinator = config_entry.runtime_data
    async_add_entities(
        CoolmasterResetFilter(coordinator, unit_id) for unit_id in coordinator.data
    )


class CoolmasterResetFilter(CoolmasterEntity, ButtonEntity):
    """Reset the clean filter timer (once filter was cleaned)."""

    entity_description = ButtonEntityDescription(
        key="reset_filter",
        translation_key="reset_filter",
        entity_category=EntityCategory.CONFIG,
    )

    async def async_press(self) -> None:
        """Press the button."""
        await self._unit.reset_filter()
        await self.coordinator.async_refresh()
