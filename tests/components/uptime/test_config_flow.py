"""Tests for the Uptime config flow."""

import pytest
from syrupy.assertion import SnapshotAssertion

from smarthub.components.uptime.const import DOMAIN
from smarthub.config_entries import SOURCE_USER
from smarthub.core import SmartHub
from smarthub.data_entry_flow import FlowResultType

from tests.common import MockConfigEntry


@pytest.mark.usefixtures("mock_setup_entry")
async def test_full_user_flow(
    hass: SmartHub,
    snapshot: SnapshotAssertion,
) -> None:
    """Test the full user configuration flow."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )

    assert result.get("type") is FlowResultType.FORM
    assert result.get("step_id") == "user"

    result2 = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        user_input={},
    )

    assert result2.get("type") is FlowResultType.CREATE_ENTRY
    assert result2 == snapshot


async def test_single_instance_allowed(
    hass: SmartHub,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test we abort if already setup."""
    mock_config_entry.add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )

    assert result.get("type") is FlowResultType.ABORT
    assert result.get("reason") == "single_instance_allowed"
