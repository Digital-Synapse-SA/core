"""Errors for the HLK-SW16 component."""

from smarthub.exceptions import SmartHubError


class SW16Exception(SmartHubError):
    """Base class for HLK-SW16 exceptions."""


class CannotConnect(SW16Exception):
    """Unable to connect to the HLK-SW16."""
