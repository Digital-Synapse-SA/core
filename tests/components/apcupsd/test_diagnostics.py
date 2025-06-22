"""Test APCUPSd diagnostics reporting abilities."""

from syrupy.assertion import SnapshotAssertion

from smarthub.core import SmartHub

from . import async_init_integration

from tests.components.diagnostics import get_diagnostics_for_config_entry
from tests.typing import ClientSessionGenerator


async def test_diagnostics(
    hass: SmartHub,
    hass_client: ClientSessionGenerator,
    snapshot: SnapshotAssertion,
) -> None:
    """Test diagnostics."""
    entry = await async_init_integration(hass)
    assert await get_diagnostics_for_config_entry(hass, hass_client, entry) == snapshot
