"""Obihai button module."""

from __future__ import annotations

from smarthub.components.button import (
    ButtonDeviceClass,
    ButtonEntity,
    ButtonEntityDescription,
)
from smarthub.config_entries import ConfigEntry
from smarthub.const import EntityCategory
from smarthub.core import SmartHub
from smarthub.exceptions import SmartHubError
from smarthub.helpers import entity_platform

from .connectivity import ObihaiConnection
from .const import DOMAIN, OBIHAI

BUTTON_DESCRIPTION = ButtonEntityDescription(
    key="reboot",
    name=f"{OBIHAI} Reboot",
    device_class=ButtonDeviceClass.RESTART,
    entity_category=EntityCategory.CONFIG,
)


async def async_setup_entry(
    hass: SmartHub,
    entry: ConfigEntry,
    async_add_entities: entity_platform.AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the Obihai sensor entries."""

    requester: ObihaiConnection = hass.data[DOMAIN][entry.entry_id]

    buttons = [ObihaiButton(requester)]
    async_add_entities(buttons, update_before_add=True)


class ObihaiButton(ButtonEntity):
    """Obihai Reboot button."""

    entity_description = BUTTON_DESCRIPTION

    def __init__(self, requester: ObihaiConnection) -> None:
        """Initialize monitor sensor."""
        self.requester = requester
        self._pyobihai = requester.pyobihai
        self._attr_unique_id = f"{requester.serial}-reboot"

    def press(self) -> None:
        """Press button."""

        if not self._pyobihai.call_reboot():
            raise SmartHubError("Reboot failed!")
