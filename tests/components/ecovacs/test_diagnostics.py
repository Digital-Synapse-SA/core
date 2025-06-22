"""Tests for diagnostics data."""

import pytest
from syrupy.assertion import SnapshotAssertion
from syrupy.filters import props

from smarthub.const import CONF_USERNAME
from smarthub.core import SmartHub

from .const import VALID_ENTRY_DATA_CLOUD, VALID_ENTRY_DATA_SELF_HOSTED

from tests.common import MockConfigEntry
from tests.components.diagnostics import get_diagnostics_for_config_entry
from tests.typing import ClientSessionGenerator


@pytest.mark.parametrize(
    "mock_config_entry_data",
    [VALID_ENTRY_DATA_CLOUD, VALID_ENTRY_DATA_SELF_HOSTED],
    ids=lambda data: data[CONF_USERNAME],
)
async def test_diagnostics(
    hass: SmartHub,
    hass_client: ClientSessionGenerator,
    init_integration: MockConfigEntry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test diagnostics."""
    assert await get_diagnostics_for_config_entry(
        hass, hass_client, init_integration
    ) == snapshot(exclude=props("entry_id", "created_at", "modified_at"))
