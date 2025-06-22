"""Provide add-on management."""

from __future__ import annotations

from smarthub.components.hassio import AddonManager
from smarthub.core import SmartHub, callback
from smarthub.helpers.singleton import singleton

from .const import ADDON_SLUG, DOMAIN, LOGGER

DATA_ADDON_MANAGER = f"{DOMAIN}_addon_manager"


@singleton(DATA_ADDON_MANAGER)
@callback
def get_addon_manager(hass: SmartHub) -> AddonManager:
    """Get the add-on manager."""
    return AddonManager(hass, LOGGER, "Z-Wave JS", ADDON_SLUG)
