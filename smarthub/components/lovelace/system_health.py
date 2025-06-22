"""Provide info to system health."""

import asyncio
from typing import Any

from smarthub.components import system_health
from smarthub.const import CONF_MODE
from smarthub.core import SmartHub, callback

from .const import LOVELACE_DATA, MODE_AUTO, MODE_STORAGE, MODE_YAML


@callback
def async_register(
    hass: SmartHub, register: system_health.SystemHealthRegistration
) -> None:
    """Register system health callbacks."""
    register.async_register_info(system_health_info, "/config/lovelace")


async def system_health_info(hass: SmartHub) -> dict[str, Any]:
    """Get info for the info page."""
    health_info: dict[str, Any] = {
        "dashboards": len(hass.data[LOVELACE_DATA].dashboards)
    }
    health_info.update(await hass.data[LOVELACE_DATA].resources.async_get_info())

    dashboards_info = await asyncio.gather(
        *(
            hass.data[LOVELACE_DATA].dashboards[dashboard].async_get_info()
            for dashboard in hass.data[LOVELACE_DATA].dashboards
        )
    )

    modes = set()
    for dashboard in dashboards_info:
        for key in dashboard:
            if isinstance(dashboard[key], int):
                health_info[key] = health_info.get(key, 0) + dashboard[key]
            elif key == CONF_MODE:
                modes.add(dashboard[key])
            else:
                health_info[key] = dashboard[key]

    if hass.data[LOVELACE_DATA].mode == MODE_YAML:
        health_info[CONF_MODE] = MODE_YAML
    elif MODE_STORAGE in modes:
        health_info[CONF_MODE] = MODE_STORAGE
    elif MODE_YAML in modes:
        health_info[CONF_MODE] = MODE_YAML
    else:
        health_info[CONF_MODE] = MODE_AUTO

    return health_info
