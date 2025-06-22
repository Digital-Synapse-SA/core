"""Fixtures for the Switch as X integration tests."""

from __future__ import annotations

from collections.abc import Generator
from unittest.mock import AsyncMock, patch

import pytest

from smarthub.core import SmartHub
from smarthub.setup import async_setup_component


@pytest.fixture(autouse=True)
async def setup_smarthub(hass: SmartHub):
    """Set up the smarthub integration."""
    await async_setup_component(hass, "smarthub", {})


@pytest.fixture
def mock_setup_entry() -> Generator[AsyncMock]:
    """Mock setting up a config entry."""
    with patch(
        "smarthub.components.switch_as_x.async_setup_entry", return_value=True
    ) as mock_setup:
        yield mock_setup
