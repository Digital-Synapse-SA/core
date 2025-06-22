"""The MyQ integration."""

from __future__ import annotations

from smarthub.config_entries import ConfigEntry
from smarthub.core import SmartHub
from smarthub.helpers import issue_registry as ir

DOMAIN = "myq"


async def async_setup_entry(hass: SmartHub, _: ConfigEntry) -> bool:
    """Set up MyQ from a config entry."""
    ir.async_create_issue(
        hass,
        DOMAIN,
        DOMAIN,
        is_fixable=False,
        severity=ir.IssueSeverity.ERROR,
        translation_key="integration_removed",
        translation_placeholders={
            "blog": "https://www.smart-hub.io/blog/2023/11/06/removal-of-myq-integration/",
            "entries": "/config/integrations/integration/myQ",
        },
    )

    return True


async def async_unload_entry(hass: SmartHub, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return True


async def async_remove_entry(hass: SmartHub, entry: ConfigEntry) -> None:
    """Remove a config entry."""
    if not hass.config_entries.async_loaded_entries(DOMAIN):
        ir.async_delete_issue(hass, DOMAIN, DOMAIN)
        # Remove any remaining disabled or ignored entries
        for _entry in hass.config_entries.async_entries(DOMAIN):
            hass.async_create_task(hass.config_entries.async_remove(_entry.entry_id))
