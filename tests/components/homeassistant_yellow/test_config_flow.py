"""Test the SmartHub Yellow config flow."""

from collections.abc import Generator
from unittest.mock import AsyncMock, Mock, patch

import pytest

from smarthub.components.hassio import (
    DOMAIN as HASSIO_DOMAIN,
    AddonInfo,
    AddonState,
)
from smarthub.components.smarthub_hardware.firmware_config_flow import (
    STEP_PICK_FIRMWARE_ZIGBEE,
)
from smarthub.components.smarthub_hardware.silabs_multiprotocol_addon import (
    CONF_DISABLE_MULTI_PAN,
    get_flasher_addon_manager,
    get_multiprotocol_addon_manager,
)
from smarthub.components.smarthub_hardware.util import (
    ApplicationType,
    FirmwareInfo,
)
from smarthub.components.smarthub_yellow.const import DOMAIN, RADIO_DEVICE
from smarthub.core import SmartHub
from smarthub.data_entry_flow import FlowResultType
from smarthub.setup import async_setup_component

from tests.common import MockConfigEntry, MockModule, mock_integration


@pytest.fixture(autouse=True)
def config_flow_handler(hass: SmartHub) -> Generator[None]:
    """Fixture for a test config flow."""
    with patch(
        "smarthub.components.smarthub_hardware.silabs_multiprotocol_addon.WaitingAddonManager.async_wait_until_addon_state"
    ):
        yield


@pytest.fixture(autouse=True)
def mock_get_supervisor_client(supervisor_client: AsyncMock) -> Generator[None]:
    """Mock get_supervisor_client method."""
    with patch(
        "smarthub.components.smarthub_yellow.config_flow.get_supervisor_client",
        return_value=supervisor_client,
    ):
        yield


@pytest.fixture(name="get_yellow_settings")
def mock_get_yellow_settings():
    """Mock getting yellow settings."""
    with patch(
        "smarthub.components.smarthub_yellow.config_flow.async_get_yellow_settings",
        return_value={"disk_led": True, "heartbeat_led": True, "power_led": True},
    ) as get_yellow_settings:
        yield get_yellow_settings


@pytest.fixture(name="set_yellow_settings")
def mock_set_yellow_settings():
    """Mock setting yellow settings."""
    with patch(
        "smarthub.components.smarthub_yellow.config_flow.async_set_yellow_settings",
    ) as set_yellow_settings:
        yield set_yellow_settings


@pytest.fixture(name="reboot_host")
def mock_reboot_host(supervisor_client: AsyncMock) -> AsyncMock:
    """Mock rebooting host."""
    return supervisor_client.host.reboot


async def test_config_flow(hass: SmartHub) -> None:
    """Test the config flow."""
    mock_integration(hass, MockModule("hassio"))
    await async_setup_component(hass, HASSIO_DOMAIN, {})

    with (
        patch(
            "smarthub.components.smarthub_yellow.async_setup_entry",
            return_value=True,
        ) as mock_setup_entry,
        patch(
            "smarthub.components.smarthub_hardware.firmware_config_flow.probe_silabs_firmware_info",
            return_value=FirmwareInfo(
                device=RADIO_DEVICE,
                firmware_type=ApplicationType.EZSP,
                firmware_version=None,
                owners=[],
                source="probe",
            ),
        ),
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": "system"}
        )

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "SmartHub Yellow"
    assert result["data"] == {"firmware": "ezsp", "firmware_version": None}
    assert result["options"] == {}
    assert len(mock_setup_entry.mock_calls) == 1

    config_entry = hass.config_entries.async_entries(DOMAIN)[0]
    assert config_entry.data == {"firmware": "ezsp", "firmware_version": None}
    assert config_entry.options == {}
    assert config_entry.title == "SmartHub Yellow"


async def test_config_flow_single_entry(hass: SmartHub) -> None:
    """Test only a single entry is allowed."""
    mock_integration(hass, MockModule("hassio"))
    await async_setup_component(hass, HASSIO_DOMAIN, {})

    # Setup the config entry
    config_entry = MockConfigEntry(
        data={"firmware": ApplicationType.EZSP},
        domain=DOMAIN,
        options={},
        title="SmartHub Yellow",
        version=1,
        minor_version=2,
    )
    config_entry.add_to_hass(hass)

    with patch(
        "smarthub.components.smarthub_yellow.async_setup_entry",
        return_value=True,
    ) as mock_setup_entry:
        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": "system"}
        )

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "single_instance_allowed"
    mock_setup_entry.assert_not_called()


