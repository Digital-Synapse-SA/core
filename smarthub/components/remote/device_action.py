"""Provides device actions for remotes."""

from __future__ import annotations

import voluptuous as vol

from smarthub.components.device_automation import (
    async_validate_entity_schema,
    toggle_entity,
)
from smarthub.const import CONF_DOMAIN
from smarthub.core import Context, SmartHub
from smarthub.helpers.typing import ConfigType, TemplateVarsType

from . import DOMAIN

# mypy: disallow-any-generics

_ACTION_SCHEMA = toggle_entity.ACTION_SCHEMA.extend({vol.Required(CONF_DOMAIN): DOMAIN})


async def async_validate_action_config(
    hass: SmartHub, config: ConfigType
) -> ConfigType:
    """Validate config."""
    return async_validate_entity_schema(hass, config, _ACTION_SCHEMA)


async def async_call_action_from_config(
    hass: SmartHub,
    config: ConfigType,
    variables: TemplateVarsType,
    context: Context | None,
) -> None:
    """Change state based on configuration."""
    await toggle_entity.async_call_action_from_config(
        hass, config, variables, context, DOMAIN
    )


async def async_get_actions(
    hass: SmartHub, device_id: str
) -> list[dict[str, str]]:
    """List device actions."""
    return await toggle_entity.async_get_actions(hass, device_id, DOMAIN)
