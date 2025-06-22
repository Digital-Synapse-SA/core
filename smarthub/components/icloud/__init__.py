"""The iCloud component."""

from __future__ import annotations

from typing import Any

from smarthub.const import CONF_PASSWORD, CONF_USERNAME
from smarthub.core import SmartHub
from smarthub.helpers import config_validation as cv
from smarthub.helpers.storage import Store
from smarthub.helpers.typing import ConfigType

from .account import IcloudAccount, IcloudConfigEntry
from .const import (
    CONF_GPS_ACCURACY_THRESHOLD,
    CONF_MAX_INTERVAL,
    CONF_WITH_FAMILY,
    DOMAIN,
    PLATFORMS,
    STORAGE_KEY,
    STORAGE_VERSION,
)
from .services import async_setup_services

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup(hass: SmartHub, config: ConfigType) -> bool:
    """Set up iCloud integration."""

    async_setup_services(hass)

    return True


async def async_setup_entry(hass: SmartHub, entry: IcloudConfigEntry) -> bool:
    """Set up an iCloud account from a config entry."""

    username = entry.data[CONF_USERNAME]
    password = entry.data[CONF_PASSWORD]
    with_family = entry.data[CONF_WITH_FAMILY]
    max_interval = entry.data[CONF_MAX_INTERVAL]
    gps_accuracy_threshold = entry.data[CONF_GPS_ACCURACY_THRESHOLD]

    # For backwards compat
    if entry.unique_id is None:
        hass.config_entries.async_update_entry(entry, unique_id=username)

    icloud_dir = Store[Any](hass, STORAGE_VERSION, STORAGE_KEY)

    account = IcloudAccount(
        hass,
        username,
        password,
        icloud_dir,
        with_family,
        max_interval,
        gps_accuracy_threshold,
        entry,
    )
    await hass.async_add_executor_job(account.setup)

    entry.runtime_data = account

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: SmartHub, entry: IcloudConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
