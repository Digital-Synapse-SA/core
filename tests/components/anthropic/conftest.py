"""Tests helpers."""

from collections.abc import AsyncGenerator
from unittest.mock import patch

import pytest

from smarthub.components.anthropic import CONF_CHAT_MODEL
from smarthub.const import CONF_LLM_HASS_API
from smarthub.core import SmartHub
from smarthub.helpers import llm
from smarthub.setup import async_setup_component

from tests.common import MockConfigEntry


@pytest.fixture
def mock_config_entry(hass: SmartHub) -> MockConfigEntry:
    """Mock a config entry."""
    entry = MockConfigEntry(
        title="Claude",
        domain="anthropic",
        data={
            "api_key": "bla",
        },
    )
    entry.add_to_hass(hass)
    return entry


@pytest.fixture
def mock_config_entry_with_assist(
    hass: SmartHub, mock_config_entry: MockConfigEntry
) -> MockConfigEntry:
    """Mock a config entry with assist."""
    hass.config_entries.async_update_entry(
        mock_config_entry, options={CONF_LLM_HASS_API: llm.LLM_API_ASSIST}
    )
    return mock_config_entry


@pytest.fixture
def mock_config_entry_with_extended_thinking(
    hass: SmartHub, mock_config_entry: MockConfigEntry
) -> MockConfigEntry:
    """Mock a config entry with assist."""
    hass.config_entries.async_update_entry(
        mock_config_entry,
        options={
            CONF_LLM_HASS_API: llm.LLM_API_ASSIST,
            CONF_CHAT_MODEL: "claude-3-7-sonnet-latest",
        },
    )
    return mock_config_entry


@pytest.fixture
async def mock_init_component(
    hass: SmartHub, mock_config_entry: MockConfigEntry
) -> AsyncGenerator[None]:
    """Initialize integration."""
    with patch("anthropic.resources.models.AsyncModels.retrieve"):
        assert await async_setup_component(hass, "anthropic", {})
        await hass.async_block_till_done()
        yield


@pytest.fixture(autouse=True)
async def setup_ha(hass: SmartHub) -> None:
    """Set up SmartHub."""
    assert await async_setup_component(hass, "smarthub", {})
