"""The tests for the KMtronic component."""

from smarthub.components.kmtronic.const import DOMAIN
from smarthub.config_entries import ConfigEntryState
from smarthub.core import SmartHub

from tests.common import MockConfigEntry
from tests.test_util.aiohttp import AiohttpClientMocker


async def test_unload_config_entry(
    hass: SmartHub, aioclient_mock: AiohttpClientMocker
) -> None:
    """Test entry unloading."""

    config_entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            "host": "1.1.1.1",
            "username": "admin",
            "password": "admin",
        },
    )
    config_entry.add_to_hass(hass)

    aioclient_mock.get(
        "http://1.1.1.1/status.xml",
        text="<response><relay0>0</relay0><relay1>0</relay1></response>",
    )
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    assert config_entry.state is ConfigEntryState.LOADED

    await hass.config_entries.async_unload(config_entry.entry_id)
    await hass.async_block_till_done()

    assert config_entry.state is ConfigEntryState.NOT_LOADED


async def test_config_entry_not_ready(
    hass: SmartHub, aioclient_mock: AiohttpClientMocker
) -> None:
    """Tests configuration entry not ready."""

    aioclient_mock.get(
        "http://1.1.1.1/status.xml",
        exc=TimeoutError(),
    )

    config_entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            "host": "1.1.1.1",
            "username": "foo",
            "password": "bar",
        },
    )
    config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    assert config_entry.state is ConfigEntryState.SETUP_RETRY
