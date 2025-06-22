"""Errors for the Media Player component."""

from smarthub.exceptions import SmartHubError


class MediaPlayerException(SmartHubError):
    """Base class for Media Player exceptions."""


class BrowseError(MediaPlayerException):
    """Error while browsing."""


class SearchError(MediaPlayerException):
    """Error while searching."""
