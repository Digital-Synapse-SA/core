"""Sonos specific exceptions."""

from smarthub.components.media_player import BrowseError
from smarthub.exceptions import SmartHubError


class UnknownMediaType(BrowseError):
    """Unknown media type."""


class SonosSubscriptionsFailed(SmartHubError):
    """Subscription creation failed."""


class SonosUpdateError(SmartHubError):
    """Update failed."""


class S1BatteryMissing(SonosUpdateError):
    """Battery update failed on S1 firmware."""
