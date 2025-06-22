"""Support for Twilio."""

from aiohttp import web
from twilio.rest import Client
import voluptuous as vol

from smarthub.components import webhook
from smarthub.config_entries import ConfigEntry
from smarthub.const import CONF_WEBHOOK_ID
from smarthub.core import SmartHub
from smarthub.helpers import config_entry_flow, config_validation as cv
from smarthub.helpers.typing import ConfigType

from .const import DOMAIN

CONF_ACCOUNT_SID = "account_sid"
CONF_AUTH_TOKEN = "auth_token"

DATA_TWILIO = DOMAIN

RECEIVED_DATA = f"{DOMAIN}_data_received"

CONFIG_SCHEMA = vol.Schema(
    {
        vol.Optional(DOMAIN): vol.Schema(
            {
                vol.Required(CONF_ACCOUNT_SID): cv.string,
                vol.Required(CONF_AUTH_TOKEN): cv.string,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)


async def async_setup(hass: SmartHub, config: ConfigType) -> bool:
    """Set up the Twilio component."""
    if DOMAIN not in config:
        return True

    conf = config[DOMAIN]
    hass.data[DATA_TWILIO] = Client(
        conf.get(CONF_ACCOUNT_SID), conf.get(CONF_AUTH_TOKEN)
    )
    return True


async def handle_webhook(
    hass: SmartHub, webhook_id: str, request: web.Request
) -> web.Response:
    """Handle incoming webhook from Twilio for inbound messages and calls."""
    data = dict(await request.post())
    data["webhook_id"] = webhook_id
    hass.bus.async_fire(RECEIVED_DATA, dict(data))

    return web.Response(text="")


async def async_setup_entry(hass: SmartHub, entry: ConfigEntry) -> bool:
    """Configure based on config entry."""
    webhook.async_register(
        hass, DOMAIN, "Twilio", entry.data[CONF_WEBHOOK_ID], handle_webhook
    )
    return True


async def async_unload_entry(hass: SmartHub, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    webhook.async_unregister(hass, entry.data[CONF_WEBHOOK_ID])
    return True


async_remove_entry = config_entry_flow.webhook_async_remove_entry
