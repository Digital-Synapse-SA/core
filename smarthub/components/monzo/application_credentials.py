"""application_credentials platform the Monzo integration."""

from smarthub.components.application_credentials import AuthorizationServer
from smarthub.core import SmartHub

OAUTH2_AUTHORIZE = "https://auth.monzo.com"
OAUTH2_TOKEN = "https://api.monzo.com/oauth2/token"


async def async_get_authorization_server(hass: SmartHub) -> AuthorizationServer:
    """Return authorization server."""
    return AuthorizationServer(
        authorize_url=OAUTH2_AUTHORIZE,
        token_url=OAUTH2_TOKEN,
    )
