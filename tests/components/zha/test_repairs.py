"""Test ZHA repairs."""

from http import HTTPStatus
from unittest.mock import Mock, call, patch

import pytest
from zigpy.application import ControllerApplication
import zigpy.backups
from zigpy.exceptions import NetworkSettingsInconsistent

from smarthub.components.smarthub_hardware.util import ApplicationType
from smarthub.components.smarthub_sky_connect.const import (  # pylint: disable=hass-component-root-import
    DOMAIN as SKYCONNECT_DOMAIN,
)
from smarthub.components.repairs import DOMAIN as REPAIRS_DOMAIN
from smarthub.components.zha.const import DOMAIN
from smarthub.components.zha.repairs.network_settings_inconsistent import (
    ISSUE_INCONSISTENT_NETWORK_SETTINGS,
)
from smarthub.components.zha.repairs.wrong_silabs_firmware import (
    ISSUE_WRONG_SILABS_FIRMWARE_INSTALLED,
    HardwareType,
    _detect_radio_hardware,
    warn_on_wrong_silabs_firmware,
)
from smarthub.config_entries import ConfigEntryState
from smarthub.core import SmartHub
from smarthub.exceptions import SmartHubError
from smarthub.helpers import issue_registry as ir
from smarthub.setup import async_setup_component

from tests.common import MockConfigEntry
from tests.typing import ClientSessionGenerator

SKYCONNECT_DEVICE = "/dev/serial/by-id/usb-Nabu_Casa_SkyConnect_v1.0_9e2adbd75b8beb119fe564a0f320645d-if00-port0"
CONNECT_ZBT1_DEVICE = "/dev/serial/by-id/usb-Nabu_Casa_Home_Assistant_Connect_ZBT-1_9e2adbd75b8beb119fe564a0f320645d-if00-port0"


def test_detect_radio_hardware(hass: SmartHub) -> None:
    """Test logic to detect radio hardware."""
    skyconnect_config_entry = MockConfigEntry(
        data={
            "device": SKYCONNECT_DEVICE,
            "vid": "10C4",
            "pid": "EA60",
            "serial_number": "3c0ed67c628beb11b1cd64a0f320645d",
            "manufacturer": "Nabu Casa",
            "product": "SkyConnect v1.0",
            "firmware": "ezsp",
        },
        version=1,
        minor_version=4,
        domain=SKYCONNECT_DOMAIN,
        options={},
        title="SmartHub SkyConnect",
    )
    skyconnect_config_entry.add_to_hass(hass)

    connect_zbt1_config_entry = MockConfigEntry(
        data={
            "device": CONNECT_ZBT1_DEVICE,
            "vid": "10C4",
            "pid": "EA60",
            "serial_number": "3c0ed67c628beb11b1cd64a0f320645d",
            "manufacturer": "Nabu Casa",
            "product": "SmartHub Connect ZBT-1",
            "firmware": "ezsp",
        },
        version=1,
        minor_version=4,
        domain=SKYCONNECT_DOMAIN,
        options={},
        title="SmartHub Connect ZBT-1",
    )
    connect_zbt1_config_entry.add_to_hass(hass)

    assert _detect_radio_hardware(hass, CONNECT_ZBT1_DEVICE) == HardwareType.SKYCONNECT
    assert _detect_radio_hardware(hass, SKYCONNECT_DEVICE) == HardwareType.SKYCONNECT
    assert (
        _detect_radio_hardware(hass, SKYCONNECT_DEVICE + "_foo") == HardwareType.OTHER
    )
    assert _detect_radio_hardware(hass, "/dev/ttyAMA1") == HardwareType.OTHER

    with patch(
        "smarthub.components.smarthub_yellow.hardware.get_os_info",
        return_value={"board": "yellow"},
    ):
        assert _detect_radio_hardware(hass, "/dev/ttyAMA1") == HardwareType.YELLOW
        assert _detect_radio_hardware(hass, "/dev/ttyAMA2") == HardwareType.OTHER
        assert (
            _detect_radio_hardware(hass, SKYCONNECT_DEVICE) == HardwareType.SKYCONNECT
        )


def test_detect_radio_hardware_failure(hass: SmartHub) -> None:
    """Test radio hardware detection failure."""

    with (
        patch(
            "smarthub.components.smarthub_yellow.hardware.async_info",
            side_effect=SmartHubError(),
        ),
        patch(
            "smarthub.components.smarthub_sky_connect.hardware.async_info",
            side_effect=SmartHubError(),
        ),
    ):
        assert _detect_radio_hardware(hass, SKYCONNECT_DEVICE) == HardwareType.OTHER


