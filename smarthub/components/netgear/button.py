"""Support for Netgear Button."""

from collections.abc import Callable, Coroutine
from dataclasses import dataclass
from typing import Any

from smarthub.components.button import (
    ButtonDeviceClass,
    ButtonEntity,
    ButtonEntityDescription,
)
from smarthub.config_entries import ConfigEntry
from smarthub.const import EntityCategory
from smarthub.core import SmartHub, callback
from smarthub.helpers.entity_platform import AddConfigEntryEntitiesCallback
from smarthub.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN, KEY_COORDINATOR, KEY_ROUTER
from .entity import NetgearRouterCoordinatorEntity
from .router import NetgearRouter


@dataclass(frozen=True, kw_only=True)
class NetgearButtonEntityDescription(ButtonEntityDescription):
    """Class describing Netgear button entities."""

    action: Callable[[NetgearRouter], Callable[[], Coroutine[Any, Any, None]]]


BUTTONS = [
    NetgearButtonEntityDescription(
        key="reboot",
        device_class=ButtonDeviceClass.RESTART,
        entity_category=EntityCategory.CONFIG,
        action=lambda router: router.async_reboot,
    )
]


async def async_setup_entry(
    hass: SmartHub,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up button for Netgear component."""
    router = hass.data[DOMAIN][entry.entry_id][KEY_ROUTER]
    coordinator = hass.data[DOMAIN][entry.entry_id][KEY_COORDINATOR]
    async_add_entities(
        NetgearRouterButtonEntity(coordinator, router, entity_description)
        for entity_description in BUTTONS
    )


class NetgearRouterButtonEntity(NetgearRouterCoordinatorEntity, ButtonEntity):
    """Netgear Router button entity."""

    entity_description: NetgearButtonEntityDescription

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        router: NetgearRouter,
        entity_description: NetgearButtonEntityDescription,
    ) -> None:
        """Initialize a Netgear device."""
        super().__init__(coordinator, router)
        self.entity_description = entity_description
        self._attr_unique_id = f"{router.serial_number}-{entity_description.key}"

    async def async_press(self) -> None:
        """Triggers the button press service."""
        async_action = self.entity_description.action(self._router)
        await async_action()

    @callback
    def async_update_device(self) -> None:
        """Update the Netgear device."""
