"""Test the Qingping config flow."""

from unittest.mock import patch

from smarthub import config_entries
from smarthub.components.qingping.const import DOMAIN
from smarthub.core import SmartHub
from smarthub.data_entry_flow import FlowResultType

from . import (
    LIGHT_AND_SIGNAL_SERVICE_INFO,
    NO_DATA_SERVICE_INFO,
    NOT_QINGPING_SERVICE_INFO,
)

from tests.common import MockConfigEntry


async def test_async_step_bluetooth_valid_device(hass: SmartHub) -> None:
    """Test discovery via bluetooth with a valid device."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": config_entries.SOURCE_BLUETOOTH},
        data=LIGHT_AND_SIGNAL_SERVICE_INFO,
    )
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "bluetooth_confirm"
    with patch(
        "smarthub.components.qingping.async_setup_entry", return_value=True
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"], user_input={}
        )
    assert result2["type"] is FlowResultType.CREATE_ENTRY
    assert result2["title"] == "Motion & Light EEFF"
    assert result2["data"] == {}
    assert result2["result"].unique_id == "aa:bb:cc:dd:ee:ff"


async def test_async_step_bluetooth_not_enough_info_at_start(
    hass: SmartHub,
) -> None:
    """Test discovery via bluetooth with only a partial adv at the start."""
    with patch(
        "smarthub.components.qingping.config_flow.async_process_advertisements",
        return_value=LIGHT_AND_SIGNAL_SERVICE_INFO,
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": config_entries.SOURCE_BLUETOOTH},
            data=NO_DATA_SERVICE_INFO,
        )
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "bluetooth_confirm"
    with patch(
        "smarthub.components.qingping.async_setup_entry", return_value=True
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"], user_input={}
        )
    assert result2["type"] is FlowResultType.CREATE_ENTRY
    assert result2["title"] == "Qingping Motion & Light"
    assert result2["data"] == {}
    assert result2["result"].unique_id == "aa:bb:cc:dd:ee:ff"


async def test_async_step_bluetooth_not_qingping(hass: SmartHub) -> None:
    """Test discovery via bluetooth not qingping."""
    with patch(
        "smarthub.components.qingping.config_flow.async_process_advertisements",
        side_effect=TimeoutError,
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": config_entries.SOURCE_BLUETOOTH},
            data=NOT_QINGPING_SERVICE_INFO,
        )
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "not_supported"


async def test_async_step_user_no_devices_found(hass: SmartHub) -> None:
    """Test setup from service info cache with no devices found."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": config_entries.SOURCE_USER},
    )
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "no_devices_found"


async def test_async_step_user_with_found_devices(hass: SmartHub) -> None:
    """Test setup from service info cache with devices found."""
    with patch(
        "smarthub.components.qingping.config_flow.async_discovered_service_info",
        return_value=[LIGHT_AND_SIGNAL_SERVICE_INFO],
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": config_entries.SOURCE_USER},
        )
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"
    with patch(
        "smarthub.components.qingping.async_setup_entry", return_value=True
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input={"address": "aa:bb:cc:dd:ee:ff"},
        )
    assert result2["type"] is FlowResultType.CREATE_ENTRY
    assert result2["title"] == "Motion & Light EEFF"
    assert result2["data"] == {}
    assert result2["result"].unique_id == "aa:bb:cc:dd:ee:ff"


async def test_async_step_user_replace_ignored(hass: SmartHub) -> None:
    """Test setup from service info can replace an ignored entry."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id=LIGHT_AND_SIGNAL_SERVICE_INFO.address,
        source=config_entries.SOURCE_IGNORE,
        data={},
    )
    entry.add_to_hass(hass)
    with patch(
        "smarthub.components.qingping.config_flow.async_discovered_service_info",
        return_value=[LIGHT_AND_SIGNAL_SERVICE_INFO],
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": config_entries.SOURCE_USER},
        )
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"
    with patch(
        "smarthub.components.qingping.async_setup_entry", return_value=True
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input={"address": "aa:bb:cc:dd:ee:ff"},
        )
    assert result2["type"] is FlowResultType.CREATE_ENTRY
    assert result2["title"] == "Motion & Light EEFF"
    assert result2["data"] == {}
    assert result2["result"].unique_id == "aa:bb:cc:dd:ee:ff"


async def test_async_step_user_device_added_between_steps(hass: SmartHub) -> None:
    """Test the device gets added via another flow between steps."""
    with patch(
        "smarthub.components.qingping.config_flow.async_discovered_service_info",
        return_value=[LIGHT_AND_SIGNAL_SERVICE_INFO],
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": config_entries.SOURCE_USER},
        )
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"

    entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id="aa:bb:cc:dd:ee:ff",
    )
    entry.add_to_hass(hass)

    with patch(
        "smarthub.components.qingping.async_setup_entry", return_value=True
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input={"address": "aa:bb:cc:dd:ee:ff"},
        )
    assert result2["type"] is FlowResultType.ABORT
    assert result2["reason"] == "already_configured"


async def test_async_step_user_with_found_devices_already_setup(
    hass: SmartHub,
) -> None:
    """Test setup from service info cache with devices found."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id="aa:bb:cc:dd:ee:ff",
    )
    entry.add_to_hass(hass)

    with patch(
        "smarthub.components.qingping.config_flow.async_discovered_service_info",
        return_value=[LIGHT_AND_SIGNAL_SERVICE_INFO],
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": config_entries.SOURCE_USER},
        )
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "no_devices_found"


async def test_async_step_bluetooth_devices_already_setup(hass: SmartHub) -> None:
    """Test we can't start a flow if there is already a config entry."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id="aa:bb:cc:dd:ee:ff",
    )
    entry.add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": config_entries.SOURCE_BLUETOOTH},
        data=LIGHT_AND_SIGNAL_SERVICE_INFO,
    )
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "already_configured"


async def test_async_step_bluetooth_already_in_progress(hass: SmartHub) -> None:
    """Test we can't start a flow for the same device twice."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": config_entries.SOURCE_BLUETOOTH},
        data=LIGHT_AND_SIGNAL_SERVICE_INFO,
    )
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "bluetooth_confirm"

    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": config_entries.SOURCE_BLUETOOTH},
        data=LIGHT_AND_SIGNAL_SERVICE_INFO,
    )
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "already_in_progress"


async def test_async_step_user_takes_precedence_over_discovery(
    hass: SmartHub,
) -> None:
    """Test manual setup takes precedence over discovery."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": config_entries.SOURCE_BLUETOOTH},
        data=LIGHT_AND_SIGNAL_SERVICE_INFO,
    )
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "bluetooth_confirm"

    with patch(
        "smarthub.components.qingping.config_flow.async_discovered_service_info",
        return_value=[LIGHT_AND_SIGNAL_SERVICE_INFO],
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": config_entries.SOURCE_USER},
        )
        assert result["type"] is FlowResultType.FORM

    with patch(
        "smarthub.components.qingping.async_setup_entry", return_value=True
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input={"address": "aa:bb:cc:dd:ee:ff"},
        )
    assert result2["type"] is FlowResultType.CREATE_ENTRY
    assert result2["title"] == "Motion & Light EEFF"
    assert result2["data"] == {}
    assert result2["result"].unique_id == "aa:bb:cc:dd:ee:ff"

    # Verify the original one was aborted
    assert not hass.config_entries.flow.async_progress(DOMAIN)
