"""Support for tracking MySensors devices."""

from __future__ import annotations

from smarthub.components.device_tracker import TrackerEntity
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
        """Discover and add a MySensors device tracker."""
        setup_mysensors_platform(
            hass,
            Platform.DEVICE_TRACKER,
            discovery_info,
            MySensorsDeviceTracker,
            async_add_entities=async_add_entities,
        )

    config_entry.async_on_unload(
        async_dispatcher_connect(
            hass,
            MYSENSORS_DISCOVERY.format(config_entry.entry_id, Platform.DEVICE_TRACKER),
            async_discover,
        ),
    )


class MySensorsDeviceTracker(MySensorsChildEntity, TrackerEntity):
    """Represent a MySensors device tracker."""

    @callback
    def _async_update(self) -> None:
        """Update the controller with the latest value from a device."""
        super()._async_update()
        node = self.gateway.sensors[self.node_id]
        child = node.children[self.child_id]
        position: str = child.values[self.value_type]
        latitude, longitude, _ = position.split(",")
        self._attr_latitude = float(latitude)
        self._attr_longitude = float(longitude)
