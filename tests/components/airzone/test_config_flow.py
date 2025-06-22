"""Define tests for the Airzone config flow."""

from unittest.mock import patch

from aioairzone.const import API_MAC, API_SYSTEMS
from aioairzone.exceptions import (
    AirzoneError,
    HotWaterNotAvailable,
    InvalidMethod,
    InvalidSystem,
    SystemOutOfRange,
)

from smarthub import config_entries
from smarthub.components.airzone.config_flow import short_mac
from smarthub.components.airzone.const import DOMAIN
from smarthub.config_entries import SOURCE_USER, ConfigEntryState
from smarthub.const import CONF_HOST, CONF_ID, CONF_PORT
from smarthub.core import SmartHub
from smarthub.data_entry_flow import FlowResultType
from smarthub.helpers import device_registry as dr
from smarthub.helpers.service_info.dhcp import DhcpServiceInfo

from .util import (
    CONFIG,
    CONFIG_ID1,
    HVAC_DHW_MOCK,
    HVAC_MOCK,
    HVAC_VERSION_MOCK,
    HVAC_WEBSERVER_MOCK,
    USER_INPUT,
)

from tests.common import MockConfigEntry

DHCP_SERVICE_INFO = DhcpServiceInfo(
    hostname="airzone",
    ip="192.168.1.100",
    macaddress=dr.format_mac("E84F25000000").replace(":", ""),
)

TEST_ID = 1
TEST_IP = DHCP_SERVICE_INFO.ip
TEST_PORT = 3000


async def test_form(hass: SmartHub) -> None:
    """Test that the form is served with valid input."""

    with (
        patch(
            "smarthub.components.airzone.async_setup_entry",
            return_value=True,
        ) as mock_setup_entry,
        patch(
            "smarthub.components.airzone.AirzoneLocalApi.get_dhw",
            return_value=HVAC_DHW_MOCK,
        ),
        patch(
            "smarthub.components.airzone.AirzoneLocalApi.get_hvac",
            return_value=HVAC_MOCK,
        ),
        patch(
            "smarthub.components.airzone.AirzoneLocalApi.get_hvac_systems",
            side_effect=SystemOutOfRange,
        ),
        patch(
            "smarthub.components.airzone.AirzoneLocalApi.get_version",
            return_value=HVAC_VERSION_MOCK,
        ),
        patch(
            "smarthub.components.airzone.AirzoneLocalApi.get_webserver",
            return_value=HVAC_WEBSERVER_MOCK,
        ),
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": SOURCE_USER}
        )

        assert result["type"] is FlowResultType.FORM
        assert result["step_id"] == "user"
        assert result["errors"] == {}

        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], USER_INPUT
        )

        await hass.async_block_till_done()

        conf_entries = hass.config_entries.async_entries(DOMAIN)
        entry = conf_entries[0]
        assert entry.state is ConfigEntryState.LOADED

        assert result["type"] is FlowResultType.CREATE_ENTRY
        assert result["title"] == f"Airzone {CONFIG[CONF_HOST]}:{CONFIG[CONF_PORT]}"
        assert result["data"][CONF_HOST] == CONFIG[CONF_HOST]
        assert result["data"][CONF_PORT] == CONFIG[CONF_PORT]
        assert result["data"][CONF_ID] == CONFIG[CONF_ID]

        assert len(mock_setup_entry.mock_calls) == 1


