"""Tests for the Enphase Envoy integration."""

from smarthub.config_entries import ConfigEntryState
from smarthub.core import SmartHub

from tests.common import MockConfigEntry


async def setup_integration(
    hass: SmartHub,
    config_entry: MockConfigEntry,
    expected_state: ConfigEntryState = ConfigEntryState.LOADED,
) -> None:
    """Fixture for setting up the component and testing expected state."""
    config_entry.add_to_hass(hass)

    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done(wait_background_tasks=True)
    assert config_entry.state is expected_state
