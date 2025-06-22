"""The tests for Media Extractor integration."""

import os
import os.path
from typing import Any
from unittest.mock import patch

import pytest
from syrupy.assertion import SnapshotAssertion
from yt_dlp import DownloadError

from smarthub.components.media_extractor.const import (
    ATTR_URL,
    DOMAIN,
    SERVICE_EXTRACT_MEDIA_URL,
)
from smarthub.components.media_player import SERVICE_PLAY_MEDIA
from smarthub.core import SmartHub, ServiceCall
from smarthub.exceptions import SmartHubError
from smarthub.setup import async_setup_component

from . import YOUTUBE_EMPTY_PLAYLIST, YOUTUBE_PLAYLIST, YOUTUBE_VIDEO, MockYoutubeDL
from .const import NO_FORMATS_RESPONSE, SOUNDCLOUD_TRACK

from tests.common import MockConfigEntry, async_load_json_object_fixture


async def test_play_media_service_is_registered(hass: SmartHub) -> None:
    """Test play media service is registered."""
    mock_config_entry = MockConfigEntry(domain=DOMAIN)

    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    assert hass.services.has_service(DOMAIN, SERVICE_PLAY_MEDIA)
    assert hass.services.has_service(DOMAIN, SERVICE_EXTRACT_MEDIA_URL)
    assert len(hass.config_entries.async_entries(DOMAIN))


@pytest.mark.parametrize(
    "url",
    [
        YOUTUBE_VIDEO,
        SOUNDCLOUD_TRACK,
        NO_FORMATS_RESPONSE,
        YOUTUBE_PLAYLIST,
    ],
)
async def test_extract_media_service(
    hass: SmartHub,
    mock_youtube_dl: MockYoutubeDL,
    snapshot: SnapshotAssertion,
    empty_media_extractor_config: dict[str, Any],
    url: str,
) -> None:
    """Test play media service is registered."""
    await async_setup_component(hass, DOMAIN, empty_media_extractor_config)
    await hass.async_block_till_done()

    assert (
        await hass.services.async_call(
            DOMAIN,
            SERVICE_EXTRACT_MEDIA_URL,
            {ATTR_URL: url},
            blocking=True,
            return_response=True,
        )
        == snapshot
    )


async def test_extracting_playlist_no_entries(
    hass: SmartHub,
    mock_youtube_dl: MockYoutubeDL,
    empty_media_extractor_config: dict[str, Any],
) -> None:
    """Test extracting a playlist without entries."""

    await async_setup_component(hass, DOMAIN, empty_media_extractor_config)
    await hass.async_block_till_done()
    with pytest.raises(SmartHubError):
        await hass.services.async_call(
            DOMAIN,
            SERVICE_EXTRACT_MEDIA_URL,
            {ATTR_URL: YOUTUBE_EMPTY_PLAYLIST},
            blocking=True,
            return_response=True,
        )


@pytest.mark.parametrize(
    "config_fixture", ["empty_media_extractor_config", "audio_media_extractor_config"]
)
@pytest.mark.parametrize(
    ("media_content_id", "media_content_type"),
    [
        (YOUTUBE_VIDEO, "VIDEO"),
        (SOUNDCLOUD_TRACK, "AUDIO"),
        (NO_FORMATS_RESPONSE, "AUDIO"),
    ],
)
async def test_play_media_service(
    hass: SmartHub,
    mock_youtube_dl: MockYoutubeDL,
    service_calls: list[ServiceCall],
    snapshot: SnapshotAssertion,
    request: pytest.FixtureRequest,
    config_fixture: str,
    media_content_id: str,
    media_content_type: str,
) -> None:
    """Test play media service is registered."""
    config: dict[str, Any] = request.getfixturevalue(config_fixture)
    await async_setup_component(hass, DOMAIN, config)
    await hass.async_block_till_done()

    await hass.services.async_call(
        DOMAIN,
        SERVICE_PLAY_MEDIA,
        {
            "entity_id": "media_player.bedroom",
            "media_content_type": media_content_type,
            "media_content_id": media_content_id,
        },
    )
    await hass.async_block_till_done()

    assert len(service_calls) == 2
    assert service_calls[1].data == snapshot


