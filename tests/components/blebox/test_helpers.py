"""Blebox helpers tests."""

from aiohttp.helpers import BasicAuth

from smarthub.components.blebox.helpers import get_maybe_authenticated_session
from smarthub.core import SmartHub


async def test_get_maybe_authenticated_session_none(hass: SmartHub) -> None:
    """Tests if session auth is None."""
    session = get_maybe_authenticated_session(hass=hass, username="", password="")
    assert session.auth is None


async def test_get_maybe_authenticated_session_auth(hass: SmartHub) -> None:
    """Tests if session have BasicAuth."""
    session = get_maybe_authenticated_session(
        hass=hass, username="user", password="password"
    )
    assert isinstance(session.auth, BasicAuth)
