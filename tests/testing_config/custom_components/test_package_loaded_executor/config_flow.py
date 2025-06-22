"""Config flow."""

from smarthub.core import SmartHub


async def _async_has_devices(hass: SmartHub) -> bool:
    return True
