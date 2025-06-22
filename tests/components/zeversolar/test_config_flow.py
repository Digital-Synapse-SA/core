"""Test the Zeversolar config flow."""

from unittest.mock import MagicMock, patch

import pytest
from zeversolar.exceptions import (
    ZeverSolarHTTPError,
    ZeverSolarHTTPNotFound,
    ZeverSolarTimeout,
)

from smarthub import config_entries
from smarthub.components.zeversolar.const import DOMAIN
from smarthub.const import CONF_HOST
from smarthub.core import SmartHub
from smarthub.data_entry_flow import FlowResultType

from tests.common import MockConfigEntry


async def test_form(hass: SmartHub) -> None:
    """Test we get the form."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["errors"] is None

    await _set_up_zeversolar(hass=hass, flow_id=result["flow_id"])


@pytest.mark.parametrize(
    ("side_effect", "errors"),
    [
        (
            ZeverSolarHTTPNotFound,
            {"base": "invalid_host"},
        ),
        (
            ZeverSolarHTTPError,
            {"base": "cannot_connect"},
        ),
        (
            ZeverSolarTimeout,
            {"base": "timeout_connect"},
        ),
        (
            RuntimeError,
            {"base": "unknown"},
        ),
    ],
)
async def test_form_errors(
    hass: SmartHub,
    side_effect: Exception,
    errors: dict,
) -> None:
    """Test we handle errors."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "zeversolar.ZeverSolarClient.get_data",
        side_effect=side_effect,
    ):
        result2 = await hass.config_entries.flow.async_configure(
            flow_id=result["flow_id"],
            user_input={
                CONF_HOST: "test_ip",
            },
        )

    assert result2["type"] is FlowResultType.FORM
    assert result2["errors"] == errors

    await _set_up_zeversolar(hass=hass, flow_id=result["flow_id"])


async def test_abort_already_configured(hass: SmartHub) -> None:
    """Test we abort when the device is already configured."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        title="Zeversolar",
        data={CONF_HOST: "test_ip"},
        unique_id="test_serial",
    )
    entry.add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result.get("type") is FlowResultType.FORM
    assert result.get("errors") is None
    assert "flow_id" in result

    mock_data = MagicMock()
    mock_data.serial_number = "test_serial"
    with (
        patch("zeversolar.ZeverSolarClient.get_data", return_value=mock_data),
        patch(
            "smarthub.components.zeversolar.async_setup_entry",
        ) as mock_setup_entry,
    ):
        result2 = await hass.config_entries.flow.async_configure(
            flow_id=result["flow_id"],
            user_input={
                CONF_HOST: "test_ip",
            },
        )
        await hass.async_block_till_done()

    assert result2.get("type") is FlowResultType.ABORT
    assert result2.get("reason") == "already_configured"
    assert len(mock_setup_entry.mock_calls) == 0


async def _set_up_zeversolar(hass: SmartHub, flow_id: str) -> None:
    """Reusable successful setup of Zeversolar sensor."""
    mock_data = MagicMock()
    mock_data.serial_number = "test_serial"
    with (
        patch("zeversolar.ZeverSolarClient.get_data", return_value=mock_data),
        patch(
            "smarthub.components.zeversolar.async_setup_entry",
            return_value=True,
        ) as mock_setup_entry,
    ):
        result2 = await hass.config_entries.flow.async_configure(
            flow_id=flow_id,
            user_input={
                CONF_HOST: "test_ip",
            },
        )
        await hass.async_block_till_done()

    assert result2["type"] is FlowResultType.CREATE_ENTRY
    assert result2["title"] == "Zeversolar"
    assert result2["data"] == {
        CONF_HOST: "test_ip",
    }
    assert len(mock_setup_entry.mock_calls) == 1
