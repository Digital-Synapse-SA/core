"""Common methods used across tests for Netatmo."""

from collections.abc import Iterator
from contextlib import contextmanager
import json
from typing import Any
from unittest.mock import patch

from syrupy.assertion import SnapshotAssertion

from smarthub.components.netatmo.const import DOMAIN
from smarthub.components.webhook import async_handle_webhook
from smarthub.const import Platform
from smarthub.core import SmartHub
from smarthub.helpers import entity_registry as er
from smarthub.util.aiohttp import MockRequest

from tests.common import MockConfigEntry, async_load_fixture
from tests.test_util.aiohttp import AiohttpClientMockResponse

COMMON_RESPONSE = {
    "user_id": "91763b24c43d3e344f424e8d",
    "home_id": "91763b24c43d3e344f424e8b",
    "home_name": "MYHOME",
    "user": {"id": "91763b24c43d3e344f424e8b", "email": "john@doe.com"},
}

FAKE_WEBHOOK_ACTIVATION = {
    "push_type": "webhook_activation",
}


async def snapshot_platform_entities(
    hass: SmartHub,
    config_entry: MockConfigEntry,
    platform: Platform,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Snapshot entities and their states."""
    with selected_platforms([platform]):
        assert await hass.config_entries.async_setup(config_entry.entry_id)

        await hass.async_block_till_done()
    entity_entries = er.async_entries_for_config_entry(
        entity_registry, config_entry.entry_id
    )

    assert entity_entries
    for entity_entry in entity_entries:
        assert entity_entry == snapshot(name=f"{entity_entry.entity_id}-entry")
        assert hass.states.get(entity_entry.entity_id) == snapshot(
            name=f"{entity_entry.entity_id}-state"
        )


async def fake_post_request(hass: SmartHub, *args: Any, **kwargs: Any):
    """Return fake data."""
    if "endpoint" not in kwargs:
        return "{}"

    endpoint = kwargs["endpoint"].split("/")[-1]

    if endpoint in "snapshot_720.jpg":
        return b"test stream image bytes"

    if endpoint in [
        "setpersonsaway",
        "setpersonshome",
        "setstate",
        "setroomthermpoint",
        "setthermmode",
        "switchhomeschedule",
    ]:
        payload = {f"{endpoint}": True, "status": "ok"}

    elif endpoint == "homestatus":
        home_id = kwargs.get("params", {}).get("home_id")
        payload = json.loads(
            await async_load_fixture(hass, f"{endpoint}_{home_id}.json", DOMAIN)
        )

    else:
        payload = json.loads(await async_load_fixture(hass, f"{endpoint}.json", DOMAIN))

    return AiohttpClientMockResponse(
        method="POST",
        url=kwargs["endpoint"],
        json=payload,
    )


async def fake_get_image(*args: Any, **kwargs: Any) -> bytes | str | None:
    """Return fake data."""
    if "endpoint" not in kwargs:
        return "{}"

    endpoint = kwargs["endpoint"].split("/")[-1]

    if endpoint in "snapshot_720.jpg":
        return b"test stream image bytes"
    return None


async def simulate_webhook(hass: SmartHub, webhook_id: str, response) -> None:
    """Simulate a webhook event."""
    request = MockRequest(
        method="POST",
        content=bytes(json.dumps({**COMMON_RESPONSE, **response}), "utf-8"),
        mock_source="test",
    )
    await async_handle_webhook(hass, webhook_id, request)
    await hass.async_block_till_done()


@contextmanager
def selected_platforms(platforms: list[Platform]) -> Iterator[None]:
    """Restrict loaded platforms to list given."""
    with (
        patch("smarthub.components.netatmo.data_handler.PLATFORMS", platforms),
        patch(
            "smarthub.helpers.config_entry_oauth2_flow.async_get_config_entry_implementation",
        ),
        patch(
            "smarthub.components.netatmo.webhook_generate_url",
        ),
    ):
        yield
