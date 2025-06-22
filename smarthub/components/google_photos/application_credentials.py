"""application_credentials platform the Google Photos integration."""

from smarthub.components.application_credentials import AuthorizationServer
from smarthub.core import SmartHub

from .const import OAUTH2_AUTHORIZE, OAUTH2_TOKEN


async def async_get_authorization_server(hass: SmartHub) -> AuthorizationServer:
    """Return authorization server."""
    return AuthorizationServer(
        authorize_url=OAUTH2_AUTHORIZE,
        token_url=OAUTH2_TOKEN,
    )


async def async_get_description_placeholders(hass: SmartHub) -> dict[str, str]:
    """Return description placeholders for the credentials dialog."""
    return {
        "oauth_consent_url": "https://console.cloud.google.com/apis/credentials/consent",
        "more_info_url": "https://www.smart-hub.io/integrations/google_photos/",
        "oauth_creds_url": "https://console.cloud.google.com/apis/credentials",
    }
