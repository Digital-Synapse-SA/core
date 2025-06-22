"""Test the SmartHub Green hardware platform."""

from unittest.mock import patch

import pytest

from smarthub.components.hassio import DOMAIN as HASSIO_DOMAIN
from smarthub.components.smarthub_green.const import DOMAIN
from smarthub.core import SmartHub
from smarthub.setup import async_setup_component

from tests.common import MockConfigEntry, MockModule, mock_integration
from tests.typing import WebSocketGenerator


async def test_hardware_info(
    hass: SmartHub, hass_ws_client: WebSocketGenerator
) -> None:
    """Test we can get the board info."""
    mock_integration(hass, MockModule("hassio"))
    await async_setup_component(hass, HASSIO_DOMAIN, {})

    # Setup the config entry
    config_entry = MockConfigEntry(
        data={},
        domain=DOMAIN,
        options={},
        title="SmartHub Green",
    )
    config_entry.add_to_hass(hass)
    with patch(
        "smarthub.components.smarthub_green.get_os_info",
        return_value={"board": "green"},
    ):
        assert await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()

    client = await hass_ws_client(hass)

    with patch(
        "smarthub.components.smarthub_green.hardware.get_os_info",
        return_value={"board": "green"},
    ):
        await client.send_json({"id": 1, "type": "hardware/info"})
        msg = await client.receive_json()

    assert msg["id"] == 1
    assert msg["success"]
    assert msg["result"] == {
        "hardware": [
            {
                "board": {
                    "hassio_board_id": "green",
                    "manufacturer": "smarthub",
                    "model": "green",
                    "revision": None,
                },
                "config_entries": [config_entry.entry_id],
                "dongle": None,
                "name": "SmartHub Green",
                "url": "https://support.nabucasa.com/hc/en-us/categories/24638797677853-Home-Assistant-Green",
            }
        ]
    }


@pytest.mark.parametrize("os_info", [None, {"board": None}, {"board": "other"}])
async def test_hardware_info_fail(
    hass: SmartHub, hass_ws_client: WebSocketGenerator, os_info
) -> None:
    """Test async_info raises if os_info is not as expected."""
    mock_integration(hass, MockModule("hassio"))
    await async_setup_component(hass, HASSIO_DOMAIN, {})

    # Setup the config entry
    config_entry = MockConfigEntry(
        data={},
        domain=DOMAIN,
        options={},
        title="SmartHub Green",
    )
    config_entry.add_to_hass(hass)
    with patch(
        "smarthub.components.smarthub_green.get_os_info",
        return_value={"board": "green"},
    ):
        assert await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()

    client = await hass_ws_client(hass)

    with patch(
        "smarthub.components.smarthub_green.hardware.get_os_info",
        return_value=os_info,
    ):
        await client.send_json({"id": 1, "type": "hardware/info"})
        msg = await client.receive_json()

    assert msg["id"] == 1
    assert msg["success"]
    assert msg["result"] == {"hardware": []}
