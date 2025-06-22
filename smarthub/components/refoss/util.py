"""Refoss helpers functions."""

from __future__ import annotations

from refoss_ha.discovery import Discovery

from smarthub.core import SmartHub
from smarthub.helpers import singleton


@singleton.singleton("refoss_discovery_server")
async def refoss_discovery_server(hass: SmartHub) -> Discovery:
    """Get refoss Discovery server."""
    discovery_server = Discovery()
    await discovery_server.initialize()
    return discovery_server
