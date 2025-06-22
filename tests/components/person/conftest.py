"""The tests for the person component."""

import logging
from typing import Any

import pytest

from smarthub.components import person
from smarthub.components.person import DOMAIN
from smarthub.core import SmartHub
from smarthub.helpers import collection
from smarthub.setup import async_setup_component

from tests.common import MockUser

DEVICE_TRACKER = "device_tracker.test_tracker"
DEVICE_TRACKER_2 = "device_tracker.test_tracker_2"


@pytest.fixture
def storage_collection(hass: SmartHub) -> person.PersonStorageCollection:
    """Return an empty storage collection."""
    id_manager = collection.IDManager()
    return person.PersonStorageCollection(
        person.PersonStore(hass, person.STORAGE_VERSION, person.STORAGE_KEY),
        id_manager,
        collection.YamlCollection(
            logging.getLogger(f"{person.__name__}.yaml_collection"), id_manager
        ),
    )


@pytest.fixture
async def storage_setup(
    hass: SmartHub, hass_storage: dict[str, Any], hass_admin_user: MockUser
) -> None:
    """Storage setup."""
    hass_storage[DOMAIN] = {
        "key": DOMAIN,
        "version": 1,
        "data": {
            "persons": [
                {
                    "id": "1234",
                    "name": "tracked person",
                    "user_id": hass_admin_user.id,
                    "device_trackers": [DEVICE_TRACKER],
                }
            ]
        },
    }
    assert await async_setup_component(hass, DOMAIN, {})