async def test_download_error(
    hass: SmartHub,
    empty_media_extractor_config: dict[str, Any],
    service_calls: list[ServiceCall],
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test handling DownloadError."""

    with patch(
        "smarthub.components.media_extractor.YoutubeDL.extract_info",
        side_effect=DownloadError("Message"),
    ):
        await async_setup_component(hass, DOMAIN, empty_media_extractor_config)
        await hass.async_block_till_done()

        await hass.services.async_call(
            DOMAIN,
            SERVICE_PLAY_MEDIA,
            {
                "entity_id": "media_player.bedroom",
                "media_content_type": "VIDEO",
                "media_content_id": YOUTUBE_VIDEO,
            },
        )
        await hass.async_block_till_done()

    assert len(service_calls) == 1
    assert f"Could not retrieve data for the URL: {YOUTUBE_VIDEO}" in caplog.text


async def test_no_target_entity(
    hass: SmartHub,
    mock_youtube_dl: MockYoutubeDL,
    empty_media_extractor_config: dict[str, Any],
    service_calls: list[ServiceCall],
    snapshot: SnapshotAssertion,
) -> None:
    """Test having no target entity."""

    await async_setup_component(hass, DOMAIN, empty_media_extractor_config)
    await hass.async_block_till_done()

    await hass.services.async_call(
        DOMAIN,
        SERVICE_PLAY_MEDIA,
        {
            "device_id": "fb034c3a9fefe47c584c32a6b51817eb",
            "media_content_type": "VIDEO",
            "media_content_id": YOUTUBE_VIDEO,
        },
    )
    await hass.async_block_till_done()

    assert len(service_calls) == 2
    assert service_calls[1].data == snapshot


async def test_playlist(
    hass: SmartHub,
    mock_youtube_dl: MockYoutubeDL,
    empty_media_extractor_config: dict[str, Any],
    service_calls: list[ServiceCall],
    snapshot: SnapshotAssertion,
) -> None:
    """Test extracting a playlist."""

    await async_setup_component(hass, DOMAIN, empty_media_extractor_config)
    await hass.async_block_till_done()

    await hass.services.async_call(
        DOMAIN,
        SERVICE_PLAY_MEDIA,
        {
            "entity_id": "media_player.bedroom",
            "media_content_type": "VIDEO",
            "media_content_id": YOUTUBE_PLAYLIST,
        },
    )
    await hass.async_block_till_done()

    assert len(service_calls) == 2
    assert service_calls[1].data == snapshot


async def test_playlist_no_entries(
    hass: SmartHub,
    mock_youtube_dl: MockYoutubeDL,
    empty_media_extractor_config: dict[str, Any],
    service_calls: list[ServiceCall],
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test extracting a playlist without entries."""

    await async_setup_component(hass, DOMAIN, empty_media_extractor_config)
    await hass.async_block_till_done()

    await hass.services.async_call(
        DOMAIN,
        SERVICE_PLAY_MEDIA,
        {
            "entity_id": "media_player.bedroom",
            "media_content_type": "VIDEO",
            "media_content_id": YOUTUBE_EMPTY_PLAYLIST,
        },
    )
    await hass.async_block_till_done()

    assert len(service_calls) == 1
    assert (
        f"Could not retrieve data for the URL: {YOUTUBE_EMPTY_PLAYLIST}" in caplog.text
    )


async def test_query_error(
    hass: SmartHub,
    empty_media_extractor_config: dict[str, Any],
    service_calls: list[ServiceCall],
) -> None:
    """Test handling error with query."""

    with (
        patch(
            "smarthub.components.media_extractor.YoutubeDL.extract_info",
            return_value=await async_load_json_object_fixture(
                hass, "youtube_1_info.json", DOMAIN
            ),
        ),
        patch(
            "smarthub.components.media_extractor.YoutubeDL.process_ie_result",
            side_effect=DownloadError("Message"),
        ),
    ):
        await async_setup_component(hass, DOMAIN, empty_media_extractor_config)
        await hass.async_block_till_done()

        await hass.services.async_call(
            DOMAIN,
            SERVICE_PLAY_MEDIA,
            {
                "entity_id": "media_player.bedroom",
                "media_content_type": "VIDEO",
                "media_content_id": YOUTUBE_VIDEO,
            },
        )
        await hass.async_block_till_done()

    assert len(service_calls) == 1


async def test_cookiefile_detection(
    hass: SmartHub,
    mock_youtube_dl: MockYoutubeDL,
    empty_media_extractor_config: dict[str, Any],
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test cookie file detection."""

    await async_setup_component(hass, DOMAIN, empty_media_extractor_config)
    await hass.async_block_till_done()

    cookies_dir = os.path.join(hass.config.config_dir, "media_extractor")
    cookies_file = os.path.join(cookies_dir, "cookies.txt")

    def _write_cookies_file() -> None:
        if not os.path.exists(cookies_dir):
            os.makedirs(cookies_dir)

        with open(cookies_file, "w+", encoding="utf-8") as f:
            f.write(
                """# Netscape HTTP Cookie File

                .youtube.com TRUE / TRUE 1701708706 GPS 1
                """
            )

    await hass.async_add_executor_job(_write_cookies_file)

    await hass.services.async_call(
        DOMAIN,
        SERVICE_PLAY_MEDIA,
        {
            "entity_id": "media_player.bedroom",
            "media_content_type": "VIDEO",
            "media_content_id": YOUTUBE_PLAYLIST,
        },
    )
    await hass.async_block_till_done()

    assert "Media extractor loaded cookies file" in caplog.text

    await hass.async_add_executor_job(os.remove, cookies_file)

    await hass.services.async_call(
        DOMAIN,
        SERVICE_PLAY_MEDIA,
        {
            "entity_id": "media_player.bedroom",
            "media_content_type": "VIDEO",
            "media_content_id": YOUTUBE_PLAYLIST,
        },
    )
    await hass.async_block_till_done()

    assert "Media extractor didn't find cookies file" in caplog.text