@pytest.mark.parametrize(
    ("detected_hardware"),
    [HardwareType.SKYCONNECT, HardwareType.YELLOW, HardwareType.OTHER],
)
async def test_multipan_firmware_repair(
    hass: SmartHub,
    detected_hardware: HardwareType,
    config_entry: MockConfigEntry,
    mock_zigpy_connect: ControllerApplication,
    issue_registry: ir.IssueRegistry,
) -> None:
    """Test creating a repair when multi-PAN firmware is installed and probed."""

    config_entry.add_to_hass(hass)

    # ZHA fails to set up
    with (
        patch(
            "smarthub.components.zha.repairs.wrong_silabs_firmware.probe_silabs_firmware_type",
            return_value=ApplicationType.CPC,
        ),
        patch(
            "smarthub.components.zha.Gateway.async_initialize",
            side_effect=RuntimeError(),
        ),
        patch(
            "smarthub.components.zha.repairs.wrong_silabs_firmware._detect_radio_hardware",
            return_value=detected_hardware,
        ),
    ):
        await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()

        assert config_entry.state is ConfigEntryState.SETUP_ERROR

    await hass.config_entries.async_unload(config_entry.entry_id)

    issue = issue_registry.async_get_issue(
        domain=DOMAIN,
        issue_id=ISSUE_WRONG_SILABS_FIRMWARE_INSTALLED,
    )

    # The issue is created when we fail to probe
    assert issue is not None
    assert issue.translation_placeholders["firmware_type"] == "CPC"

    # If ZHA manages to start up normally after this, the issue will be deleted
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    issue = issue_registry.async_get_issue(
        domain=DOMAIN,
        issue_id=ISSUE_WRONG_SILABS_FIRMWARE_INSTALLED,
    )
    assert issue is None


async def test_multipan_firmware_no_repair_on_probe_failure(
    hass: SmartHub, config_entry: MockConfigEntry, issue_registry: ir.IssueRegistry
) -> None:
    """Test that a repair is not created when multi-PAN firmware cannot be probed."""

    config_entry.add_to_hass(hass)

    # ZHA fails to set up
    with (
        patch(
            "smarthub.components.zha.repairs.wrong_silabs_firmware.probe_silabs_firmware_type",
            return_value=None,
        ),
        patch(
            "smarthub.components.zha.Gateway.async_initialize",
            side_effect=RuntimeError(),
        ),
    ):
        await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()

        assert config_entry.state is ConfigEntryState.SETUP_RETRY

    await hass.config_entries.async_unload(config_entry.entry_id)

    # No repair is created
    issue = issue_registry.async_get_issue(
        domain=DOMAIN,
        issue_id=ISSUE_WRONG_SILABS_FIRMWARE_INSTALLED,
    )
    assert issue is None


async def test_multipan_firmware_retry_on_probe_ezsp(
    hass: SmartHub,
    config_entry: MockConfigEntry,
    mock_zigpy_connect: ControllerApplication,
    issue_registry: ir.IssueRegistry,
) -> None:
    """Test that ZHA is reloaded when EZSP firmware is probed."""

    config_entry.add_to_hass(hass)

    # ZHA fails to set up
    with (
        patch(
            "smarthub.components.zha.repairs.wrong_silabs_firmware.probe_silabs_firmware_type",
            return_value=ApplicationType.EZSP,
        ),
        patch(
            "smarthub.components.zha.Gateway.async_initialize",
            side_effect=RuntimeError(),
        ),
    ):
        await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()

        # The config entry state is `SETUP_RETRY`, not `SETUP_ERROR`!
        assert config_entry.state is ConfigEntryState.SETUP_RETRY

    await hass.config_entries.async_unload(config_entry.entry_id)

    # No repair is created
    issue = issue_registry.async_get_issue(
        domain=DOMAIN,
        issue_id=ISSUE_WRONG_SILABS_FIRMWARE_INSTALLED,
    )
    assert issue is None


async def test_no_warn_on_socket(hass: SmartHub) -> None:
    """Test that no warning is issued when the device is a socket."""
    with patch(
        "smarthub.components.zha.repairs.wrong_silabs_firmware.probe_silabs_firmware_type",
    ) as mock_probe:
        await warn_on_wrong_silabs_firmware(hass, device="socket://1.2.3.4:5678")

    mock_probe.assert_not_called()


