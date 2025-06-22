"""Collection of helper methods.

All containing methods are legacy helpers that should not be used by new
components. Instead call the service directly.
"""

from smarthub.components.water_heater import (
    _LOGGER,
    ATTR_AWAY_MODE,
    ATTR_OPERATION_MODE,
    DOMAIN,
    SERVICE_SET_AWAY_MODE,
    SERVICE_SET_OPERATION_MODE,
    SERVICE_SET_TEMPERATURE,
    SERVICE_TURN_OFF,
    SERVICE_TURN_ON,
)
from smarthub.const import ATTR_ENTITY_ID, ATTR_TEMPERATURE, ENTITY_MATCH_ALL
from smarthub.core import SmartHub


async def async_set_away_mode(
    hass: SmartHub, away_mode: bool, entity_id: str = ENTITY_MATCH_ALL
) -> None:
    """Turn all or specified water_heater devices away mode on."""
    data = {ATTR_AWAY_MODE: away_mode}

    if entity_id:
        data[ATTR_ENTITY_ID] = entity_id

    await hass.services.async_call(DOMAIN, SERVICE_SET_AWAY_MODE, data, blocking=True)


async def async_set_temperature(
    hass: SmartHub,
    temperature: float,
    entity_id: str = ENTITY_MATCH_ALL,
    operation_mode: str | None = None,
) -> None:
    """Set new target temperature."""
    kwargs = {
        key: value
        for key, value in (
            (ATTR_TEMPERATURE, temperature),
            (ATTR_ENTITY_ID, entity_id),
            (ATTR_OPERATION_MODE, operation_mode),
        )
        if value is not None
    }
    _LOGGER.debug("set_temperature start data=%s", kwargs)
    await hass.services.async_call(
        DOMAIN, SERVICE_SET_TEMPERATURE, kwargs, blocking=True
    )


async def async_set_operation_mode(
    hass: SmartHub, operation_mode: str, entity_id: str = ENTITY_MATCH_ALL
) -> None:
    """Set new target operation mode."""
    data = {ATTR_OPERATION_MODE: operation_mode}

    if entity_id is not None:
        data[ATTR_ENTITY_ID] = entity_id

    await hass.services.async_call(
        DOMAIN, SERVICE_SET_OPERATION_MODE, data, blocking=True
    )


async def async_turn_on(hass: SmartHub, entity_id: str = ENTITY_MATCH_ALL) -> None:
    """Turn all or specified water_heater devices on."""
    data = {}

    if entity_id:
        data[ATTR_ENTITY_ID] = entity_id

    await hass.services.async_call(DOMAIN, SERVICE_TURN_ON, data, blocking=True)


async def async_turn_off(
    hass: SmartHub, entity_id: str = ENTITY_MATCH_ALL
) -> None:
    """Turn all or specified water_heater devices off."""
    data = {}

    if entity_id:
        data[ATTR_ENTITY_ID] = entity_id

    await hass.services.async_call(DOMAIN, SERVICE_TURN_OFF, data, blocking=True)
