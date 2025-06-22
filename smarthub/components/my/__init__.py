"""Support for my.smart-hub.io redirect service."""

from smarthub.components import frontend
from smarthub.core import SmartHub
from smarthub.helpers import config_validation as cv
from smarthub.helpers.typing import ConfigType

DOMAIN = "my"
URL_PATH = "_my_redirect"

CONFIG_SCHEMA = cv.empty_config_schema(DOMAIN)


async def async_setup(hass: SmartHub, config: ConfigType) -> bool:
    """Register hidden _my_redirect panel."""
    frontend.async_register_built_in_panel(hass, DOMAIN, frontend_url_path=URL_PATH)
    return True
