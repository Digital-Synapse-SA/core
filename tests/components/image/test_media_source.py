"""Test image media source."""

import pytest

from smarthub.components import media_source
from smarthub.core import SmartHub
from smarthub.setup import async_setup_component


@pytest.fixture(autouse=True)
async def setup_media_source(hass: SmartHub) -> None:
    """Set up media source."""
    assert await async_setup_component(hass, "media_source", {})


async def test_browsing(hass: SmartHub, mock_image_platform) -> None:
    """Test browsing image media source."""
    item = await media_source.async_browse_media(hass, "media-source://image")
    assert item is not None
    assert item.title == "Image"
    assert len(item.children) == 1
    assert item.children[0].media_content_type == "image/jpeg"


async def test_resolving(hass: SmartHub, mock_image_platform) -> None:
    """Test resolving."""
    item = await media_source.async_resolve_media(
        hass, "media-source://image/image.test", None
    )
    assert item is not None
    assert item.url == "/api/image_proxy_stream/image.test"
    assert item.mime_type == "image/jpeg"


async def test_resolving_non_existing_camera(
    hass: SmartHub, mock_image_platform
) -> None:
    """Test resolving."""
    with pytest.raises(
        media_source.Unresolvable,
        match="Could not resolve media item: image.non_existing",
    ):
        await media_source.async_resolve_media(
            hass, "media-source://image/image.non_existing", None
        )
