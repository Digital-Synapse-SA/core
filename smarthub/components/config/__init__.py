"""Component to configure SmartHub via an API."""

from __future__ import annotations

from smarthub.components import frontend
from smarthub.const import EVENT_COMPONENT_LOADED
from smarthub.core import SmartHub
from smarthub.helpers import config_validation as cv
from smarthub.helpers.typing import ConfigType
from smarthub.setup import EventComponentLoaded

from . import (
    area_registry,
    auth,
    auth_provider_smarthub,
    automation,
    category_registry,
    config_entries,
    core,
    device_registry,
    entity_registry,
    floor_registry,
    label_registry,
    scene,
    script,
)
from .const import DOMAIN

SECTIONS = (
    area_registry,
    auth,
    auth_provider_smarthub,
    automation,
    category_registry,
    config_entries,
    core,
    device_registry,
    entity_registry,
    floor_registry,
    label_registry,
    script,
    scene,
)


CONFIG_SCHEMA = cv.empty_config_schema(DOMAIN)


async def async_setup(hass: SmartHub, config: ConfigType) -> bool:
    """Set up the config component."""
    frontend.async_register_built_in_panel(
        hass, "config", "config", "hass:cog", require_admin=True
    )

    for panel in SECTIONS:
        if panel.async_setup(hass):
            name = panel.__name__.split(".")[-1]
            key = f"{DOMAIN}.{name}"
            hass.bus.async_fire(
                EVENT_COMPONENT_LOADED, EventComponentLoaded(component=key)
            )

    return True
