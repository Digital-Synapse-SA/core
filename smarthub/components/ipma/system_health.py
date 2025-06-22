"""Provide info to system health."""

from smarthub.components import system_health
from smarthub.core import SmartHub, callback

IPMA_API_URL = "http://api.ipma.pt"


@callback
def async_register(
    hass: SmartHub, register: system_health.SystemHealthRegistration
) -> None:
    """Register system health callbacks."""
    register.async_register_info(system_health_info)


async def system_health_info(hass):
    """Get info for the info page."""
    return {
        "api_endpoint_reachable": system_health.async_check_can_reach_url(
            hass, IPMA_API_URL
        )
    }
