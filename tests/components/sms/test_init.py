"""Test init."""

from unittest.mock import Mock, patch

from smarthub.config_entries import ConfigEntryState
from smarthub.const import CONF_DEVICE
from smarthub.core import DOMAIN as HOMEASSISTANT_DOMAIN, SmartHub
from smarthub.helpers import issue_registry as ir

from tests.common import MockConfigEntry


@patch.dict(
    "sys.modules",
    {
        "gammu": Mock(),
        "gammu.asyncworker": Mock(),
    },
)
async def test_repair_issue_is_created(
    hass: SmartHub,
    issue_registry: ir.IssueRegistry,
) -> None:
    """Test repair issue is created."""
    from smarthub.components.sms import (  # noqa: PLC0415
        DEPRECATED_ISSUE_ID,
        DOMAIN,
    )

    with (
        patch("smarthub.components.sms.create_sms_gateway", autospec=True),
        patch("smarthub.components.sms.PLATFORMS", []),
    ):
        config_entry = MockConfigEntry(
            title="test",
            domain=DOMAIN,
            data={
                CONF_DEVICE: "/dev/ttyUSB0",
            },
        )

        config_entry.add_to_hass(hass)
        await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()

        assert config_entry.state is ConfigEntryState.LOADED
        assert (
            HOMEASSISTANT_DOMAIN,
            DEPRECATED_ISSUE_ID,
        ) in issue_registry.issues

        await hass.config_entries.async_unload(config_entry.entry_id)
        await hass.async_block_till_done()

        assert config_entry.state is ConfigEntryState.NOT_LOADED
        assert (
            HOMEASSISTANT_DOMAIN,
            DEPRECATED_ISSUE_ID,
        ) not in issue_registry.issues
