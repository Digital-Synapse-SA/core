"""Test the WiZ Platform config flow."""

from unittest.mock import AsyncMock, patch

import pytest
from pywizlight.exceptions import WizLightConnectionError, WizLightTimeOutError

from smarthub import config_entries
from smarthub.components.wiz.config_flow import CONF_DEVICE
from smarthub.components.wiz.const import DOMAIN
from smarthub.config_entries import ConfigEntryState
from smarthub.const import CONF_HOST
from smarthub.core import SmartHub
from smarthub.data_entry_flow import FlowResultType
from smarthub.helpers.service_info.dhcp import DhcpServiceInfo

from . import (
    FAKE_DIMMABLE_BULB,
    FAKE_EXTENDED_WHITE_RANGE,
    FAKE_IP,
    FAKE_MAC,
    FAKE_RGBW_BULB,
    FAKE_RGBWW_BULB,
    FAKE_SOCKET,
    TEST_CONNECTION,
    TEST_SYSTEM_INFO,
    _mocked_wizlight,
    _patch_discovery,
    _patch_wizlight,
    async_setup_integration,
)

from tests.common import MockConfigEntry

DHCP_DISCOVERY = DhcpServiceInfo(
    hostname="wiz_abcabc",
    ip=FAKE_IP,
    macaddress=FAKE_MAC,
)


INTEGRATION_DISCOVERY = {
    "ip_address": FAKE_IP,
    "mac_address": FAKE_MAC,
}


async def test_form(hass: SmartHub) -> None:
    """Test we get the form."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {}
    # Patch functions
    with (
        _patch_wizlight(),
        patch(
            "smarthub.components.wiz.async_setup_entry",
            return_value=True,
        ) as mock_setup_entry,
        patch(
            "smarthub.components.wiz.async_setup", return_value=True
        ) as mock_setup,
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            TEST_CONNECTION,
        )
        await hass.async_block_till_done()

    assert result2["type"] is FlowResultType.CREATE_ENTRY
    assert result2["title"] == "WiZ Dimmable White ABCABC"
    assert result2["data"] == {
        CONF_HOST: "1.1.1.1",
    }
    assert len(mock_setup.mock_calls) == 1
    assert len(mock_setup_entry.mock_calls) == 1


async def test_user_flow_enters_dns_name(hass: SmartHub) -> None:
    """Test we reject dns names and want ips."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {}

    result2 = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {CONF_HOST: "ip.only"},
    )
    await hass.async_block_till_done()

    assert result2["type"] is FlowResultType.FORM
    assert result2["errors"] == {"base": "no_ip"}

    with (
        _patch_wizlight(),
        patch(
            "smarthub.components.wiz.async_setup_entry",
            return_value=True,
        ) as mock_setup_entry,
        patch(
            "smarthub.components.wiz.async_setup", return_value=True
        ) as mock_setup,
    ):
        result3 = await hass.config_entries.flow.async_configure(
            result2["flow_id"],
            TEST_CONNECTION,
        )
        await hass.async_block_till_done()

    assert result3["type"] is FlowResultType.CREATE_ENTRY
    assert result3["title"] == "WiZ Dimmable White ABCABC"
    assert result3["data"] == {
        CONF_HOST: "1.1.1.1",
    }
    assert len(mock_setup.mock_calls) == 1
    assert len(mock_setup_entry.mock_calls) == 1


@pytest.mark.parametrize(
    ("side_effect", "error_base"),
    [
        (WizLightTimeOutError, "bulb_time_out"),
        (WizLightConnectionError, "no_wiz_light"),
        (Exception, "unknown"),
        (ConnectionRefusedError, "cannot_connect"),
    ],
)
async def test_user_form_exceptions(
    hass: SmartHub, side_effect, error_base
) -> None:
    """Test all user exceptions in the flow."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "smarthub.components.wiz.wizlight.getBulbConfig",
        side_effect=side_effect,
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            TEST_CONNECTION,
        )

    assert result2["type"] is FlowResultType.FORM
    assert result2["errors"] == {"base": error_base}


async def test_form_updates_unique_id(hass: SmartHub) -> None:
    """Test a duplicate id aborts and updates existing entry."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id=TEST_SYSTEM_INFO["id"],
        data={CONF_HOST: "dummy"},
    )
    entry.add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    with _patch_wizlight():
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            TEST_CONNECTION,
        )
        await hass.async_block_till_done()

    assert result2["type"] is FlowResultType.ABORT
    assert result2["reason"] == "already_configured"
    assert entry.data[CONF_HOST] == FAKE_IP


