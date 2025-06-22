"""The errors of Epson integration."""

from smarthub import exceptions


class CannotConnect(exceptions.SmartHubError):
    """Error to indicate we cannot connect."""


class PoweredOff(exceptions.SmartHubError):
    """Error to indicate projector is off."""
