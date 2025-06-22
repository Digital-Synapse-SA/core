"""The tests for the recorder helpers."""

from unittest.mock import patch

from smarthub.core import SmartHub
from smarthub.helpers import recorder

from tests.typing import RecorderInstanceGenerator


async def test_async_migration_in_progress(
    async_setup_recorder_instance: RecorderInstanceGenerator, hass: SmartHub
) -> None:
    """Test async_migration_in_progress wraps the recorder."""
    with patch(
        "smarthub.components.recorder.util.async_migration_in_progress",
        return_value=False,
    ):
        assert recorder.async_migration_in_progress(hass) is False

    with patch(
        "smarthub.components.recorder.util.async_migration_in_progress",
        return_value=True,
    ):
        assert recorder.async_migration_in_progress(hass) is True


async def test_async_migration_is_live(
    async_setup_recorder_instance: RecorderInstanceGenerator, hass: SmartHub
) -> None:
    """Test async_migration_in_progress wraps the recorder."""
    with patch(
        "smarthub.components.recorder.util.async_migration_is_live",
        return_value=False,
    ):
        assert recorder.async_migration_is_live(hass) is False

    with patch(
        "smarthub.components.recorder.util.async_migration_is_live",
        return_value=True,
    ):
        assert recorder.async_migration_is_live(hass) is True
