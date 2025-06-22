"""Tests for Bosch Alarm component."""

import asyncio
from collections.abc import AsyncGenerator
import datetime as dt
from unittest.mock import AsyncMock, patch

import pytest
import voluptuous as vol

from smarthub.components.bosch_alarm.const import (
    ATTR_CONFIG_ENTRY_ID,
    ATTR_DATETIME,
    DOMAIN,
    SERVICE_SET_DATE_TIME,
)
from smarthub.core import SmartHub
from smarthub.exceptions import SmartHubError, ServiceValidationError
from smarthub.setup import async_setup_component
from smarthub.util import dt as dt_util

from . import setup_integration

from tests.common import MockConfigEntry


@pytest.fixture(autouse=True)
async def platforms() -> AsyncGenerator[None]:
    """Return the platforms to be loaded for this test."""
    with patch("smarthub.components.bosch_alarm.PLATFORMS", []):
        yield


async def test_set_date_time_service(
    hass: SmartHub,
    mock_panel: AsyncMock,
    area: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test that the service calls succeed if the service call is valid."""
    await setup_integration(hass, mock_config_entry)
    await hass.services.async_call(
        DOMAIN,
        SERVICE_SET_DATE_TIME,
        {
            ATTR_CONFIG_ENTRY_ID: mock_config_entry.entry_id,
            ATTR_DATETIME: dt_util.now(),
        },
        blocking=True,
    )
    mock_panel.set_panel_date.assert_called_once()


async def test_set_date_time_service_fails_bad_entity(
    hass: SmartHub,
    mock_panel: AsyncMock,
    area: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test that the service calls fail if the service call is done for an incorrect entity."""
    await setup_integration(hass, mock_config_entry)
    with pytest.raises(
        ServiceValidationError,
        match='Integration "bad-config_id" not found in registry',
    ):
        await hass.services.async_call(
            DOMAIN,
            SERVICE_SET_DATE_TIME,
            {
                ATTR_CONFIG_ENTRY_ID: "bad-config_id",
                ATTR_DATETIME: dt_util.now(),
            },
            blocking=True,
        )


async def test_set_date_time_service_fails_bad_params(
    hass: SmartHub,
    mock_panel: AsyncMock,
    area: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test that the service calls fail if the service call is done with incorrect params."""
    await setup_integration(hass, mock_config_entry)
    with pytest.raises(
        vol.MultipleInvalid,
        match=r"Invalid datetime specified:  for dictionary value @ data\['datetime'\]",
    ):
        await hass.services.async_call(
            DOMAIN,
            SERVICE_SET_DATE_TIME,
            {
                ATTR_CONFIG_ENTRY_ID: mock_config_entry.entry_id,
                ATTR_DATETIME: "",
            },
            blocking=True,
        )


async def test_set_date_time_service_fails_bad_year_before(
    hass: SmartHub,
    mock_panel: AsyncMock,
    area: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test that the service calls fail if the panel fails the service call."""
    await setup_integration(hass, mock_config_entry)
    with pytest.raises(
        vol.MultipleInvalid,
        match=r"datetime must be before 2038 for dictionary value @ data\['datetime'\]",
    ):
        await hass.services.async_call(
            DOMAIN,
            SERVICE_SET_DATE_TIME,
            {
                ATTR_CONFIG_ENTRY_ID: mock_config_entry.entry_id,
                ATTR_DATETIME: dt.datetime(2038, 1, 1),
            },
            blocking=True,
        )


async def test_set_date_time_service_fails_bad_year_after(
    hass: SmartHub,
    mock_panel: AsyncMock,
    area: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test that the service calls fail if the panel fails the service call."""
    await setup_integration(hass, mock_config_entry)
    mock_panel.set_panel_date.side_effect = ValueError()
    with pytest.raises(
        vol.MultipleInvalid,
        match=r"datetime must be after 2009 for dictionary value @ data\['datetime'\]",
    ):
        await hass.services.async_call(
            DOMAIN,
            SERVICE_SET_DATE_TIME,
            {
                ATTR_CONFIG_ENTRY_ID: mock_config_entry.entry_id,
                ATTR_DATETIME: dt.datetime(2009, 1, 1),
            },
            blocking=True,
        )


async def test_set_date_time_service_fails_connection_error(
    hass: SmartHub,
    mock_panel: AsyncMock,
    area: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test that the service calls fail if the panel fails the service call."""
    await setup_integration(hass, mock_config_entry)
    mock_panel.set_panel_date.side_effect = asyncio.InvalidStateError()
    with pytest.raises(
        SmartHubError,
        match=f'Could not connect to "{mock_config_entry.title}"',
    ):
        await hass.services.async_call(
            DOMAIN,
            SERVICE_SET_DATE_TIME,
            {
                ATTR_CONFIG_ENTRY_ID: mock_config_entry.entry_id,
                ATTR_DATETIME: dt_util.now(),
            },
            blocking=True,
        )


async def test_set_date_time_service_fails_unloaded(
    hass: SmartHub,
    mock_panel: AsyncMock,
    area: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test that the service calls fail if the config entry is unloaded."""
    await async_setup_component(hass, DOMAIN, {})
    mock_config_entry.add_to_hass(hass)
    with pytest.raises(
        SmartHubError,
        match=f"{mock_config_entry.title} is not loaded",
    ):
        await hass.services.async_call(
            DOMAIN,
            SERVICE_SET_DATE_TIME,
            {
                ATTR_CONFIG_ENTRY_ID: mock_config_entry.entry_id,
                ATTR_DATETIME: dt_util.now(),
            },
            blocking=True,
        )
