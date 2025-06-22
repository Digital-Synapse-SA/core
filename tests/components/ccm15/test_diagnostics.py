"""Test CCM15 diagnostics."""

import pytest
from syrupy.assertion import SnapshotAssertion

from smarthub.components.ccm15.const import DOMAIN
from smarthub.const import CONF_HOST, CONF_PORT
from smarthub.core import SmartHub

from tests.common import MockConfigEntry
from tests.components.diagnostics import get_diagnostics_for_config_entry
from tests.typing import ClientSessionGenerator


@pytest.mark.usefixtures("ccm15_device")
async def test_entry_diagnostics(
    hass: SmartHub,
    hass_client: ClientSessionGenerator,
    snapshot: SnapshotAssertion,
) -> None:
    """Test config entry diagnostics."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id="1.1.1.1",
        data={
            CONF_HOST: "1.1.1.1",
            CONF_PORT: 80,
        },
    )
    entry.add_to_hass(hass)

    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    result = await get_diagnostics_for_config_entry(hass, hass_client, entry)

    assert result == snapshot
