"""application_credentials platform for YouTube."""

from smarthub.components.application_credentials import AuthorizationServer
from smarthub.core import SmartHub


async def async_get_authorization_server(hass: SmartHub) -> AuthorizationServer:
    """Return authorization server."""
    return AuthorizationServer(
        "https://accounts.google.com/o/oauth2/v2/auth",
        "https://oauth2.googleapis.com/token",
    )
