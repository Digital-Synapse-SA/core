"""Various utilities for the Bang & Olufsen integration."""

from __future__ import annotations

from smarthub.core import SmartHub
from smarthub.helpers import device_registry as dr
from smarthub.helpers.device_registry import DeviceEntry

from .const import DOMAIN


def get_device(hass: SmartHub, unique_id: str) -> DeviceEntry:
    """Get the device."""
    device_registry = dr.async_get(hass)
    device = device_registry.async_get_device({(DOMAIN, unique_id)})
    assert device

    return device


def get_serial_number_from_jid(jid: str) -> str:
    """Get serial number from Beolink JID."""
    return jid.split(".")[2].split("@")[0]
