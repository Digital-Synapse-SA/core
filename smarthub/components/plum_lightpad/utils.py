"""Reusable utilities for the Plum Lightpad component."""

from plumlightpad import Plum

from smarthub.core import SmartHub
from smarthub.helpers.aiohttp_client import async_get_clientsession


async def load_plum(username: str, password: str, hass: SmartHub) -> Plum:
    """Initialize Plum Lightpad API and load metadata stored in the cloud."""
    plum = Plum(username, password)
    cloud_web_session = async_get_clientsession(hass, verify_ssl=True)
    await plum.loadCloudData(cloud_web_session)
    return plum
