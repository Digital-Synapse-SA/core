"""Blebox helpers."""

from __future__ import annotations

import aiohttp

from smarthub.core import SmartHub
from smarthub.helpers.aiohttp_client import (
    async_create_clientsession,
    async_get_clientsession,
)


def get_maybe_authenticated_session(
    hass: SmartHub, password: str | None, username: str | None
) -> aiohttp.ClientSession:
    """Return proper session object."""
    if username and password:
        auth = aiohttp.BasicAuth(login=username, password=password)
        return async_create_clientsession(hass, auth=auth)

    return async_get_clientsession(hass)
