"""The Google Drive integration."""

from __future__ import annotations

from collections.abc import Callable

from google_drive_api.exceptions import GoogleDriveApiError

from smarthub.config_entries import ConfigEntry
from smarthub.core import SmartHub
from smarthub.exceptions import ConfigEntryNotReady
from smarthub.helpers import instance_id
from smarthub.helpers.aiohttp_client import async_get_clientsession
from smarthub.helpers.config_entry_oauth2_flow import (
    OAuth2Session,
    async_get_config_entry_implementation,
)
from smarthub.util.hass_dict import HassKey

from .api import AsyncConfigEntryAuth, DriveClient
from .const import DOMAIN

DATA_BACKUP_AGENT_LISTENERS: HassKey[list[Callable[[], None]]] = HassKey(
    f"{DOMAIN}.backup_agent_listeners"
)


type GoogleDriveConfigEntry = ConfigEntry[DriveClient]


async def async_setup_entry(hass: SmartHub, entry: GoogleDriveConfigEntry) -> bool:
    """Set up Google Drive from a config entry."""
    auth = AsyncConfigEntryAuth(
        async_get_clientsession(hass),
        OAuth2Session(
            hass, entry, await async_get_config_entry_implementation(hass, entry)
        ),
    )

    # Test we can refresh the token and raise ConfigEntryAuthFailed or ConfigEntryNotReady if not
    await auth.async_get_access_token()

    client = DriveClient(await instance_id.async_get(hass), auth)
    entry.runtime_data = client

    # Test we can access Google Drive and raise if not
    try:
        await client.async_create_ha_root_folder_if_not_exists()
    except GoogleDriveApiError as err:
        raise ConfigEntryNotReady from err

    def async_notify_backup_listeners() -> None:
        for listener in hass.data.get(DATA_BACKUP_AGENT_LISTENERS, []):
            listener()

    entry.async_on_unload(entry.async_on_state_change(async_notify_backup_listeners))

    return True


async def async_unload_entry(
    hass: SmartHub, entry: GoogleDriveConfigEntry
) -> bool:
    """Unload a config entry."""
    return True
