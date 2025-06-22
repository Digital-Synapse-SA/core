"""Errors for media source."""

from smarthub.exceptions import SmartHubError


class MediaSourceError(SmartHubError):
    """Base class for media source errors."""


class Unresolvable(MediaSourceError):
    """When media ID is not resolvable."""


class UnknownMediaSource(MediaSourceError, ValueError):
    """When media source is unknown."""
