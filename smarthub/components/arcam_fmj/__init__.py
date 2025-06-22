"""Arcam component."""

import asyncio
from asyncio import timeout
import logging
from typing import Any

from arcam.fmj import ConnectionFailed
from arcam.fmj.client import Client

from smarthub.config_entries import ConfigEntry
from smarthub.const import CONF_HOST, CONF_PORT, Platform
from smarthub.core import SmartHub
from smarthub.helpers.dispatcher import async_dispatcher_send

from .const import (
    DEFAULT_SCAN_INTERVAL,
    SIGNAL_CLIENT_DATA,
    SIGNAL_CLIENT_STARTED,
    SIGNAL_CLIENT_STOPPED,
)

type ArcamFmjConfigEntry = ConfigEntry[Client]

_LOGGER = logging.getLogger(__name__)


PLATFORMS = [Platform.MEDIA_PLAYER]


async def async_setup_entry(hass: SmartHub, entry: ArcamFmjConfigEntry) -> bool:
    """Set up config entry."""
    entry.runtime_data = Client(entry.data[CONF_HOST], entry.data[CONF_PORT])

    entry.async_create_background_task(
        hass, _run_client(hass, entry.runtime_data, DEFAULT_SCAN_INTERVAL), "arcam_fmj"
    )

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: SmartHub, entry: ConfigEntry) -> bool:
    """Cleanup before removing config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def _run_client(hass: SmartHub, client: Client, interval: float) -> None:
    def _listen(_: Any) -> None:
        async_dispatcher_send(hass, SIGNAL_CLIENT_DATA, client.host)

    while True:
        try:
            async with timeout(interval):
                await client.start()

            _LOGGER.debug("Client connected %s", client.host)
            async_dispatcher_send(hass, SIGNAL_CLIENT_STARTED, client.host)

            try:
                with client.listen(_listen):
                    await client.process()
            finally:
                await client.stop()

                _LOGGER.debug("Client disconnected %s", client.host)
                async_dispatcher_send(hass, SIGNAL_CLIENT_STOPPED, client.host)

        except ConnectionFailed:
            await asyncio.sleep(interval)
        except TimeoutError:
            continue
        except Exception:
            _LOGGER.exception("Unexpected exception, aborting arcam client")
            return
