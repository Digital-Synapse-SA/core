"""Tests for the Omnilogic integration."""

from unittest.mock import patch

from smarthub.components.omnilogic.const import DOMAIN
from smarthub.const import CONF_PASSWORD, CONF_USERNAME
from smarthub.core import SmartHub

from .const import TELEMETRY

from tests.common import MockConfigEntry


async def init_integration(hass: SmartHub) -> MockConfigEntry:
    """Mock integration setup."""
    with (
        patch(
            "smarthub.components.omnilogic.OmniLogic.connect",
            return_value=True,
        ),
        patch(
            "smarthub.components.omnilogic.OmniLogic.get_telemetry_data",
            return_value={},
        ),
        patch(
            "smarthub.components.omnilogic.coordinator.OmniLogicUpdateCoordinator._async_update_data",
            return_value=TELEMETRY,
        ),
    ):
        entry = MockConfigEntry(
            domain=DOMAIN,
            data={CONF_USERNAME: "test-username", CONF_PASSWORD: "test-password"},
            entry_id="6fa019921cf8e7a3f57a3c2ed001a10d",
        )
        entry.add_to_hass(hass)
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()
        return entry
