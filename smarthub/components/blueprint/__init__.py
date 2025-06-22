"""The blueprint integration."""

from smarthub.core import SmartHub
from smarthub.helpers import config_validation as cv
from smarthub.helpers.typing import ConfigType

from . import websocket_api
from .const import CONF_USE_BLUEPRINT, DOMAIN  # noqa: F401
from .errors import (  # noqa: F401
    BlueprintException,
    BlueprintInUse,
    BlueprintWithNameException,
    FailedToLoad,
    InvalidBlueprint,
    InvalidBlueprintInputs,
    MissingInput,
)
from .models import Blueprint, BlueprintInputs, DomainBlueprints  # noqa: F401
from .schemas import (  # noqa: F401
    BLUEPRINT_INSTANCE_FIELDS,
    BLUEPRINT_SCHEMA,
    is_blueprint_instance_config,
)

CONFIG_SCHEMA = cv.empty_config_schema(DOMAIN)


async def async_setup(hass: SmartHub, config: ConfigType) -> bool:
    """Set up the blueprint integration."""
    websocket_api.async_setup(hass)
    return True
