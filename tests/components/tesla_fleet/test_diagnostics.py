"""Test the Tesla Fleet Diagnostics."""

from syrupy.assertion import SnapshotAssertion

from smarthub.core import SmartHub

from . import setup_platform

from tests.common import MockConfigEntry
from tests.components.diagnostics import get_diagnostics_for_config_entry
from tests.typing import ClientSessionGenerator


async def test_diagnostics(
    hass: SmartHub,
    hass_client: ClientSessionGenerator,
    snapshot: SnapshotAssertion,
    normal_config_entry: MockConfigEntry,
) -> None:
    """Test diagnostics."""

    await setup_platform(hass, normal_config_entry)

    diag = await get_diagnostics_for_config_entry(
        hass, hass_client, normal_config_entry
    )
    assert diag == snapshot
