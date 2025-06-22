"""Component to embed Google Cast."""

from __future__ import annotations

from typing import Protocol

from pychromecast import Chromecast

from smarthub.components.media_player import BrowseMedia, MediaType
from smarthub.config_entries import ConfigEntry
from smarthub.const import Platform
from smarthub.core import SmartHub, callback
from smarthub.exceptions import SmartHubError
from smarthub.helpers import device_registry as dr
from smarthub.helpers.integration_platform import (
    async_process_integration_platforms,
)

from . import home_assistant_cast
from .const import DOMAIN

PLATFORMS = [Platform.MEDIA_PLAYER]


async def async_setup_entry(hass: SmartHub, entry: ConfigEntry) -> bool:
    """Set up Cast from a config entry."""
    hass.data[DOMAIN] = {"cast_platform": {}, "unknown_models": {}}
    await home_assistant_cast.async_setup_ha_cast(hass, entry)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    await async_process_integration_platforms(hass, DOMAIN, _register_cast_platform)
    return True


class CastProtocol(Protocol):
    """Define the format of cast platforms."""

    async def async_get_media_browser_root_object(
        self, hass: SmartHub, cast_type: str
    ) -> list[BrowseMedia]:
        """Create a list of root objects for media browsing."""

    async def async_browse_media(
        self,
        hass: SmartHub,
        media_content_type: MediaType | str,
        media_content_id: str,
        cast_type: str,
    ) -> BrowseMedia | None:
        """Browse media.

        Return a BrowseMedia object or None if the media does not belong to
        this platform.
        """

    async def async_play_media(
        self,
        hass: SmartHub,
        cast_entity_id: str,
        chromecast: Chromecast,
        media_type: MediaType | str,
        media_id: str,
    ) -> bool:
        """Play media.

        Return True if the media is played by the platform, False if not.
        """


@callback
def _register_cast_platform(
    hass: SmartHub, integration_domain: str, platform: CastProtocol
):
    """Register a cast platform."""
    if (
        not hasattr(platform, "async_get_media_browser_root_object")
        or not hasattr(platform, "async_browse_media")
        or not hasattr(platform, "async_play_media")
    ):
        raise SmartHubError(f"Invalid cast platform {platform}")
    hass.data[DOMAIN]["cast_platform"][integration_domain] = platform


async def async_remove_entry(hass: SmartHub, entry: ConfigEntry) -> None:
    """Remove SmartHub Cast user."""
    await home_assistant_cast.async_remove_user(hass, entry)


async def async_remove_config_entry_device(
    hass: SmartHub, config_entry: ConfigEntry, device_entry: dr.DeviceEntry
) -> bool:
    """Remove cast config entry from a device.

    The actual cleanup is done in CastMediaPlayerEntity.async_will_remove_from_hass.
    """
    return True
