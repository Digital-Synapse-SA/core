"""Collection of helper methods.

All containing methods are legacy helpers that should not be used by new
components. Instead call the service directly.
"""

from smarthub.components.counter import (
    DOMAIN,
    SERVICE_DECREMENT,
    SERVICE_INCREMENT,
    SERVICE_RESET,
)
from smarthub.const import ATTR_ENTITY_ID
from smarthub.core import SmartHub, callback
from smarthub.loader import bind_hass


@callback
@bind_hass
def async_increment(hass: SmartHub, entity_id: str) -> None:
    """Increment a counter."""
    hass.async_create_task(
        hass.services.async_call(DOMAIN, SERVICE_INCREMENT, {ATTR_ENTITY_ID: entity_id})
    )


@callback
@bind_hass
def async_decrement(hass: SmartHub, entity_id: str) -> None:
    """Decrement a counter."""
    hass.async_create_task(
        hass.services.async_call(DOMAIN, SERVICE_DECREMENT, {ATTR_ENTITY_ID: entity_id})
    )


@callback
@bind_hass
def async_reset(hass: SmartHub, entity_id: str) -> None:
    """Reset a counter."""
    hass.async_create_task(
        hass.services.async_call(DOMAIN, SERVICE_RESET, {ATTR_ENTITY_ID: entity_id})
    )