@pytest.mark.parametrize(
    ("reboot_menu_choice", "reboot_calls"),
    [("reboot_now", 1), ("reboot_later", 0)],
)
async def test_option_flow_led_settings(
    hass: SmartHub,
    get_yellow_settings: AsyncMock,
    set_yellow_settings: AsyncMock,
    reboot_host: AsyncMock,
    reboot_menu_choice: str,
    reboot_calls: int,
) -> None:
    """Test updating LED settings."""
    mock_integration(hass, MockModule("hassio"))
    await async_setup_component(hass, HASSIO_DOMAIN, {})

    # Setup the config entry
    config_entry = MockConfigEntry(
        data={"firmware": ApplicationType.EZSP},
        domain=DOMAIN,
        options={},
        title="SmartHub Yellow",
        version=1,
        minor_version=2,
    )
    config_entry.add_to_hass(hass)

    result = await hass.config_entries.options.async_init(config_entry.entry_id)
    assert result["type"] is FlowResultType.MENU
    assert result["step_id"] == "main_menu"

    result = await hass.config_entries.options.async_configure(
        result["flow_id"],
        {"next_step_id": "hardware_settings"},
    )
    assert result["type"] is FlowResultType.FORM

    result = await hass.config_entries.options.async_configure(
        result["flow_id"],
        {"disk_led": False, "heartbeat_led": False, "power_led": False},
    )
    assert result["type"] is FlowResultType.MENU
    assert result["step_id"] == "reboot_menu"
    set_yellow_settings.assert_called_once_with(
        hass, {"disk_led": False, "heartbeat_led": False, "power_led": False}
    )

    result = await hass.config_entries.options.async_configure(
        result["flow_id"],
        {"next_step_id": reboot_menu_choice},
    )
    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert reboot_host.call_count == reboot_calls


async def test_option_flow_led_settings_unchanged(
    hass: SmartHub,
    get_yellow_settings,
    set_yellow_settings,
) -> None:
    """Test updating LED settings."""
    mock_integration(hass, MockModule("hassio"))
    await async_setup_component(hass, HASSIO_DOMAIN, {})

    # Setup the config entry
    config_entry = MockConfigEntry(
        data={"firmware": ApplicationType.EZSP},
        domain=DOMAIN,
        options={},
        title="SmartHub Yellow",
        version=1,
        minor_version=2,
    )
    config_entry.add_to_hass(hass)

    result = await hass.config_entries.options.async_init(config_entry.entry_id)
    assert result["type"] is FlowResultType.MENU
    assert result["step_id"] == "main_menu"

    result = await hass.config_entries.options.async_configure(
        result["flow_id"],
        {"next_step_id": "hardware_settings"},
    )
    assert result["type"] is FlowResultType.FORM

    result = await hass.config_entries.options.async_configure(
        result["flow_id"],
        {"disk_led": True, "heartbeat_led": True, "power_led": True},
    )
    assert result["type"] is FlowResultType.CREATE_ENTRY
    set_yellow_settings.assert_not_called()


async def test_option_flow_led_settings_fail_1(hass: SmartHub) -> None:
    """Test updating LED settings."""
    mock_integration(hass, MockModule("hassio"))
    await async_setup_component(hass, HASSIO_DOMAIN, {})

    # Setup the config entry
    config_entry = MockConfigEntry(
        data={"firmware": ApplicationType.EZSP},
        domain=DOMAIN,
        options={},
        title="SmartHub Yellow",
        version=1,
        minor_version=2,
    )
    config_entry.add_to_hass(hass)

    result = await hass.config_entries.options.async_init(config_entry.entry_id)
    assert result["type"] is FlowResultType.MENU
    assert result["step_id"] == "main_menu"

    with patch(
        "smarthub.components.smarthub_yellow.config_flow.async_get_yellow_settings",
        side_effect=TimeoutError,
    ):
        result = await hass.config_entries.options.async_configure(
            result["flow_id"],
            {"next_step_id": "hardware_settings"},
        )
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "read_hw_settings_error"


async def test_option_flow_led_settings_fail_2(
    hass: SmartHub, get_yellow_settings
) -> None:
    """Test updating LED settings."""
    mock_integration(hass, MockModule("hassio"))
    await async_setup_component(hass, HASSIO_DOMAIN, {})

    # Setup the config entry
    config_entry = MockConfigEntry(
        data={"firmware": ApplicationType.EZSP},
        domain=DOMAIN,
        options={},
        title="SmartHub Yellow",
        version=1,
        minor_version=2,
    )
    config_entry.add_to_hass(hass)

    result = await hass.config_entries.options.async_init(config_entry.entry_id)
    assert result["type"] is FlowResultType.MENU
    assert result["step_id"] == "main_menu"

    result = await hass.config_entries.options.async_configure(
        result["flow_id"],
        {"next_step_id": "hardware_settings"},
    )
    assert result["type"] is FlowResultType.FORM

    with patch(
        "smarthub.components.smarthub_yellow.config_flow.async_set_yellow_settings",
        side_effect=TimeoutError,
    ):
        result = await hass.config_entries.options.async_configure(
            result["flow_id"],
            {"disk_led": False, "heartbeat_led": False, "power_led": False},
        )
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "write_hw_settings_error"


