"""Collection of helper methods.

All containing methods are legacy helpers that should not be used by new
components. Instead call the service directly.
"""

from smarthub.components.image_processing import DOMAIN, SERVICE_SCAN
from smarthub.const import ATTR_ENTITY_ID, ENTITY_MATCH_ALL
from smarthub.core import SmartHub, callback
from smarthub.loader import bind_hass


@bind_hass
def scan(hass: SmartHub, entity_id: str = ENTITY_MATCH_ALL) -> None:
    """Force process of all cameras or given entity."""
    hass.add_job(async_scan, hass, entity_id)


@callback
@bind_hass
def async_scan(hass: SmartHub, entity_id: str = ENTITY_MATCH_ALL) -> None:
    """Force process of all cameras or given entity."""
    data = {ATTR_ENTITY_ID: entity_id} if entity_id else None
    hass.async_create_task(hass.services.async_call(DOMAIN, SERVICE_SCAN, data))
