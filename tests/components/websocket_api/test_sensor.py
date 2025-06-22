"""Test cases for the API stream sensor."""

from smarthub.auth.providers.smarthub import HassAuthProvider
from smarthub.components.websocket_api.auth import TYPE_AUTH_REQUIRED
from smarthub.components.websocket_api.http import URL
from smarthub.core import SmartHub
from smarthub.setup import async_setup_component

from .test_auth import test_auth_active_with_token

from tests.typing import ClientSessionGenerator


async def test_websocket_api(
    hass: SmartHub,
    hass_client_no_auth: ClientSessionGenerator,
    hass_access_token: str,
    local_auth: HassAuthProvider,
) -> None:
    """Test API streams."""
    await async_setup_component(
        hass, "sensor", {"sensor": {"platform": "websocket_api"}}
    )
    await hass.async_block_till_done()

    client = await hass_client_no_auth()
    ws = await client.ws_connect(URL)

    auth_ok = await ws.receive_json()

    assert auth_ok["type"] == TYPE_AUTH_REQUIRED

    ws.client = client

    state = hass.states.get("sensor.connected_clients")
    assert state.state == "0"

    await test_auth_active_with_token(hass, ws, hass_access_token)

    state = hass.states.get("sensor.connected_clients")
    assert state.state == "1"

    await ws.close()
    await hass.async_block_till_done()

    state = hass.states.get("sensor.connected_clients")
    assert state.state == "0"
