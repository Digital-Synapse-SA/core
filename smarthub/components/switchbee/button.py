"""Support for SwitchBee scenario button."""

from switchbee.api.central_unit import SwitchBeeError
from switchbee.device import ApiStateCommand, DeviceType

from smarthub.components.button import ButtonEntity
from smarthub.config_entries import ConfigEntry
from smarthub.core import SmartHub
from smarthub.exceptions import SmartHubError
from smarthub.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import DOMAIN
from .coordinator import SwitchBeeCoordinator
from .entity import SwitchBeeEntity


async def async_setup_entry(
    hass: SmartHub,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Switchbee button."""
    coordinator: SwitchBeeCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        SwitchBeeButton(switchbee_device, coordinator)
        for switchbee_device in coordinator.data.values()
        if switchbee_device.type == DeviceType.Scenario
    )


class SwitchBeeButton(SwitchBeeEntity, ButtonEntity):
    """Representation of an Switchbee button."""

    async def async_press(self) -> None:
        """Fire the scenario in the SwitchBee hub."""
        try:
            await self.coordinator.api.set_state(self._device.id, ApiStateCommand.ON)
        except SwitchBeeError as exp:
            raise SmartHubError(
                f"Failed to fire scenario {self.name}, {exp!s}"
            ) from exp
