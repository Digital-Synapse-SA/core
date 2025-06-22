"""The songpal component."""

import voluptuous as vol

from smarthub.config_entries import SOURCE_IMPORT, ConfigEntry
from smarthub.const import CONF_NAME, Platform
from smarthub.core import SmartHub
from smarthub.helpers import config_validation as cv
from smarthub.helpers.typing import ConfigType

from .const import CONF_ENDPOINT, DOMAIN

SONGPAL_CONFIG_SCHEMA = vol.Schema(
    {vol.Optional(CONF_NAME): cv.string, vol.Required(CONF_ENDPOINT): cv.string}
)

CONFIG_SCHEMA = vol.Schema(
    {vol.Optional(DOMAIN): vol.All(cv.ensure_list, [SONGPAL_CONFIG_SCHEMA])},
    extra=vol.ALLOW_EXTRA,
)

PLATFORMS = [Platform.MEDIA_PLAYER]


async def async_setup(hass: SmartHub, config: ConfigType) -> bool:
    """Set up songpal environment."""
    if (conf := config.get(DOMAIN)) is None:
        return True
    for config_entry in conf:
        hass.async_create_task(
            hass.config_entries.flow.async_init(
                DOMAIN,
                context={"source": SOURCE_IMPORT},
                data=config_entry,
            ),
        )
    return True


async def async_setup_entry(hass: SmartHub, entry: ConfigEntry) -> bool:
    """Set up songpal media player."""
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: SmartHub, entry: ConfigEntry) -> bool:
    """Unload songpal media player."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
