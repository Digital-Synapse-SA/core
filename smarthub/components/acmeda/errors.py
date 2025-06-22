"""Errors for the Acmeda Pulse component."""

from smarthub.exceptions import SmartHubError


class PulseException(SmartHubError):
    """Base class for Acmeda Pulse exceptions."""


class CannotConnect(PulseException):
    """Unable to connect to the bridge."""
