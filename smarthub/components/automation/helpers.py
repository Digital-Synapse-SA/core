"""Helpers for automation integration."""

from smarthub.components import blueprint
from smarthub.const import SERVICE_RELOAD
from smarthub.core import SmartHub, callback
from smarthub.helpers.singleton import singleton

from .const import DOMAIN, LOGGER

DATA_BLUEPRINTS = "automation_blueprints"


def _blueprint_in_use(hass: SmartHub, blueprint_path: str) -> bool:
    """Return True if any automation references the blueprint."""
    from . import automations_with_blueprint  # noqa: PLC0415

    return len(automations_with_blueprint(hass, blueprint_path)) > 0


async def _reload_blueprint_automations(
    hass: SmartHub, blueprint_path: str
) -> None:
    """Reload all automations that rely on a specific blueprint."""
    await hass.services.async_call(DOMAIN, SERVICE_RELOAD)


@singleton(DATA_BLUEPRINTS)
@callback
def async_get_blueprints(hass: SmartHub) -> blueprint.DomainBlueprints:
    """Get automation blueprints."""
    from .config import AUTOMATION_BLUEPRINT_SCHEMA  # noqa: PLC0415

    return blueprint.DomainBlueprints(
        hass,
        DOMAIN,
        LOGGER,
        _blueprint_in_use,
        _reload_blueprint_automations,
        AUTOMATION_BLUEPRINT_SCHEMA,
    )
