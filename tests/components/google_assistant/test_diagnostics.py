"""Test diagnostics."""

from unittest.mock import patch

import pytest
from syrupy.assertion import SnapshotAssertion
from syrupy.filters import props

from smarthub import setup
from smarthub.components import google_assistant as ga, switch
from smarthub.const import Platform
from smarthub.core import SmartHub
from smarthub.setup import async_setup_component

from .test_http import DUMMY_CONFIG

from tests.components.diagnostics import get_diagnostics_for_config_entry
from tests.typing import ClientSessionGenerator


@pytest.fixture(autouse=True)
async def switch_only() -> None:
    """Enable only the switch platform."""
    with patch(
        "smarthub.components.demo.COMPONENTS_WITH_CONFIG_ENTRY_DEMO_PLATFORM",
        [Platform.SWITCH],
    ):
        yield


async def test_diagnostics(
    hass: SmartHub,
    hass_client: ClientSessionGenerator,
    snapshot: SnapshotAssertion,
) -> None:
    """Test diagnostics v1."""

    await async_setup_component(hass, "smarthub", {})
    await setup.async_setup_component(
        hass, switch.DOMAIN, {"switch": [{"platform": "demo"}]}
    )

    await async_setup_component(
        hass,
        ga.DOMAIN,
        {"google_assistant": DUMMY_CONFIG},
    )
    await hass.async_block_till_done()

    config_entry = hass.config_entries.async_entries("google_assistant")[0]
    assert await get_diagnostics_for_config_entry(
        hass, hass_client, config_entry
    ) == snapshot(exclude=props("entry_id", "created_at", "modified_at"))