@pytest.mark.parametrize(
    ("source", "data"),
    [
        (config_entries.SOURCE_DHCP, DHCP_DISCOVERY),
        (config_entries.SOURCE_INTEGRATION_DISCOVERY, INTEGRATION_DISCOVERY),
    ],
)
async def test_discovered_by_dhcp_connection_fails(
    hass: SmartHub, source, data
) -> None:
    """Test we abort on connection failure."""
    with patch(
        "smarthub.components.wiz.wizlight.getBulbConfig",
        side_effect=WizLightTimeOutError,
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": source}, data=data
        )
        await hass.async_block_till_done()

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "cannot_connect"


@pytest.mark.parametrize(
    ("source", "data", "bulb_type", "extended_white_range", "name"),
    [
        (
            config_entries.SOURCE_DHCP,
            DHCP_DISCOVERY,
            FAKE_DIMMABLE_BULB,
            FAKE_EXTENDED_WHITE_RANGE,
            "WiZ Dimmable White ABCABC",
        ),
        (
            config_entries.SOURCE_INTEGRATION_DISCOVERY,
            INTEGRATION_DISCOVERY,
            FAKE_DIMMABLE_BULB,
            FAKE_EXTENDED_WHITE_RANGE,
            "WiZ Dimmable White ABCABC",
        ),
        (
            config_entries.SOURCE_DHCP,
            DHCP_DISCOVERY,
            FAKE_RGBW_BULB,
            FAKE_EXTENDED_WHITE_RANGE,
            "WiZ RGBW Tunable ABCABC",
        ),
        (
            config_entries.SOURCE_INTEGRATION_DISCOVERY,
            INTEGRATION_DISCOVERY,
            FAKE_RGBW_BULB,
            FAKE_EXTENDED_WHITE_RANGE,
            "WiZ RGBW Tunable ABCABC",
        ),
        (
            config_entries.SOURCE_DHCP,
            DHCP_DISCOVERY,
            FAKE_RGBWW_BULB,
            FAKE_EXTENDED_WHITE_RANGE,
            "WiZ RGBWW Tunable ABCABC",
        ),
        (
            config_entries.SOURCE_INTEGRATION_DISCOVERY,
            INTEGRATION_DISCOVERY,
            FAKE_RGBWW_BULB,
            FAKE_EXTENDED_WHITE_RANGE,
            "WiZ RGBWW Tunable ABCABC",
        ),
        (
            config_entries.SOURCE_DHCP,
            DHCP_DISCOVERY,
            FAKE_SOCKET,
            None,
            "WiZ Socket ABCABC",
        ),
        (
            config_entries.SOURCE_INTEGRATION_DISCOVERY,
            INTEGRATION_DISCOVERY,
            FAKE_SOCKET,
            None,
            "WiZ Socket ABCABC",
        ),
    ],
)
async def test_discovered_by_dhcp_or_integration_discovery(
    hass: SmartHub, source, data, bulb_type, extended_white_range, name
) -> None:
    """Test we can configure when discovered from dhcp or discovery."""
    with _patch_wizlight(
        device=None, extended_white_range=extended_white_range, bulb_type=bulb_type
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": source}, data=data
        )
        await hass.async_block_till_done()

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "discovery_confirm"

    with (
        _patch_wizlight(
            device=None, extended_white_range=extended_white_range, bulb_type=bulb_type
        ),
        patch(
            "smarthub.components.wiz.async_setup_entry",
            return_value=True,
        ) as mock_setup_entry,
        patch(
            "smarthub.components.wiz.async_setup", return_value=True
        ) as mock_setup,
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {},
        )
        await hass.async_block_till_done()

    assert result2["type"] is FlowResultType.CREATE_ENTRY
    assert result2["title"] == name
    assert result2["data"] == {
        CONF_HOST: "1.1.1.1",
    }
    assert len(mock_setup.mock_calls) == 1
    assert len(mock_setup_entry.mock_calls) == 1