async def test_form_invalid_system_id(hass: SmartHub) -> None:
    """Test Invalid System ID 0."""

    with (
        patch(
            "smarthub.components.airzone.async_setup_entry",
            return_value=True,
        ) as mock_setup_entry,
        patch(
            "smarthub.components.airzone.AirzoneLocalApi.get_dhw",
            side_effect=HotWaterNotAvailable,
        ),
        patch(
            "smarthub.components.airzone.AirzoneLocalApi.get_hvac",
            side_effect=InvalidSystem,
        ) as mock_hvac,
        patch(
            "smarthub.components.airzone.AirzoneLocalApi.get_hvac_systems",
            side_effect=SystemOutOfRange,
        ),
        patch(
            "smarthub.components.airzone.AirzoneLocalApi.get_version",
            return_value=HVAC_VERSION_MOCK,
        ),
        patch(
            "smarthub.components.airzone.AirzoneLocalApi.get_webserver",
            side_effect=InvalidMethod,
        ),
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": SOURCE_USER}, data=USER_INPUT
        )

        assert result["type"] is FlowResultType.FORM
        assert result["step_id"] == "user"
        assert result["errors"] == {CONF_ID: "invalid_system_id"}

        mock_hvac.return_value = HVAC_MOCK[API_SYSTEMS][0]
        mock_hvac.side_effect = None

        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], CONFIG_ID1
        )

        assert result["type"] is FlowResultType.CREATE_ENTRY

        await hass.async_block_till_done()

        conf_entries = hass.config_entries.async_entries(DOMAIN)
        entry = conf_entries[0]
        assert entry.state is ConfigEntryState.LOADED

        assert result["type"] is FlowResultType.CREATE_ENTRY
        assert (
            result["title"]
            == f"Airzone {CONFIG_ID1[CONF_HOST]}:{CONFIG_ID1[CONF_PORT]} #{CONFIG_ID1[CONF_ID]}"
        )
        assert result["data"][CONF_HOST] == CONFIG_ID1[CONF_HOST]
        assert result["data"][CONF_PORT] == CONFIG_ID1[CONF_PORT]
        assert result["data"][CONF_ID] == CONFIG_ID1[CONF_ID]

        mock_setup_entry.assert_called_once()


async def test_form_duplicated_id(hass: SmartHub) -> None:
    """Test setting up duplicated entry."""

    config_entry = MockConfigEntry(
        minor_version=2,
        data=CONFIG,
        domain=DOMAIN,
        unique_id="airzone_unique_id",
    )
    config_entry.add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}, data=USER_INPUT
    )

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "already_configured"


async def test_connection_error(hass: SmartHub) -> None:
    """Test connection to host error."""

    with patch(
        "smarthub.components.airzone.AirzoneLocalApi.validate",
        side_effect=AirzoneError,
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": SOURCE_USER}, data=USER_INPUT
        )

        assert result["errors"] == {"base": "cannot_connect"}


async def test_dhcp_flow(hass: SmartHub) -> None:
    """Test that DHCP discovery works."""

    with patch(
        "smarthub.components.airzone.AirzoneLocalApi.get_version",
        return_value=HVAC_VERSION_MOCK,
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            data=DHCP_SERVICE_INFO,
            context={"source": config_entries.SOURCE_DHCP},
        )

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "discovered_connection"

    with (
        patch(
            "smarthub.components.airzone.async_setup_entry",
            return_value=True,
        ) as mock_setup_entry,
        patch(
            "smarthub.components.airzone.AirzoneLocalApi.get_dhw",
            return_value=HVAC_DHW_MOCK,
        ),
        patch(
            "smarthub.components.airzone.AirzoneLocalApi.get_hvac",
            return_value=HVAC_MOCK,
        ),
        patch(
            "smarthub.components.airzone.AirzoneLocalApi.get_hvac_systems",
            side_effect=SystemOutOfRange,
        ),
        patch(
            "smarthub.components.airzone.AirzoneLocalApi.get_version",
            return_value=HVAC_VERSION_MOCK,
        ),
        patch(
            "smarthub.components.airzone.AirzoneLocalApi.get_webserver",
            return_value=HVAC_WEBSERVER_MOCK,
        ),
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_PORT: TEST_PORT,
            },
        )

    assert result2["type"] is FlowResultType.CREATE_ENTRY
    assert result2["data"] == {
        CONF_HOST: TEST_IP,
        CONF_PORT: TEST_PORT,
    }

    assert len(mock_setup_entry.mock_calls) == 1


async def test_dhcp_flow_error(hass: SmartHub) -> None:
    """Test that DHCP discovery fails."""

    with patch(
        "smarthub.components.airzone.AirzoneLocalApi.get_version",
        side_effect=AirzoneError,
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            data=DHCP_SERVICE_INFO,
            context={"source": config_entries.SOURCE_DHCP},
        )

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "cannot_connect"


