"""Application credentials platform for senz."""

from aiosenz import AUTHORIZATION_ENDPOINT, TOKEN_ENDPOINT

from smarthub.components.application_credentials import AuthorizationServer
from smarthub.core import SmartHub


async def async_get_authorization_server(hass: SmartHub) -> AuthorizationServer:
    """Return authorization server."""
    return AuthorizationServer(
        authorize_url=AUTHORIZATION_ENDPOINT,
        token_url=TOKEN_ENDPOINT,
    )
