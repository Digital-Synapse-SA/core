"""Intents for the cover integration."""

from smarthub.const import SERVICE_CLOSE_COVER, SERVICE_OPEN_COVER
from smarthub.core import SmartHub
from smarthub.helpers import intent

from . import DOMAIN, INTENT_CLOSE_COVER, INTENT_OPEN_COVER, CoverDeviceClass


async def async_setup_intents(hass: SmartHub) -> None:
    """Set up the cover intents."""
    intent.async_register(
        hass,
        intent.ServiceIntentHandler(
            INTENT_OPEN_COVER,
            DOMAIN,
            SERVICE_OPEN_COVER,
            "Opening {}",
            description="Opens a cover",
            platforms={DOMAIN},
            device_classes={CoverDeviceClass},
        ),
    )
    intent.async_register(
        hass,
        intent.ServiceIntentHandler(
            INTENT_CLOSE_COVER,
            DOMAIN,
            SERVICE_CLOSE_COVER,
            "Closing {}",
            description="Closes a cover",
            platforms={DOMAIN},
            device_classes={CoverDeviceClass},
        ),
    )
