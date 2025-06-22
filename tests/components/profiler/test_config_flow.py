"""Test the Profiler config flow."""

from unittest.mock import patch

from smarthub import config_entries
from smarthub.components.profiler.const import DOMAIN
from smarthub.core import SmartHub
from smarthub.data_entry_flow import FlowResultType

from tests.common import MockConfigEntry


async def test_form_user(hass: SmartHub) -> None:
    """Test we can setup by the user."""

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["errors"] is None

    with patch(
        "smarthub.components.profiler.async_setup_entry",
        return_value=True,
    ) as mock_setup_entry:
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {},
        )
        await hass.async_block_till_done()

    assert result2["type"] is FlowResultType.CREATE_ENTRY
    assert result2["title"] == "Profiler"
    assert result2["data"] == {}
    assert len(mock_setup_entry.mock_calls) == 1


async def test_form_user_only_once(hass: SmartHub) -> None:
    """Test we can setup by the user only once."""
    MockConfigEntry(domain=DOMAIN).add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "single_instance_allowed"
