"""Support for Qwikswitch relays."""

from __future__ import annotations

from smarthub.components.switch import SwitchEntity
from smarthub.core import SmartHub
from smarthub.helpers.entity_platform import AddEntitiesCallback
from smarthub.helpers.typing import ConfigType, DiscoveryInfoType

from . import DOMAIN
from .entity import QSToggleEntity


async def async_setup_platform(
    hass: SmartHub,
    _: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Add switches from the main Qwikswitch component."""
    if discovery_info is None:
        return

    qsusb = hass.data[DOMAIN]
    devs = [QSSwitch(qsid, qsusb) for qsid in discovery_info[DOMAIN]]
    add_entities(devs)


class QSSwitch(QSToggleEntity, SwitchEntity):
    """Switch based on a Qwikswitch relay module."""