async def test_firmware_options_flow(hass: SmartHub) -> None:
    """Test the firmware options flow for Yellow."""
    mock_integration(hass, MockModule("hassio"))
    await async_setup_component(hass, HASSIO_DOMAIN, {})

    config_entry = MockConfigEntry(
        data={"firmware": ApplicationType.SPINEL},
        domain=DOMAIN,
        options={},
        title="SmartHub Yellow",
        version=1,
        minor_version=2,
    )
    config_entry.add_to_hass(hass)

    # First step is confirmation
    result = await hass.config_entries.options.async_init(config_entry.entry_id)
    assert result["type"] is FlowResultType.MENU
    assert result["step_id"] == "main_menu"
    assert "firmware_settings" in result["menu_options"]

    # Pick firmware settings
    result = await hass.config_entries.options.async_configure(
        result["flow_id"],
        user_input={"next_step_id": "firmware_settings"},
    )

    assert result["step_id"] == "pick_firmware"
    assert result["description_placeholders"]["firmware_type"] == "spinel"
    assert result["description_placeholders"]["model"] == "SmartHub Yellow"

    async def mock_async_step_pick_firmware_zigbee(self, data):
        return await self.async_step_confirm_zigbee(user_input={})

    with (
        patch(
            "smarthub.components.smarthub_hardware.firmware_config_flow.BaseFirmwareOptionsFlow.async_step_pick_firmware_zigbee",
            autospec=True,
            side_effect=mock_async_step_pick_firmware_zigbee,
        ),
        patch(
            "smarthub.components.smarthub_hardware.firmware_config_flow.probe_silabs_firmware_info",
            return_value=FirmwareInfo(
                device=RADIO_DEVICE,
                firmware_type=ApplicationType.EZSP,
                firmware_version="7.4.4.0 build 0",
                owners=[],
                source="probe",
            ),
        ),
    ):
        result = await hass.config_entries.options.async_configure(
            result["flow_id"],
            user_input={"next_step_id": STEP_PICK_FIRMWARE_ZIGBEE},
        )

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["result"] is True

    assert config_entry.data == {
        "firmware": "ezsp",
        "firmware_version": "7.4.4.0 build 0",
    }


@pytest.mark.usefixtures("supervisor_client")
async def test_options_flow_multipan_uninstall(hass: SmartHub) -> None:
    """Test options flow for when multi-PAN firmware is installed."""
    mock_integration(hass, MockModule("hassio"))
    await async_setup_component(hass, HASSIO_DOMAIN, {})

    config_entry = MockConfigEntry(
        data={"firmware": ApplicationType.CPC},
        domain=DOMAIN,
        options={},
        title="SmartHub Yellow",
        version=1,
        minor_version=2,
    )
    config_entry.add_to_hass(hass)

    # Multi-PAN addon is running
    mock_multipan_manager = Mock(spec_set=await get_multiprotocol_addon_manager(hass))
    mock_multipan_manager.async_get_addon_info.return_value = AddonInfo(
        available=True,
        hostname=None,
        options={"device": RADIO_DEVICE},
        state=AddonState.RUNNING,
        update_available=False,
        version="1.0.0",
    )

    mock_flasher_manager = Mock(spec_set=get_flasher_addon_manager(hass))
    mock_flasher_manager.async_get_addon_info.return_value = AddonInfo(
        available=True,
        hostname=None,
        options={},
        state=AddonState.NOT_RUNNING,
        update_available=False,
        version="1.0.0",
    )

    with (
        patch(
            "smarthub.components.smarthub_hardware.silabs_multiprotocol_addon.get_multiprotocol_addon_manager",
            return_value=mock_multipan_manager,
        ),
        patch(
            "smarthub.components.smarthub_hardware.silabs_multiprotocol_addon.get_flasher_addon_manager",
            return_value=mock_flasher_manager,
        ),
        patch(
            "smarthub.components.smarthub_hardware.silabs_multiprotocol_addon.is_hassio",
            return_value=True,
        ),
    ):
        result = await hass.config_entries.options.async_init(config_entry.entry_id)
        assert result["type"] is FlowResultType.MENU
        assert result["step_id"] == "main_menu"
        assert "multipan_settings" in result["menu_options"]

        # Pick multi-PAN settings
        result = await hass.config_entries.options.async_configure(
            result["flow_id"],
            user_input={"next_step_id": "multipan_settings"},
        )

        # Pick the uninstall option
        result = await hass.config_entries.options.async_configure(
            result["flow_id"],
            user_input={"next_step_id": "uninstall_addon"},
        )

        # Check the box
        result = await hass.config_entries.options.async_configure(
            result["flow_id"], user_input={CONF_DISABLE_MULTI_PAN: True}
        )

        # Finish the flow
        result = await hass.config_entries.options.async_configure(result["flow_id"])
        await hass.async_block_till_done(wait_background_tasks=True)
        result = await hass.config_entries.options.async_configure(result["flow_id"])
        await hass.async_block_till_done(wait_background_tasks=True)
        result = await hass.config_entries.options.async_configure(result["flow_id"])
        assert result["type"] is FlowResultType.CREATE_ENTRY

    # We've reverted the firmware back to Zigbee
    assert config_entry.data["firmware"] == "ezsp"