async def test_dhcp_connection_error(hass: SmartHub) -> None:
    """Test DHCP connection to host error."""

    with patch(
        "smarthub.components.airzone.AirzoneLocalApi.get_version",
        return_value=HVAC_VERSION_MOCK,
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            data=DHCP_SERVICE_INFO,
            context={"source": config_entries.SOURCE_DHCP},
        )

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "discovered_connection"

    with patch(
        "smarthub.components.airzone.AirzoneLocalApi.validate",
        side_effect=AirzoneError,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_PORT: 3001,
            },
        )

        assert result["errors"] == {"base": "cannot_connect"}

    with (
        patch(
            "smarthub.components.airzone.async_setup_entry",
            return_value=True,
        ) as mock_setup_entry,
        patch(
            "smarthub.components.airzone.AirzoneLocalApi.get_dhw",
            return_value=HVAC_DHW_MOCK,
        ),
        patch(
            "smarthub.components.airzone.AirzoneLocalApi.get_hvac",
            return_value=HVAC_MOCK,
        ),
        patch(
            "smarthub.components.airzone.AirzoneLocalApi.get_hvac_systems",
            side_effect=SystemOutOfRange,
        ),
        patch(
            "smarthub.components.airzone.AirzoneLocalApi.get_version",
            return_value=HVAC_VERSION_MOCK,
        ),
        patch(
            "smarthub.components.airzone.AirzoneLocalApi.get_webserver",
            return_value=HVAC_WEBSERVER_MOCK,
        ),
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_PORT: TEST_PORT,
            },
        )

        await hass.async_block_till_done()

        conf_entries = hass.config_entries.async_entries(DOMAIN)
        entry = conf_entries[0]
        assert entry.state is ConfigEntryState.LOADED

        assert result["type"] is FlowResultType.CREATE_ENTRY
        assert result["title"] == f"Airzone {short_mac(HVAC_WEBSERVER_MOCK[API_MAC])}"
        assert result["data"][CONF_HOST] == TEST_IP
        assert result["data"][CONF_PORT] == TEST_PORT

        mock_setup_entry.assert_called_once()


async def test_dhcp_invalid_system_id(hass: SmartHub) -> None:
    """Test Invalid System ID 0."""

    with patch(
        "smarthub.components.airzone.AirzoneLocalApi.get_version",
        return_value=HVAC_VERSION_MOCK,
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            data=DHCP_SERVICE_INFO,
            context={"source": config_entries.SOURCE_DHCP},
        )

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "discovered_connection"

    with (
        patch(
            "smarthub.components.airzone.async_setup_entry",
            return_value=True,
        ) as mock_setup_entry,
        patch(
            "smarthub.components.airzone.AirzoneLocalApi.get_dhw",
            side_effect=HotWaterNotAvailable,
        ),
        patch(
            "smarthub.components.airzone.AirzoneLocalApi.get_hvac",
            side_effect=InvalidSystem,
        ) as mock_hvac,
        patch(
            "smarthub.components.airzone.AirzoneLocalApi.get_hvac_systems",
            side_effect=SystemOutOfRange,
        ),
        patch(
            "smarthub.components.airzone.AirzoneLocalApi.get_version",
            return_value=HVAC_VERSION_MOCK,
        ),
        patch(
            "smarthub.components.airzone.AirzoneLocalApi.get_webserver",
            side_effect=InvalidMethod,
        ),
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_PORT: TEST_PORT,
            },
        )

        assert result["type"] is FlowResultType.FORM
        assert result["step_id"] == "discovered_connection"
        assert result["errors"] == {CONF_ID: "invalid_system_id"}

        mock_hvac.return_value = HVAC_MOCK[API_SYSTEMS][0]
        mock_hvac.side_effect = None

        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_PORT: TEST_PORT,
                CONF_ID: TEST_ID,
            },
        )

        await hass.async_block_till_done()

        conf_entries = hass.config_entries.async_entries(DOMAIN)
        entry = conf_entries[0]
        assert entry.state is ConfigEntryState.LOADED

        assert result["type"] is FlowResultType.CREATE_ENTRY
        assert result["title"] == f"Airzone {short_mac(DHCP_SERVICE_INFO.macaddress)}"
        assert result["data"][CONF_HOST] == TEST_IP
        assert result["data"][CONF_PORT] == TEST_PORT
        assert result["data"][CONF_ID] == TEST_ID

        mock_setup_entry.assert_called_once()
