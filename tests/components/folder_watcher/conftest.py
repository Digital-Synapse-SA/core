"""Fixtures for Folder Watcher integration tests."""

from __future__ import annotations

from collections.abc import Generator
from pathlib import Path
from unittest.mock import patch

from freezegun.api import FrozenDateTimeFactory
import pytest

from smarthub.components.folder_watcher.const import DOMAIN
from smarthub.config_entries import SOURCE_USER
from smarthub.core import SmartHub

from tests.common import MockConfigEntry


@pytest.fixture
def mock_setup_entry() -> Generator[None]:
    """Mock setting up a config entry."""
    with patch(
        "smarthub.components.folder_watcher.async_setup_entry", return_value=True
    ):
        yield


@pytest.fixture
async def load_int(
    hass: SmartHub, tmp_path: Path, freezer: FrozenDateTimeFactory
) -> MockConfigEntry:
    """Set up the Folder watcher integration in SmartHub."""
    freezer.move_to("2022-04-19 10:31:02+00:00")
    path = tmp_path.as_posix()
    hass.config.allowlist_external_dirs = {path}
    config_entry = MockConfigEntry(
        domain=DOMAIN,
        source=SOURCE_USER,
        title=f"Folder Watcher {tmp_path.parts[-1]!s}",
        data={},
        options={"folder": str(path), "patterns": ["*"]},
        entry_id="1",
    )

    config_entry.add_to_hass(hass)

    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    return config_entry
