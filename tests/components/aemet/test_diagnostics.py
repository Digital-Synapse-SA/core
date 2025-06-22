"""Define tests for the AEMET OpenData diagnostics."""

from unittest.mock import patch

import pytest
from syrupy.assertion import SnapshotAssertion
from syrupy.filters import props

from smarthub.components.aemet.const import DOMAIN
from smarthub.core import SmartHub

from .util import async_init_integration

from tests.components.diagnostics import get_diagnostics_for_config_entry
from tests.typing import ClientSessionGenerator


@pytest.mark.freeze_time("2024-02-23T18:00:00+00:00")
async def test_config_entry_diagnostics(
    hass: SmartHub,
    hass_client: ClientSessionGenerator,
    snapshot: SnapshotAssertion,
) -> None:
    """Test config entry diagnostics."""
    await async_init_integration(hass)

    config_entry = hass.config_entries.async_entries(DOMAIN)[0]

    with patch(
        "smarthub.components.aemet.AEMET.raw_data",
        return_value={},
    ):
        result = await get_diagnostics_for_config_entry(hass, hass_client, config_entry)
        assert result == snapshot(exclude=props("created_at", "modified_at"))
