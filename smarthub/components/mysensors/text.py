"""Provide a text platform for MySensors."""

from __future__ import annotations

from smarthub.components.text import TextEntity
from smarthub.config_entries import ConfigEntry
from smarthub.const import Platform
from smarthub.core import SmartHub, callback
from smarthub.helpers.dispatcher import async_dispatcher_connect
from smarthub.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import setup_mysensors_platform
from .const import MYSENSORS_DISCOVERY, DiscoveryInfo
from .entity import MySensorsChildEntity


async def async_setup_entry(
    hass: SmartHub,
    config_entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up this platform for a specific ConfigEntry(==Gateway)."""

    @callback
    def async_discover(discovery_info: DiscoveryInfo) -> None:
        """Discover and add a MySensors text entity."""
        setup_mysensors_platform(
            hass,
            Platform.TEXT,
            discovery_info,
            MySensorsText,
            async_add_entities=async_add_entities,
        )

    config_entry.async_on_unload(
        async_dispatcher_connect(
            hass,
            MYSENSORS_DISCOVERY.format(config_entry.entry_id, Platform.TEXT),
            async_discover,
        ),
    )


class MySensorsText(MySensorsChildEntity, TextEntity):
    """Representation of the value of a MySensors Text child node."""

    _attr_native_max = 25

    @property
    def native_value(self) -> str | None:
        """Return the value reported by the text."""
        return self._values.get(self.value_type)

    async def async_set_value(self, value: str) -> None:
        """Change the value."""
        self.gateway.set_child_value(
            self.node_id, self.child_id, self.value_type, value, ack=1
        )