@pytest.mark.parametrize(
    ("source", "data"),
    [
        (config_entries.SOURCE_DHCP, DHCP_DISCOVERY),
        (config_entries.SOURCE_INTEGRATION_DISCOVERY, INTEGRATION_DISCOVERY),
    ],
)
async def test_discovered_by_dhcp_or_integration_discovery_updates_host(
    hass: SmartHub, source, data
) -> None:
    """Test dhcp or discovery updates existing host."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id=TEST_SYSTEM_INFO["id"],
        data={CONF_HOST: "dummy"},
    )
    entry.add_to_hass(hass)

    with _patch_wizlight():
        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": source}, data=data
        )
        await hass.async_block_till_done()

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "already_configured"
    assert entry.data[CONF_HOST] == FAKE_IP


@pytest.mark.parametrize(
    ("source", "data"),
    [
        (config_entries.SOURCE_DHCP, DHCP_DISCOVERY),
        (config_entries.SOURCE_INTEGRATION_DISCOVERY, INTEGRATION_DISCOVERY),
    ],
)
async def test_discovered_by_dhcp_or_integration_discovery_avoid_waiting_for_retry(
    hass: SmartHub, source, data
) -> None:
    """Test dhcp or discovery kicks off setup when in retry."""
    bulb = _mocked_wizlight(None, None, FAKE_SOCKET)
    bulb.getMac = AsyncMock(side_effect=OSError)
    _, entry = await async_setup_integration(hass, wizlight=bulb)
    assert entry.data[CONF_HOST] == FAKE_IP
    assert entry.state is ConfigEntryState.SETUP_RETRY
    bulb.getMac = AsyncMock(return_value=FAKE_MAC)

    with _patch_wizlight():
        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": source}, data=data
        )
        await hass.async_block_till_done()

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "already_configured"
    assert entry.state is ConfigEntryState.LOADED


async def test_setup_via_discovery(hass: SmartHub) -> None:
    """Test setting up via discovery."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    await hass.async_block_till_done()
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"
    assert not result["errors"]

    with _patch_discovery():
        result2 = await hass.config_entries.flow.async_configure(result["flow_id"], {})
        await hass.async_block_till_done()

    assert result2["type"] is FlowResultType.FORM
    assert result2["step_id"] == "pick_device"
    assert not result2["errors"]

    # test we can try again
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"
    assert not result["errors"]

    with _patch_discovery():
        result2 = await hass.config_entries.flow.async_configure(result["flow_id"], {})
        await hass.async_block_till_done()

    assert result2["type"] is FlowResultType.FORM
    assert result2["step_id"] == "pick_device"
    assert not result2["errors"]

    with (
        _patch_wizlight(),
        patch(
            "smarthub.components.wiz.async_setup", return_value=True
        ) as mock_setup,
        patch(
            "smarthub.components.wiz.async_setup_entry", return_value=True
        ) as mock_setup_entry,
    ):
        result3 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_DEVICE: FAKE_MAC},
        )
        await hass.async_block_till_done()

    assert result3["type"] is FlowResultType.CREATE_ENTRY
    assert result3["title"] == "WiZ Dimmable White ABCABC"
    assert result3["data"] == {
        CONF_HOST: "1.1.1.1",
    }
    assert len(mock_setup.mock_calls) == 1
    assert len(mock_setup_entry.mock_calls) == 1

    # ignore configured devices
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"
    assert not result["errors"]

    with _patch_discovery():
        result2 = await hass.config_entries.flow.async_configure(result["flow_id"], {})
        await hass.async_block_till_done()

    assert result2["type"] is FlowResultType.ABORT
    assert result2["reason"] == "no_devices_found"


