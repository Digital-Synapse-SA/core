"""Errors for the Mikrotik component."""

from smarthub.exceptions import SmartHubError


class CannotConnect(SmartHubError):
    """Unable to connect to the hub."""


class LoginError(SmartHubError):
    """Component got logged out."""
