"""Application credentials platform for LaMetric."""

from smarthub.components.application_credentials import AuthorizationServer
from smarthub.core import SmartHub


async def async_get_authorization_server(hass: SmartHub) -> AuthorizationServer:
    """Return authorization server."""
    return AuthorizationServer(
        authorize_url="https://developer.lametric.com/api/v2/oauth2/authorize",
        token_url="https://developer.lametric.com/api/v2/oauth2/token",
    )
