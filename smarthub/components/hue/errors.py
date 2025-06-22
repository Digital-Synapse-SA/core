"""Errors for the Hue component."""

from smarthub.exceptions import SmartHubError


class HueException(SmartHubError):
    """Base class for Hue exceptions."""


class CannotConnect(HueException):
    """Unable to connect to the bridge."""


class AuthenticationRequired(HueException):
    """Unknown error occurred."""
