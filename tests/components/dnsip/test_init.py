"""Test for DNS IP component Init."""

from __future__ import annotations

from unittest.mock import patch

from smarthub.components.dnsip.const import (
    CONF_HOSTNAME,
    CONF_IPV4,
    CONF_IPV6,
    CONF_PORT_IPV6,
    CONF_RESOLVER,
    CONF_RESOLVER_IPV6,
    DEFAULT_PORT,
    DOMAIN,
)
from smarthub.config_entries import SOURCE_USER, ConfigEntryState
from smarthub.const import CONF_NAME, CONF_PORT
from smarthub.core import SmartHub

from . import RetrieveDNS

from tests.common import MockConfigEntry


async def test_load_unload_entry(hass: SmartHub) -> None:
    """Test load and unload an entry."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        source=SOURCE_USER,
        data={
            CONF_HOSTNAME: "smart-hub.io",
            CONF_NAME: "smart-hub.io",
            CONF_IPV4: True,
            CONF_IPV6: False,
        },
        options={
            CONF_RESOLVER: "208.67.222.222",
            CONF_RESOLVER_IPV6: "2620:119:53::53",
            CONF_PORT: 53,
            CONF_PORT_IPV6: 53,
        },
        entry_id="1",
        unique_id="smart-hub.io",
    )
    entry.add_to_hass(hass)

    with patch(
        "smarthub.components.dnsip.config_flow.aiodns.DNSResolver",
        return_value=RetrieveDNS(),
    ):
        await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    assert entry.state is ConfigEntryState.LOADED
    assert await hass.config_entries.async_unload(entry.entry_id)
    await hass.async_block_till_done()
    assert entry.state is ConfigEntryState.NOT_LOADED


async def test_port_migration(
    hass: SmartHub,
) -> None:
    """Test migration of the config entry from no ports to with ports."""

    entry = MockConfigEntry(
        domain=DOMAIN,
        source=SOURCE_USER,
        data={
            CONF_HOSTNAME: "smart-hub.io",
            CONF_NAME: "smart-hub.io",
            CONF_IPV4: True,
            CONF_IPV6: True,
        },
        options={
            CONF_RESOLVER: "208.67.222.222",
            CONF_RESOLVER_IPV6: "2620:119:53::53",
        },
        entry_id="1",
        unique_id="smart-hub.io",
        version=1,
        minor_version=1,
    )
    entry.add_to_hass(hass)

    with patch(
        "smarthub.components.dnsip.sensor.aiodns.DNSResolver",
        return_value=RetrieveDNS(),
    ):
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    assert entry.version == 1
    assert entry.minor_version == 2
    assert entry.options[CONF_PORT] == DEFAULT_PORT
    assert entry.options[CONF_PORT_IPV6] == DEFAULT_PORT
    assert entry.state is ConfigEntryState.LOADED


async def test_migrate_error_from_future(hass: SmartHub) -> None:
    """Test a future version isn't migrated."""

    entry = MockConfigEntry(
        domain=DOMAIN,
        source=SOURCE_USER,
        data={
            CONF_HOSTNAME: "smart-hub.io",
            CONF_NAME: "smart-hub.io",
            CONF_IPV4: True,
            CONF_IPV6: True,
            "some_new_data": "new_value",
        },
        options={
            CONF_RESOLVER: "208.67.222.222",
            CONF_RESOLVER_IPV6: "2620:119:53::53",
        },
        entry_id="1",
        unique_id="smart-hub.io",
        version=2,
        minor_version=1,
    )
    entry.add_to_hass(hass)

    with patch(
        "smarthub.components.dnsip.sensor.aiodns.DNSResolver",
        return_value=RetrieveDNS(),
    ):
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    entry = hass.config_entries.async_get_entry(entry.entry_id)
    assert entry.state is ConfigEntryState.MIGRATION_ERROR
