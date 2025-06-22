"""Application credentials platform for the Honeywell Lyric integration."""

from smarthub.components.application_credentials import (
    AuthorizationServer,
    ClientCredential,
)
from smarthub.core import SmartHub
from smarthub.helpers import config_entry_oauth2_flow

from .api import LyricLocalOAuth2Implementation
from .const import OAUTH2_AUTHORIZE, OAUTH2_TOKEN


async def async_get_auth_implementation(
    hass: SmartHub, auth_domain: str, credential: ClientCredential
) -> config_entry_oauth2_flow.AbstractOAuth2Implementation:
    """Return custom auth implementation."""
    return LyricLocalOAuth2Implementation(
        hass,
        auth_domain,
        credential,
        AuthorizationServer(
            authorize_url=OAUTH2_AUTHORIZE,
            token_url=OAUTH2_TOKEN,
        ),
    )


async def async_get_description_placeholders(hass: SmartHub) -> dict[str, str]:
    """Return description placeholders for the credentials dialog."""
    return {
        "developer_dashboard_url": "https://developer.honeywellhome.com",
        "redirect_url": "https://my.smart-hub.io/redirect/oauth",
    }
