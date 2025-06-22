"""application_credentials platform the yale integration."""

from smarthub.components.application_credentials import AuthorizationServer
from smarthub.core import SmartHub

OAUTH2_AUTHORIZE = "https://oauth.aaecosystem.com/authorize"
OAUTH2_TOKEN = "https://oauth.aaecosystem.com/access_token"


async def async_get_authorization_server(hass: SmartHub) -> AuthorizationServer:
    """Return authorization server."""
    return AuthorizationServer(
        authorize_url=OAUTH2_AUTHORIZE,
        token_url=OAUTH2_TOKEN,
    )
