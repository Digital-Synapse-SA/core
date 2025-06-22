"""Test AfterShip config flow."""

from unittest.mock import AsyncMock, patch

from pyaftership import AfterShipException

from smarthub.components.aftership.const import DOMAIN
from smarthub.config_entries import SOURCE_USER
from smarthub.const import CONF_API_KEY
from smarthub.core import SmartHub
from smarthub.data_entry_flow import FlowResultType


async def test_full_user_flow(hass: SmartHub, mock_setup_entry) -> None:
    """Test the full user configuration flow."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": SOURCE_USER},
    )

    with patch(
        "smarthub.components.aftership.config_flow.AfterShip",
        return_value=AsyncMock(),
    ) as mock_aftership:
        mock_aftership.return_value.trackings.return_value.list.return_value = {}
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input={
                CONF_API_KEY: "mock-api-key",
            },
        )
        assert result["type"] is FlowResultType.CREATE_ENTRY
        assert result["title"] == "AfterShip"
        assert result["data"] == {
            CONF_API_KEY: "mock-api-key",
        }


async def test_flow_cannot_connect(hass: SmartHub, mock_setup_entry) -> None:
    """Test handling invalid connection."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": SOURCE_USER},
    )

    with patch(
        "smarthub.components.aftership.config_flow.AfterShip",
        return_value=AsyncMock(),
    ) as mock_aftership:
        mock_aftership.side_effect = AfterShipException
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input={
                CONF_API_KEY: "mock-api-key",
            },
        )
        assert result["type"] is FlowResultType.FORM
        assert result["step_id"] == "user"

    with patch(
        "smarthub.components.aftership.config_flow.AfterShip",
        return_value=AsyncMock(),
    ) as mock_aftership:
        mock_aftership.return_value.trackings.return_value.list.return_value = {}
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input={
                CONF_API_KEY: "mock-api-key",
            },
        )
        assert result["type"] is FlowResultType.CREATE_ENTRY
        assert result["title"] == "AfterShip"
        assert result["data"] == {
            CONF_API_KEY: "mock-api-key",
        }
