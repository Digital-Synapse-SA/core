"""Test the SmartHub analytics init module."""

from __future__ import annotations

from unittest.mock import AsyncMock

from smarthub.components.analytics_insights.const import DOMAIN
from smarthub.config_entries import ConfigEntryState
from smarthub.core import SmartHub

from . import setup_integration

from tests.common import MockConfigEntry


async def test_load_unload_entry(
    hass: SmartHub,
    mock_analytics_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test load and unload entry."""
    await setup_integration(hass, mock_config_entry)
    entry = hass.config_entries.async_entries(DOMAIN)[0]

    assert entry.state is ConfigEntryState.LOADED

    await hass.config_entries.async_remove(entry.entry_id)
    await hass.async_block_till_done()

    assert entry.state is ConfigEntryState.NOT_LOADED
