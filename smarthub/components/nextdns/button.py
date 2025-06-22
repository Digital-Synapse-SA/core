"""Support for the NextDNS service."""

from __future__ import annotations

from aiohttp import ClientError
from aiohttp.client_exceptions import ClientConnectorError
from nextdns import ApiError, InvalidApiKeyError

from smarthub.components.button import ButtonEntity, ButtonEntityDescription
from smarthub.const import EntityCategory
from smarthub.core import SmartHub
from smarthub.exceptions import SmartHubError
from smarthub.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import NextDnsConfigEntry
from .const import DOMAIN
from .entity import NextDnsEntity

PARALLEL_UPDATES = 1


CLEAR_LOGS_BUTTON = ButtonEntityDescription(
    key="clear_logs",
    translation_key="clear_logs",
    entity_category=EntityCategory.CONFIG,
)


async def async_setup_entry(
    hass: SmartHub,
    entry: NextDnsConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Add aNextDNS entities from a config_entry."""
    coordinator = entry.runtime_data.status

    async_add_entities([NextDnsButton(coordinator, CLEAR_LOGS_BUTTON)])


class NextDnsButton(NextDnsEntity, ButtonEntity):
    """Define an NextDNS button."""

    async def async_press(self) -> None:
        """Trigger cleaning logs."""
        try:
            await self.coordinator.nextdns.clear_logs(self.coordinator.profile_id)
        except (
            ApiError,
            ClientConnectorError,
            TimeoutError,
            ClientError,
        ) as err:
            raise SmartHubError(
                translation_domain=DOMAIN,
                translation_key="method_error",
                translation_placeholders={
                    "entity": self.entity_id,
                    "error": repr(err),
                },
            ) from err
        except InvalidApiKeyError:
            self.coordinator.config_entry.async_start_reauth(self.hass)