async def test_setup_via_discovery_cannot_connect(hass: SmartHub) -> None:
    """Test setting up via discovery and we fail to connect to the discovered device."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    await hass.async_block_till_done()
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"
    assert not result["errors"]

    with _patch_discovery():
        result2 = await hass.config_entries.flow.async_configure(result["flow_id"], {})
        await hass.async_block_till_done()

    assert result2["type"] is FlowResultType.FORM
    assert result2["step_id"] == "pick_device"
    assert not result2["errors"]

    with (
        patch(
            "smarthub.components.wiz.wizlight.getBulbConfig",
            side_effect=WizLightTimeOutError,
        ),
        _patch_discovery(),
    ):
        result3 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_DEVICE: FAKE_MAC},
        )
        await hass.async_block_till_done()

    assert result3["type"] is FlowResultType.ABORT
    assert result3["reason"] == "cannot_connect"


async def test_setup_via_discovery_exception_finds_nothing(hass: SmartHub) -> None:
    """Test we do not find anything if discovery throws."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    await hass.async_block_till_done()
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"
    assert not result["errors"]

    with patch(
        "smarthub.components.wiz.discovery.find_wizlights",
        side_effect=OSError,
    ):
        result2 = await hass.config_entries.flow.async_configure(result["flow_id"], {})
        await hass.async_block_till_done()

    assert result2["type"] is FlowResultType.ABORT
    assert result2["reason"] == "no_devices_found"


async def test_discovery_with_firmware_update(hass: SmartHub) -> None:
    """Test we check the device again between first discovery and config entry creation."""
    with _patch_wizlight(
        device=None,
        extended_white_range=FAKE_EXTENDED_WHITE_RANGE,
        bulb_type=FAKE_RGBW_BULB,
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": config_entries.SOURCE_INTEGRATION_DISCOVERY},
            data=INTEGRATION_DISCOVERY,
        )
        await hass.async_block_till_done()

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "discovery_confirm"

    # In between discovery and when the user clicks to set it up the firmware
    # updates and we now can see its really RGBWW not RGBW since the older
    # firmwares did not tell us how many white channels exist

    with (
        patch(
            "smarthub.components.wiz.async_setup_entry",
            return_value=True,
        ) as mock_setup_entry,
        patch(
            "smarthub.components.wiz.async_setup", return_value=True
        ) as mock_setup,
        _patch_wizlight(
            device=None,
            extended_white_range=FAKE_EXTENDED_WHITE_RANGE,
            bulb_type=FAKE_RGBWW_BULB,
        ),
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {},
        )
        await hass.async_block_till_done()

    assert result2["type"] is FlowResultType.CREATE_ENTRY
    assert result2["title"] == "WiZ RGBWW Tunable ABCABC"
    assert result2["data"] == {
        CONF_HOST: "1.1.1.1",
    }
    assert len(mock_setup.mock_calls) == 1
    assert len(mock_setup_entry.mock_calls) == 1


@pytest.mark.parametrize(
    ("source", "data"),
    [
        (config_entries.SOURCE_DHCP, DHCP_DISCOVERY),
        (config_entries.SOURCE_INTEGRATION_DISCOVERY, INTEGRATION_DISCOVERY),
    ],
)
async def test_discovered_during_onboarding(hass: SmartHub, source, data) -> None:
    """Test dhcp or discovery during onboarding creates the config entry."""
    with (
        _patch_wizlight(),
        patch(
            "smarthub.components.wiz.async_setup_entry",
            return_value=True,
        ) as mock_setup_entry,
        patch(
            "smarthub.components.wiz.async_setup", return_value=True
        ) as mock_setup,
        patch(
            "smarthub.components.onboarding.async_is_onboarded", return_value=False
        ),
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": source}, data=data
        )
        await hass.async_block_till_done()

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "WiZ Dimmable White ABCABC"
    assert result["data"] == {
        CONF_HOST: "1.1.1.1",
    }
    assert len(mock_setup.mock_calls) == 1
    assert len(mock_setup_entry.mock_calls) == 1
