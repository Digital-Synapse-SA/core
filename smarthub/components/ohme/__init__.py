"""Set up ohme integration."""

from ohme import ApiException, AuthException, OhmeApiClient

from smarthub.const import CONF_EMAIL, CONF_PASSWORD
from smarthub.core import SmartHub
from smarthub.exceptions import ConfigEntryAuthFailed, ConfigEntryNotReady
from smarthub.helpers import config_validation as cv
from smarthub.helpers.aiohttp_client import async_get_clientsession
from smarthub.helpers.typing import ConfigType

from .const import DOMAIN, PLATFORMS
from .coordinator import (
    OhmeAdvancedSettingsCoordinator,
    OhmeChargeSessionCoordinator,
    OhmeConfigEntry,
    OhmeDeviceInfoCoordinator,
    OhmeRuntimeData,
)
from .services import async_setup_services

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup(hass: SmartHub, config: ConfigType) -> bool:
    """Set up Ohme integration."""
    async_setup_services(hass)

    return True


async def async_setup_entry(hass: SmartHub, entry: OhmeConfigEntry) -> bool:
    """Set up Ohme from a config entry."""

    client = OhmeApiClient(
        email=entry.data[CONF_EMAIL],
        password=entry.data[CONF_PASSWORD],
        session=async_get_clientsession(hass),
    )

    try:
        await client.async_login()

        if not await client.async_update_device_info():
            raise ConfigEntryNotReady(
                translation_key="device_info_failed", translation_domain=DOMAIN
            )
    except AuthException as e:
        raise ConfigEntryAuthFailed(
            translation_key="auth_failed", translation_domain=DOMAIN
        ) from e
    except ApiException as e:
        raise ConfigEntryNotReady(
            translation_key="api_failed", translation_domain=DOMAIN
        ) from e

    coordinators = (
        OhmeChargeSessionCoordinator(hass, entry, client),
        OhmeAdvancedSettingsCoordinator(hass, entry, client),
        OhmeDeviceInfoCoordinator(hass, entry, client),
    )

    for coordinator in coordinators:
        await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = OhmeRuntimeData(*coordinators)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: SmartHub, entry: OhmeConfigEntry) -> bool:
    """Unload a config entry."""

    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
