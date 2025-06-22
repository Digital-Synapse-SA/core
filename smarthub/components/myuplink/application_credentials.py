"""application_credentials platform the myUplink integration."""

from smarthub.components.application_credentials import AuthorizationServer
from smarthub.core import SmartHub

from .const import DOMAIN, OAUTH2_AUTHORIZE, OAUTH2_TOKEN


async def async_get_authorization_server(hass: SmartHub) -> AuthorizationServer:
    """Return authorization server."""
    return AuthorizationServer(
        authorize_url=OAUTH2_AUTHORIZE,
        token_url=OAUTH2_TOKEN,
    )


async def async_get_description_placeholders(hass: SmartHub) -> dict[str, str]:
    """Return description placeholders for the credentials dialog."""
    return {
        "more_info_url": f"https://www.smart-hub.io/integrations/{DOMAIN}/",
        "create_creds_url": "https://dev.myuplink.com/apps",
        "callback_url": "https://my.smart-hub.io/redirect/oauth",
    }
