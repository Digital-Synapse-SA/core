"""The Local To-do integration."""

from __future__ import annotations

from pathlib import Path

from smarthub.config_entries import ConfigEntry
from smarthub.const import Platform
from smarthub.core import SmartHub
from smarthub.exceptions import ConfigEntryNotReady
from smarthub.util import slugify

from .const import CONF_STORAGE_KEY, CONF_TODO_LIST_NAME
from .store import LocalTodoListStore

PLATFORMS: list[Platform] = [Platform.TODO]

STORAGE_PATH = ".storage/local_todo.{key}.ics"

type LocalTodoConfigEntry = ConfigEntry[LocalTodoListStore]


async def async_setup_entry(hass: SmartHub, entry: LocalTodoConfigEntry) -> bool:
    """Set up Local To-do from a config entry."""
    path = Path(hass.config.path(STORAGE_PATH.format(key=entry.data[CONF_STORAGE_KEY])))
    store = LocalTodoListStore(hass, path)
    try:
        await store.async_load()
    except OSError as err:
        raise ConfigEntryNotReady("Failed to load file {path}: {err}") from err

    entry.runtime_data = store

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: SmartHub, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_remove_entry(hass: SmartHub, entry: ConfigEntry) -> None:
    """Handle removal of an entry."""
    key = slugify(entry.data[CONF_TODO_LIST_NAME])
    path = Path(hass.config.path(STORAGE_PATH.format(key=key)))

    def unlink(path: Path) -> None:
        path.unlink(missing_ok=True)

    await hass.async_add_executor_job(unlink, path)
