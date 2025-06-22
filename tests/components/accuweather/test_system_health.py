"""Test AccuWeather system health."""

import asyncio
from unittest.mock import AsyncMock

from aiohttp import ClientError

from smarthub.components.accuweather.const import DOMAIN
from smarthub.core import SmartHub
from smarthub.setup import async_setup_component

from . import init_integration

from tests.common import get_system_health_info
from tests.test_util.aiohttp import AiohttpClientMocker


async def test_accuweather_system_health(
    hass: SmartHub,
    aioclient_mock: AiohttpClientMocker,
    mock_accuweather_client: AsyncMock,
) -> None:
    """Test AccuWeather system health."""
    aioclient_mock.get("https://dataservice.accuweather.com/", text="")

    await init_integration(hass)
    assert await async_setup_component(hass, "system_health", {})
    await hass.async_block_till_done()

    info = await get_system_health_info(hass, DOMAIN)

    for key, val in info.items():
        if asyncio.iscoroutine(val):
            info[key] = await val

    assert info == {
        "can_reach_server": "ok",
        "remaining_requests": 10,
    }


async def test_accuweather_system_health_fail(
    hass: SmartHub,
    aioclient_mock: AiohttpClientMocker,
    mock_accuweather_client: AsyncMock,
) -> None:
    """Test AccuWeather system health."""
    aioclient_mock.get("https://dataservice.accuweather.com/", exc=ClientError)

    await init_integration(hass)
    assert await async_setup_component(hass, "system_health", {})
    await hass.async_block_till_done()

    info = await get_system_health_info(hass, DOMAIN)

    for key, val in info.items():
        if asyncio.iscoroutine(val):
            info[key] = await val

    assert info == {
        "can_reach_server": {"type": "failed", "error": "unreachable"},
        "remaining_requests": 10,
    }
