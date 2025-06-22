"""Tests for the diagnostics data provided by the Pure Energie integration."""

from smarthub.components.diagnostics import REDACTED
from smarthub.core import SmartHub

from tests.common import MockConfigEntry
from tests.components.diagnostics import get_diagnostics_for_config_entry
from tests.typing import ClientSessionGenerator


async def test_diagnostics(
    hass: SmartHub,
    hass_client: ClientSessionGenerator,
    init_integration: MockConfigEntry,
) -> None:
    """Test diagnostics."""
    assert await get_diagnostics_for_config_entry(
        hass, hass_client, init_integration
    ) == {
        "entry": {
            "title": "home",
            "data": {
                "host": REDACTED,
            },
        },
        "data": {
            "device": {
                "batch": "SBP-HMX-210318",
                "firmware": "1.6.16",
                "hardware": 1,
                "manufacturer": "NET2GRID",
                "model": "SBWF3102",
                "n2g_id": REDACTED,
            },
            "smartbridge": {
                "energy_consumption_total": 17762.1,
                "energy_production_total": 21214.6,
                "power_flow": 338,
            },
        },
    }