async def test_inconsistent_settings_keep_new(
    hass: SmartHub,
    hass_client: ClientSessionGenerator,
    config_entry: MockConfigEntry,
    mock_zigpy_connect: ControllerApplication,
    network_backup: zigpy.backups.NetworkBackup,
    issue_registry: ir.IssueRegistry,
) -> None:
    """Test inconsistent ZHA network settings: keep new settings."""

    assert await async_setup_component(hass, REPAIRS_DOMAIN, {REPAIRS_DOMAIN: {}})

    config_entry.add_to_hass(hass)

    new_state = network_backup.replace(
        network_info=network_backup.network_info.replace(pan_id=0xBBBB)
    )
    old_state = network_backup

    with patch(
        "smarthub.components.zha.Gateway.async_initialize",
        side_effect=NetworkSettingsInconsistent(
            message="Network settings are inconsistent",
            new_state=new_state,
            old_state=old_state,
        ),
    ):
        await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()

        assert config_entry.state is ConfigEntryState.SETUP_ERROR

    await hass.config_entries.async_unload(config_entry.entry_id)

    issue = issue_registry.async_get_issue(
        domain=DOMAIN,
        issue_id=ISSUE_INCONSISTENT_NETWORK_SETTINGS,
    )

    # The issue is created
    assert issue is not None

    client = await hass_client()
    resp = await client.post(
        "/api/repairs/issues/fix",
        json={"handler": DOMAIN, "issue_id": issue.issue_id},
    )

    assert resp.status == HTTPStatus.OK
    data = await resp.json()

    flow_id = data["flow_id"]
    assert data["description_placeholders"]["diff"] == "- PAN ID: `0x2DB4` → `0xBBBB`"

    mock_zigpy_connect.backups.add_backup = Mock()

    resp = await client.post(
        f"/api/repairs/issues/fix/{flow_id}",
        json={"next_step_id": "use_new_settings"},
    )
    await hass.async_block_till_done()

    assert resp.status == HTTPStatus.OK
    data = await resp.json()
    assert data["type"] == "create_entry"

    await hass.config_entries.async_unload(config_entry.entry_id)

    assert (
        issue_registry.async_get_issue(
            domain=DOMAIN,
            issue_id=ISSUE_INCONSISTENT_NETWORK_SETTINGS,
        )
        is None
    )

    assert mock_zigpy_connect.backups.add_backup.mock_calls == [call(new_state)]


async def test_inconsistent_settings_restore_old(
    hass: SmartHub,
    hass_client: ClientSessionGenerator,
    config_entry: MockConfigEntry,
    mock_zigpy_connect: ControllerApplication,
    network_backup: zigpy.backups.NetworkBackup,
    issue_registry: ir.IssueRegistry,
) -> None:
    """Test inconsistent ZHA network settings: restore last backup."""

    assert await async_setup_component(hass, REPAIRS_DOMAIN, {REPAIRS_DOMAIN: {}})

    config_entry.add_to_hass(hass)

    new_state = network_backup.replace(
        network_info=network_backup.network_info.replace(pan_id=0xBBBB)
    )
    old_state = network_backup

    with patch(
        "smarthub.components.zha.Gateway.async_initialize",
        side_effect=NetworkSettingsInconsistent(
            message="Network settings are inconsistent",
            new_state=new_state,
            old_state=old_state,
        ),
    ):
        await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()

        assert config_entry.state is ConfigEntryState.SETUP_ERROR

    await hass.config_entries.async_unload(config_entry.entry_id)

    issue = issue_registry.async_get_issue(
        domain=DOMAIN,
        issue_id=ISSUE_INCONSISTENT_NETWORK_SETTINGS,
    )

    # The issue is created
    assert issue is not None

    client = await hass_client()
    resp = await client.post(
        "/api/repairs/issues/fix",
        json={"handler": DOMAIN, "issue_id": issue.issue_id},
    )

    assert resp.status == HTTPStatus.OK
    data = await resp.json()

    flow_id = data["flow_id"]
    assert data["description_placeholders"]["diff"] == "- PAN ID: `0x2DB4` → `0xBBBB`"

    resp = await client.post(
        f"/api/repairs/issues/fix/{flow_id}",
        json={"next_step_id": "restore_old_settings"},
    )
    await hass.async_block_till_done()

    assert resp.status == HTTPStatus.OK
    data = await resp.json()
    assert data["type"] == "create_entry"

    await hass.config_entries.async_unload(config_entry.entry_id)

    assert (
        issue_registry.async_get_issue(
            domain=DOMAIN,
            issue_id=ISSUE_INCONSISTENT_NETWORK_SETTINGS,
        )
        is None
    )

    assert mock_zigpy_connect.backups.restore_backup.mock_calls == [call(old_state)]
