"""Exceptions raised by IMAP integration."""

from smarthub.exceptions import SmartHubError


class InvalidAuth(SmartHubError):
    """Raise exception for invalid credentials."""


class InvalidFolder(SmartHubError):
    """Raise exception for invalid folder."""
