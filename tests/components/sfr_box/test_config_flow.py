"""Test the SFR Box config flow."""

import json
from unittest.mock import AsyncMock, patch

import pytest
from sfrbox_api.exceptions import SFRBoxAuthenticationError, SFRBoxError
from sfrbox_api.models import SystemInfo

from smarthub import config_entries
from smarthub.components.sfr_box.const import DOMAIN
from smarthub.config_entries import ConfigEntry
from smarthub.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME
from smarthub.core import SmartHub
from smarthub.data_entry_flow import FlowResultType

from tests.common import async_load_fixture

pytestmark = pytest.mark.usefixtures("mock_setup_entry")


async def test_config_flow_skip_auth(
    hass: SmartHub, mock_setup_entry: AsyncMock
) -> None:
    """Test we get the form."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {}

    with patch(
        "smarthub.components.sfr_box.config_flow.SFRBox.system_get_info",
        side_effect=SFRBoxError,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input={
                CONF_HOST: "192.168.0.1",
            },
        )

    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {"base": "cannot_connect"}

    with patch(
        "smarthub.components.sfr_box.config_flow.SFRBox.system_get_info",
        return_value=SystemInfo(
            **json.loads(await async_load_fixture(hass, "system_getInfo.json", DOMAIN))
        ),
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input={
                CONF_HOST: "192.168.0.1",
            },
        )

    assert result["type"] is FlowResultType.MENU
    assert result["step_id"] == "choose_auth"

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {"next_step_id": "skip_auth"},
    )

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "SFR Box"
    assert result["data"] == {CONF_HOST: "192.168.0.1"}

    assert len(mock_setup_entry.mock_calls) == 1


async def test_config_flow_with_auth(
    hass: SmartHub, mock_setup_entry: AsyncMock
) -> None:
    """Test we get the form."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {}

    with patch(
        "smarthub.components.sfr_box.config_flow.SFRBox.system_get_info",
        return_value=SystemInfo(
            **json.loads(await async_load_fixture(hass, "system_getInfo.json", DOMAIN))
        ),
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input={
                CONF_HOST: "192.168.0.1",
            },
        )

    assert result["type"] is FlowResultType.MENU
    assert result["step_id"] == "choose_auth"

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {"next_step_id": "auth"},
    )

    with patch(
        "smarthub.components.sfr_box.config_flow.SFRBox.authenticate",
        side_effect=SFRBoxAuthenticationError,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input={
                CONF_USERNAME: "admin",
                CONF_PASSWORD: "invalid",
            },
        )

    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {"base": "invalid_auth"}

    with patch("smarthub.components.sfr_box.config_flow.SFRBox.authenticate"):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input={
                CONF_USERNAME: "admin",
                CONF_PASSWORD: "valid",
            },
        )

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "SFR Box"
    assert result["data"] == {
        CONF_HOST: "192.168.0.1",
        CONF_USERNAME: "admin",
        CONF_PASSWORD: "valid",
    }

    assert len(mock_setup_entry.mock_calls) == 1


@pytest.mark.usefixtures("config_entry")
async def test_config_flow_duplicate_host(
    hass: SmartHub, mock_setup_entry: AsyncMock
) -> None:
    """Test abort if unique_id configured."""
    assert len(hass.config_entries.async_entries(DOMAIN)) == 1

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {}

    system_info = SystemInfo(
        **json.loads(await async_load_fixture(hass, "system_getInfo.json", DOMAIN))
    )
    # Ensure mac doesn't match existing mock entry
    system_info.mac_addr = "aa:bb:cc:dd:ee:ff"
    with patch(
        "smarthub.components.sfr_box.config_flow.SFRBox.system_get_info",
        return_value=system_info,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input={
                CONF_HOST: "192.168.0.1",
            },
        )

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "already_configured"
    await hass.async_block_till_done()

    assert len(mock_setup_entry.mock_calls) == 0


@pytest.mark.usefixtures("config_entry")
async def test_config_flow_duplicate_mac(
    hass: SmartHub, mock_setup_entry: AsyncMock
) -> None:
    """Test abort if unique_id configured."""
    assert len(hass.config_entries.async_entries(DOMAIN)) == 1

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {}

    system_info = SystemInfo(
        **json.loads(await async_load_fixture(hass, "system_getInfo.json", DOMAIN))
    )
    with patch(
        "smarthub.components.sfr_box.config_flow.SFRBox.system_get_info",
        return_value=system_info,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input={
                CONF_HOST: "192.168.0.2",
            },
        )

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "already_configured"
    await hass.async_block_till_done()

    assert len(mock_setup_entry.mock_calls) == 0


async def test_reauth(hass: SmartHub, config_entry_with_auth: ConfigEntry) -> None:
    """Test the start of the config flow."""
    assert len(hass.config_entries.async_entries(DOMAIN)) == 1

    result = await config_entry_with_auth.start_reauth_flow(hass)

    assert result.get("type") is FlowResultType.FORM
    assert result.get("errors") == {}

    # Failed credentials
    with patch(
        "smarthub.components.sfr_box.config_flow.SFRBox.authenticate",
        side_effect=SFRBoxAuthenticationError,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input={
                CONF_USERNAME: "admin",
                CONF_PASSWORD: "invalid",
            },
        )

    assert result.get("type") is FlowResultType.FORM
    assert result.get("errors") == {"base": "invalid_auth"}

    # Valid credentials
    with patch("smarthub.components.sfr_box.config_flow.SFRBox.authenticate"):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input={
                CONF_USERNAME: "admin",
                CONF_PASSWORD: "new_password",
            },
        )

    assert result.get("type") is FlowResultType.ABORT
    assert result.get("reason") == "reauth_successful"
