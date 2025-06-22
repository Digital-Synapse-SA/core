"""Config flow for National Weather Service (NWS) integration."""

from __future__ import annotations

import logging
from typing import Any

import aiohttp
from pynws import SimpleNWS
import voluptuous as vol

from smarthub.config_entries import ConfigFlow, ConfigFlowResult
from smarthub.const import CONF_API_KEY, CONF_LATITUDE, CONF_LONGITUDE
from smarthub.core import SmartHub
from smarthub.exceptions import SmartHubError
from smarthub.helpers import config_validation as cv
from smarthub.helpers.aiohttp_client import async_get_clientsession

from . import base_unique_id
from .const import CONF_STATION, DOMAIN

_LOGGER = logging.getLogger(__name__)


async def validate_input(hass: SmartHub, data: dict[str, Any]) -> dict[str, str]:
    """Validate the user input allows us to connect.

    Data has the keys from DATA_SCHEMA with values provided by the user.
    """
    latitude = data[CONF_LATITUDE]
    longitude = data[CONF_LONGITUDE]
    api_key = data[CONF_API_KEY]
    station = data.get(CONF_STATION)

    client_session = async_get_clientsession(hass)
    ha_api_key = f"{api_key} smarthub"
    nws = SimpleNWS(latitude, longitude, ha_api_key, client_session)

    try:
        await nws.set_station(station)
    except aiohttp.ClientError as err:
        _LOGGER.error("Could not connect: %s", err)
        raise CannotConnect from err

    return {"title": nws.station}


class NWSConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for National Weather Service (NWS)."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            await self.async_set_unique_id(
                base_unique_id(user_input[CONF_LATITUDE], user_input[CONF_LONGITUDE])
            )
            self._abort_if_unique_id_configured()
            try:
                info = await validate_input(self.hass, user_input)
                user_input[CONF_STATION] = info["title"]
                return self.async_create_entry(title=info["title"], data=user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        data_schema = vol.Schema(
            {
                vol.Required(CONF_API_KEY): str,
                vol.Required(
                    CONF_LATITUDE, default=self.hass.config.latitude
                ): cv.latitude,
                vol.Required(
                    CONF_LONGITUDE, default=self.hass.config.longitude
                ): cv.longitude,
                vol.Optional(CONF_STATION): str,
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )


class CannotConnect(SmartHubError):
    """Error to indicate we cannot connect."""
