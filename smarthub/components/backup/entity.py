"""Base for backup entities."""

from __future__ import annotations

from smarthub.const import __version__ as HA_VERSION
from smarthub.helpers.device_registry import DeviceEntryType, DeviceInfo
from smarthub.helpers.entity import EntityDescription
from smarthub.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import BackupDataUpdateCoordinator


class BackupManagerBaseEntity(CoordinatorEntity[BackupDataUpdateCoordinator]):
    """Base entity for backup manager."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: BackupDataUpdateCoordinator,
    ) -> None:
        """Initialize base entity."""
        super().__init__(coordinator)
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, "backup_manager")},
            manufacturer="SmartHub",
            model="SmartHub Backup",
            sw_version=HA_VERSION,
            name="Backup",
            entry_type=DeviceEntryType.SERVICE,
            configuration_url="smarthub://config/backup",
        )


class BackupManagerEntity(BackupManagerBaseEntity):
    """Entity for backup manager."""

    def __init__(
        self,
        coordinator: BackupDataUpdateCoordinator,
        entity_description: EntityDescription,
    ) -> None:
        """Initialize entity."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = entity_description.key
