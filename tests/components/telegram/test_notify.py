"""The tests for the telegram.notify platform."""

from unittest.mock import patch

from smarthub import config as hass_config
from smarthub.components import notify
from smarthub.components.telegram import DOMAIN
from smarthub.const import SERVICE_RELOAD
from smarthub.core import SmartHub
from smarthub.setup import async_setup_component

from tests.common import get_fixture_path


async def test_reload_notify(hass: SmartHub) -> None:
    """Verify we can reload the notify service."""

    with patch("smarthub.components.telegram_bot.async_setup", return_value=True):
        assert await async_setup_component(
            hass,
            notify.DOMAIN,
            {
                notify.DOMAIN: [
                    {
                        "name": DOMAIN,
                        "platform": DOMAIN,
                        "chat_id": 1,
                    },
                ]
            },
        )
        await hass.async_block_till_done()

    assert hass.services.has_service(notify.DOMAIN, DOMAIN)

    yaml_path = get_fixture_path("configuration.yaml", "telegram")
    with patch.object(hass_config, "YAML_CONFIG_FILE", yaml_path):
        await hass.services.async_call(
            DOMAIN,
            SERVICE_RELOAD,
            {},
            blocking=True,
        )
        await hass.async_block_till_done()

    assert not hass.services.has_service(notify.DOMAIN, DOMAIN)
    assert hass.services.has_service(notify.DOMAIN, "telegram_reloaded")
