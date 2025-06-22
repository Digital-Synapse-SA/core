"""Tests for the Gstreamer platform."""

from unittest.mock import Mock, patch

from smarthub.components.gstreamer import DOMAIN
from smarthub.components.media_player import DOMAIN as PLATFORM_DOMAIN
from smarthub.const import CONF_PLATFORM
from smarthub.core import DOMAIN as HOMEASSISTANT_DOMAIN, SmartHub
from smarthub.helpers import issue_registry as ir
from smarthub.setup import async_setup_component


@patch.dict("sys.modules", gsp=Mock())
async def test_repair_issue_is_created(
    hass: SmartHub,
    issue_registry: ir.IssueRegistry,
) -> None:
    """Test repair issue is created."""
    assert await async_setup_component(
        hass,
        PLATFORM_DOMAIN,
        {
            PLATFORM_DOMAIN: [
                {
                    CONF_PLATFORM: DOMAIN,
                }
            ],
        },
    )
    await hass.async_block_till_done()
    assert (
        HOMEASSISTANT_DOMAIN,
        f"deprecated_system_packages_yaml_integration_{DOMAIN}",
    ) in issue_registry.issues
