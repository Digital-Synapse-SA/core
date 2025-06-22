"""Test the SmartHub Supervisor config flow."""

from unittest.mock import patch

from smarthub.components.hassio import DOMAIN
from smarthub.core import SmartHub
from smarthub.data_entry_flow import FlowResultType


async def test_config_flow(hass: SmartHub) -> None:
    """Test we get the form."""

    with (
        patch(
            "smarthub.components.hassio.async_setup", return_value=True
        ) as mock_setup,
        patch(
            "smarthub.components.hassio.async_setup_entry",
            return_value=True,
        ) as mock_setup_entry,
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": "system"}
        )
        assert result["type"] is FlowResultType.CREATE_ENTRY
        assert result["title"] == "Supervisor"
        assert result["data"] == {}
        await hass.async_block_till_done()

    assert len(mock_setup.mock_calls) == 1
    assert len(mock_setup_entry.mock_calls) == 1


async def test_multiple_entries(hass: SmartHub) -> None:
    """Test creating multiple hassio entries."""
    await test_config_flow(hass)
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": "system"}
    )
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "single_instance_allowed"
