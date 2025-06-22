"""Define NextDNS entities."""

from nextdns.model import NextDnsData

from smarthub.helpers.device_registry import DeviceEntryType, DeviceInfo
from smarthub.helpers.entity import EntityDescription
from smarthub.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import NextDnsUpdateCoordinator


class NextDnsEntity[CoordinatorDataT: NextDnsData](
    CoordinatorEntity[NextDnsUpdateCoordinator[CoordinatorDataT]]
):
    """Define NextDNS entity."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: NextDnsUpdateCoordinator[CoordinatorDataT],
        description: EntityDescription,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator)
        self._attr_device_info = DeviceInfo(
            configuration_url=f"https://my.nextdns.io/{coordinator.profile_id}/setup",
            entry_type=DeviceEntryType.SERVICE,
            identifiers={(DOMAIN, str(coordinator.profile_id))},
            manufacturer="NextDNS Inc.",
            name=coordinator.nextdns.get_profile_name(coordinator.profile_id),
        )
        self._attr_unique_id = f"{coordinator.profile_id}_{description.key}"
        self.entity_description = description
