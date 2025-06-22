"""Utils for Vodafone Station."""

from aiohttp import ClientSession, CookieJar

from smarthub.core import SmartHub
from smarthub.helpers import aiohttp_client


async def async_client_session(hass: SmartHub) -> ClientSession:
    """Return a new aiohttp session."""
    return aiohttp_client.async_create_clientsession(
        hass, verify_ssl=False, cookie_jar=CookieJar(unsafe=True, quote_cookie=False)
    )
