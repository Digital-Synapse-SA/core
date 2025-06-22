"""Helper to test significant NEW_NAME state changes."""

from __future__ import annotations

from typing import Any

from smarthub.const import ATTR_DEVICE_CLASS
from smarthub.core import SmartHub, callback


@callback
def async_check_significant_change(
    hass: SmartHub,
    old_state: str,
    old_attrs: dict,
    new_state: str,
    new_attrs: dict,
    **kwargs: Any,
) -> bool | None:
    """Test if state significantly changed."""
    device_class = new_attrs.get(ATTR_DEVICE_CLASS)

    if device_class is None:
        return None

    return None
