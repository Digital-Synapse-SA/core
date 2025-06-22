"""The SmartHub Green hardware platform."""

from __future__ import annotations

from smarthub.components.hardware.models import BoardInfo, HardwareInfo
from smarthub.components.hassio import get_os_info
from smarthub.core import SmartHub, callback
from smarthub.exceptions import SmartHubError

from .const import DOMAIN

BOARD_NAME = "SmartHub Green"
DOCUMENTATION_URL = "https://support.nabucasa.com/hc/en-us/categories/24638797677853-Home-Assistant-Green"
MANUFACTURER = "smarthub"
MODEL = "green"


@callback
def async_info(hass: SmartHub) -> list[HardwareInfo]:
    """Return board info."""
    if (os_info := get_os_info(hass)) is None:
        raise SmartHubError
    board: str | None
    if (board := os_info.get("board")) is None:
        raise SmartHubError
    if not board == "green":
        raise SmartHubError

    config_entries = [
        entry.entry_id for entry in hass.config_entries.async_entries(DOMAIN)
    ]

    return [
        HardwareInfo(
            board=BoardInfo(
                hassio_board_id=board,
                manufacturer=MANUFACTURER,
                model=MODEL,
                revision=None,
            ),
            config_entries=config_entries,
            dongle=None,
            name=BOARD_NAME,
            url=DOCUMENTATION_URL,
        )
    ]
