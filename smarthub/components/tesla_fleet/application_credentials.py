"""Application Credentials platform the Tesla Fleet integration."""

from smarthub.components.application_credentials import ClientCredential
from smarthub.core import SmartHub
from smarthub.helpers import config_entry_oauth2_flow

from .oauth import TeslaUserImplementation


async def async_get_auth_implementation(
    hass: SmartHub, auth_domain: str, credential: ClientCredential
) -> config_entry_oauth2_flow.AbstractOAuth2Implementation:
    """Return auth implementation."""
    return TeslaUserImplementation(
        hass,
        auth_domain,
        credential,
    )
