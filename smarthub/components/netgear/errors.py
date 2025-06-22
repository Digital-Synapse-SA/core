"""Errors for the Netgear component."""

from smarthub.exceptions import SmartHubError


class NetgearException(SmartHubError):
    """Base class for Netgear exceptions."""


class CannotLoginException(NetgearException):
    """Unable to login to the router."""
