"""Provide info to system health."""

from __future__ import annotations

from typing import Any, Final

from smarthub.components import system_health
from smarthub.core import SmartHub, callback

API_ENDPOINT: Final = "http://api.gios.gov.pl/"


@callback
def async_register(
    hass: SmartHub, register: system_health.SystemHealthRegistration
) -> None:
    """Register system health callbacks."""
    register.async_register_info(system_health_info)


async def system_health_info(hass: SmartHub) -> dict[str, Any]:
    """Get info for the info page."""
    return {
        "can_reach_server": system_health.async_check_can_reach_url(hass, API_ENDPOINT)
    }
