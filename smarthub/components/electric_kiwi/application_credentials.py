"""application_credentials platform the Electric Kiwi integration."""

from smarthub.components.application_credentials import (
    AuthorizationServer,
    ClientCredential,
)
from smarthub.core import SmartHub
from smarthub.helpers import config_entry_oauth2_flow

from .const import OAUTH2_AUTHORIZE, OAUTH2_TOKEN
from .oauth2 import ElectricKiwiLocalOAuth2Implementation


async def async_get_auth_implementation(
    hass: SmartHub, auth_domain: str, credential: ClientCredential
) -> config_entry_oauth2_flow.AbstractOAuth2Implementation:
    """Return auth implementation."""
    return ElectricKiwiLocalOAuth2Implementation(
        hass,
        auth_domain,
        credential,
        authorization_server=await async_get_authorization_server(hass),
    )


async def async_get_authorization_server(hass: SmartHub) -> AuthorizationServer:
    """Return authorization server."""
    return AuthorizationServer(
        authorize_url=OAUTH2_AUTHORIZE,
        token_url=OAUTH2_TOKEN,
    )


async def async_get_description_placeholders(hass: SmartHub) -> dict[str, str]:
    """Return description placeholders for the credentials dialog."""
    return {
        "more_info_url": "https://www.smart-hub.io/integrations/electric_kiwi/"
    }
