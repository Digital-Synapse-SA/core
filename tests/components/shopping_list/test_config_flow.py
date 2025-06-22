"""Test config flow."""

from smarthub.components.shopping_list.const import DOMAIN
from smarthub.config_entries import SOURCE_IMPORT, SOURCE_USER
from smarthub.core import SmartHub
from smarthub.data_entry_flow import FlowResultType


async def test_import(hass: SmartHub) -> None:
    """Test entry will be imported."""

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_IMPORT}, data={}
    )
    assert result["type"] is FlowResultType.CREATE_ENTRY


async def test_user(hass: SmartHub) -> None:
    """Test we can start a config flow."""

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"


async def test_user_confirm(hass: SmartHub) -> None:
    """Test we can finish a config flow."""

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}, data={}
    )

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["result"].data == {}


async def test_onboarding_flow(hass: SmartHub) -> None:
    """Test the onboarding configuration flow."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": "onboarding"}
    )

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "Shopping list"
    assert result["data"] == {}
