"""Tests for the Zodiac config flow."""

from unittest.mock import patch

import pytest

from smarthub.components.zodiac.const import DOMAIN
from smarthub.config_entries import SOURCE_USER
from smarthub.core import SmartHub
from smarthub.data_entry_flow import FlowResultType

from tests.common import MockConfigEntry


async def test_full_user_flow(hass: SmartHub) -> None:
    """Test the full user configuration flow."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )

    assert result.get("type") is FlowResultType.FORM
    assert result.get("step_id") == "user"

    with patch(
        "smarthub.components.zodiac.async_setup_entry",
        return_value=True,
    ) as mock_setup_entry:
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input={},
        )

    assert result.get("type") is FlowResultType.CREATE_ENTRY
    assert result.get("title") == "Zodiac"
    assert result.get("data") == {}
    assert result.get("options") == {}
    assert len(mock_setup_entry.mock_calls) == 1


@pytest.mark.parametrize("source", [SOURCE_USER])
async def test_single_instance_allowed(
    hass: SmartHub,
    source: str,
) -> None:
    """Test we abort if already setup."""
    mock_config_entry = MockConfigEntry(domain=DOMAIN)

    mock_config_entry.add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": source}
    )

    assert result.get("type") is FlowResultType.ABORT
    assert result.get("reason") == "single_instance_allowed"
