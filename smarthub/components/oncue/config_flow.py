"""The Oncue integration."""

from smarthub.config_entries import ConfigFlow

from . import DOMAIN


class OncueConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Oncue."""

    VERSION = 1
