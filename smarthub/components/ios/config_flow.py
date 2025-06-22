"""Config flow for iOS."""

from smarthub.helpers import config_entry_flow

from .const import DOMAIN

config_entry_flow.register_discovery_flow(
    DOMAIN, "SmartHub iOS", lambda hass: True
)
