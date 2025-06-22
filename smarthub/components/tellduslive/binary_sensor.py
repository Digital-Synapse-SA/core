"""Support for binary sensors using Tellstick Net."""

from smarthub.components import binary_sensor
from smarthub.components.binary_sensor import BinarySensorEntity
from smarthub.config_entries import ConfigEntry
from smarthub.core import SmartHub
from smarthub.helpers.dispatcher import async_dispatcher_connect
from smarthub.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import DOMAIN, TELLDUS_DISCOVERY_NEW
from .entity import TelldusLiveEntity


async def async_setup_entry(
    hass: SmartHub,
    config_entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up tellduslive sensors dynamically."""

    async def async_discover_binary_sensor(device_id):
        """Discover and add a discovered sensor."""
        client = hass.data[DOMAIN]
        async_add_entities([TelldusLiveSensor(client, device_id)])

    async_dispatcher_connect(
        hass,
        TELLDUS_DISCOVERY_NEW.format(binary_sensor.DOMAIN, DOMAIN),
        async_discover_binary_sensor,
    )


class TelldusLiveSensor(TelldusLiveEntity, BinarySensorEntity):
    """Representation of a Tellstick sensor."""

    _attr_name = None

    @property
    def is_on(self):
        """Return true if switch is on."""
        return self.device.is_on
