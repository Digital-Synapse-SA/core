"""The Raspberry Pi hardware platform."""

from __future__ import annotations

from smarthub.components.hardware.models import BoardInfo, HardwareInfo
from smarthub.components.hassio import get_os_info
from smarthub.core import SmartHub, callback
from smarthub.exceptions import SmartHubError

from .const import DOMAIN

BOARD_NAMES = {
    "rpi": "Raspberry Pi",
    "rpi0": "Raspberry Pi Zero",
    "rpi0-w": "Raspberry Pi Zero W",
    "rpi2": "Raspberry Pi 2",
    "rpi3": "Raspberry Pi 3 (32-bit)",
    "rpi3-64": "Raspberry Pi 3",
    "rpi4": "Raspberry Pi 4 (32-bit)",
    "rpi4-64": "Raspberry Pi 4",
    "rpi5-64": "Raspberry Pi 5",
}

MODELS = {
    "rpi": "1",
    "rpi0": "zero",
    "rpi0-w": "zero_w",
    "rpi2": "2",
    "rpi3": "3",
    "rpi3-64": "3",
    "rpi4": "4",
    "rpi4-64": "4",
    "rpi5-64": "5",
}


@callback
def async_info(hass: SmartHub) -> list[HardwareInfo]:
    """Return board info."""
    if (os_info := get_os_info(hass)) is None:
        raise SmartHubError
    board: str | None
    if (board := os_info.get("board")) is None:
        raise SmartHubError
    if not board.startswith("rpi"):
        raise SmartHubError

    config_entries = [
        entry.entry_id for entry in hass.config_entries.async_entries(DOMAIN)
    ]

    return [
        HardwareInfo(
            board=BoardInfo(
                hassio_board_id=board,
                manufacturer=DOMAIN,
                model=MODELS.get(board),
                revision=None,
            ),
            config_entries=config_entries,
            dongle=None,
            name=BOARD_NAMES.get(board, f"Unknown Raspberry Pi model '{board}'"),
            url=None,
        )
    ]
