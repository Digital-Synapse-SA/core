"""Provides device triggers for remotes."""

from __future__ import annotations

import voluptuous as vol

from smarthub.components.device_automation import toggle_entity
from smarthub.const import CONF_DOMAIN
from smarthub.core import CALLBACK_TYPE, SmartHub
from smarthub.helpers.trigger import TriggerActionType, TriggerInfo
from smarthub.helpers.typing import ConfigType

from . import DOMAIN

TRIGGER_SCHEMA = vol.All(
    toggle_entity.TRIGGER_SCHEMA,
    vol.Schema({vol.Required(CONF_DOMAIN): DOMAIN}, extra=vol.ALLOW_EXTRA),
)


async def async_attach_trigger(
    hass: SmartHub,
    config: ConfigType,
    action: TriggerActionType,
    trigger_info: TriggerInfo,
) -> CALLBACK_TYPE:
    """Listen for state changes based on configuration."""
    return await toggle_entity.async_attach_trigger(hass, config, action, trigger_info)


async def async_get_triggers(
    hass: SmartHub, device_id: str
) -> list[dict[str, str]]:
    """List device triggers."""
    return await toggle_entity.async_get_triggers(hass, device_id, DOMAIN)


async def async_get_trigger_capabilities(
    hass: SmartHub, config: ConfigType
) -> dict[str, vol.Schema]:
    """List trigger capabilities."""
    return await toggle_entity.async_get_trigger_capabilities(hass, config)
