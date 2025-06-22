"""Test the Reolink camera platform."""

from unittest.mock import MagicMock, patch

import pytest
from reolink_aio.exceptions import ReolinkError

from smarthub.components.camera import (
    CameraState,
    async_get_image,
    async_get_stream_source,
)
from smarthub.config_entries import ConfigEntryState
from smarthub.const import Platform
from smarthub.core import SmartHub
from smarthub.exceptions import SmartHubError

from .conftest import TEST_DUO_MODEL, TEST_NVR_NAME

from tests.common import MockConfigEntry
from tests.typing import ClientSessionGenerator


async def test_camera(
    hass: SmartHub,
    hass_client_no_auth: ClientSessionGenerator,
    config_entry: MockConfigEntry,
    reolink_host: MagicMock,
) -> None:
    """Test camera entity with fluent."""
    with patch("smarthub.components.reolink.PLATFORMS", [Platform.CAMERA]):
        assert await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()
    assert config_entry.state is ConfigEntryState.LOADED

    entity_id = f"{Platform.CAMERA}.{TEST_NVR_NAME}_fluent"
    assert hass.states.get(entity_id).state == CameraState.IDLE

    # check getting a image from the camera
    reolink_host.get_snapshot.return_value = b"image"
    assert (await async_get_image(hass, entity_id)).content == b"image"

    reolink_host.get_snapshot.side_effect = ReolinkError("Test error")
    with pytest.raises(SmartHubError):
        await async_get_image(hass, entity_id)

    # check getting the stream source
    assert await async_get_stream_source(hass, entity_id) is not None


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_camera_no_stream_source(
    hass: SmartHub,
    config_entry: MockConfigEntry,
    reolink_host: MagicMock,
) -> None:
    """Test camera entity with no stream source."""
    reolink_host.model = TEST_DUO_MODEL
    reolink_host.get_stream_source.return_value = None

    with patch("smarthub.components.reolink.PLATFORMS", [Platform.CAMERA]):
        assert await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()
    assert config_entry.state is ConfigEntryState.LOADED

    entity_id = f"{Platform.CAMERA}.{TEST_NVR_NAME}_snapshots_fluent_lens_0"
    assert hass.states.get(entity_id).state == CameraState.IDLE
