"""Dlib Face Identity Image Processing Tests."""

from unittest.mock import Mock, patch

from smarthub.components.dlib_face_detect import DOMAIN
from smarthub.components.image_processing import DOMAIN as IMAGE_PROCESSING_DOMAIN
from smarthub.const import CONF_ENTITY_ID, CONF_PLATFORM, CONF_SOURCE
from smarthub.core import DOMAIN as HOMEASSISTANT_DOMAIN, SmartHub
from smarthub.helpers import issue_registry as ir
from smarthub.setup import async_setup_component


@patch.dict("sys.modules", face_recognition=Mock())
async def test_repair_issue_is_created(
    hass: SmartHub,
    issue_registry: ir.IssueRegistry,
) -> None:
    """Test repair issue is created."""
    assert await async_setup_component(
        hass,
        IMAGE_PROCESSING_DOMAIN,
        {
            IMAGE_PROCESSING_DOMAIN: [
                {
                    CONF_PLATFORM: DOMAIN,
                    CONF_SOURCE: [
                        {CONF_ENTITY_ID: "camera.test_camera"},
                    ],
                }
            ],
        },
    )
    await hass.async_block_till_done()
    assert (
        HOMEASSISTANT_DOMAIN,
        f"deprecated_system_packages_yaml_integration_{DOMAIN}",
    ) in issue_registry.issues
