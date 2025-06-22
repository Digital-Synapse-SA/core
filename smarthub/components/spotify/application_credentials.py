"""Application credentials platform for spotify."""

from smarthub.components.application_credentials import AuthorizationServer
from smarthub.core import SmartHub


async def async_get_authorization_server(hass: SmartHub) -> AuthorizationServer:
    """Return authorization server."""
    return AuthorizationServer(
        authorize_url="https://accounts.spotify.com/authorize",
        token_url="https://accounts.spotify.com/api/token",
    )
