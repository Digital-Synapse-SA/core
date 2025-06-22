"""application_credentials platform for nest."""

import oauth2client

from smarthub.components.application_credentials import (
    AuthorizationServer,
    ClientCredential,
)
from smarthub.core import SmartHub
from smarthub.helpers import config_entry_oauth2_flow

from .api import GoogleHybridAuth

AUTHORIZATION_SERVER = AuthorizationServer(
    oauth2client.GOOGLE_AUTH_URI, oauth2client.GOOGLE_TOKEN_URI
)


async def async_get_auth_implementation(
    hass: SmartHub, auth_domain: str, credential: ClientCredential
) -> config_entry_oauth2_flow.AbstractOAuth2Implementation:
    """Return auth implementation."""
    return GoogleHybridAuth(hass, auth_domain, credential, AUTHORIZATION_SERVER)


async def async_get_description_placeholders(hass: SmartHub) -> dict[str, str]:
    """Return description placeholders for the credentials dialog."""
    return {
        "oauth_consent_url": (
            "https://console.cloud.google.com/apis/credentials/consent"
        ),
        "more_info_url": "https://www.smart-hub.io/integrations/google/",
        "oauth_creds_url": "https://console.cloud.google.com/apis/credentials",
    }
