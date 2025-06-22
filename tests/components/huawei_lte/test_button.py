"""Tests for the Huawei LTE switches."""

from unittest.mock import MagicMock, patch

from huawei_lte_api.enums.device import ControlModeEnum

from smarthub.components.button import DOMAIN as BUTTON_DOMAIN, SERVICE_PRESS
from smarthub.components.huawei_lte.const import (
    BUTTON_KEY_CLEAR_TRAFFIC_STATISTICS,
    BUTTON_KEY_RESTART,
    DOMAIN,
    SERVICE_SUSPEND_INTEGRATION,
)
from smarthub.const import ATTR_ENTITY_ID, CONF_URL
from smarthub.core import SmartHub

from . import magic_client

from tests.common import MockConfigEntry

MOCK_CONF_URL = "http://huawei-lte.example.com"


@patch("smarthub.components.huawei_lte.Connection", MagicMock())
@patch("smarthub.components.huawei_lte.Client", return_value=magic_client({}))
async def test_clear_traffic_statistics(client, hass: SmartHub) -> None:
    """Test clear traffic statistics button."""
    huawei_lte = MockConfigEntry(domain=DOMAIN, data={CONF_URL: MOCK_CONF_URL})
    huawei_lte.add_to_hass(hass)
    await hass.config_entries.async_setup(huawei_lte.entry_id)
    await hass.async_block_till_done()
    await hass.services.async_call(
        BUTTON_DOMAIN,
        SERVICE_PRESS,
        {ATTR_ENTITY_ID: f"button.lte_{BUTTON_KEY_CLEAR_TRAFFIC_STATISTICS}"},
        blocking=True,
    )
    await hass.async_block_till_done()
    client.return_value.monitoring.set_clear_traffic.assert_called_once()

    client.return_value.monitoring.set_clear_traffic.reset_mock()
    await hass.services.async_call(
        DOMAIN,
        SERVICE_SUSPEND_INTEGRATION,
        {CONF_URL: MOCK_CONF_URL},
        blocking=True,
    )
    await hass.async_block_till_done()
    client.return_value.monitoring.set_clear_traffic.assert_not_called()


@patch("smarthub.components.huawei_lte.Connection", MagicMock())
@patch("smarthub.components.huawei_lte.Client", return_value=magic_client({}))
async def test_restart(client, hass: SmartHub) -> None:
    """Test restart button."""
    huawei_lte = MockConfigEntry(domain=DOMAIN, data={CONF_URL: MOCK_CONF_URL})
    huawei_lte.add_to_hass(hass)
    await hass.config_entries.async_setup(huawei_lte.entry_id)
    await hass.async_block_till_done()
    await hass.services.async_call(
        BUTTON_DOMAIN,
        SERVICE_PRESS,
        {ATTR_ENTITY_ID: f"button.lte_{BUTTON_KEY_RESTART}"},
        blocking=True,
    )
    await hass.async_block_till_done()
    client.return_value.device.set_control.assert_called_with(ControlModeEnum.REBOOT)

    client.return_value.device.set_control.reset_mock()
    await hass.services.async_call(
        DOMAIN,
        SERVICE_SUSPEND_INTEGRATION,
        {CONF_URL: MOCK_CONF_URL},
        blocking=True,
    )
    await hass.async_block_till_done()
    client.return_value.device.set_control.assert_not_called()
