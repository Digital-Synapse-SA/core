"""Test KNX scene."""

from smarthub.components.knx.const import KNX_ADDRESS
from smarthub.components.knx.schema import SceneSchema
from smarthub.const import CONF_ENTITY_CATEGORY, CONF_NAME, EntityCategory
from smarthub.core import SmartHub
from smarthub.helpers import entity_registry as er

from .conftest import KNXTestKit


async def test_activate_knx_scene(
    hass: SmartHub, knx: KNXTestKit, entity_registry: er.EntityRegistry
) -> None:
    """Test KNX scene."""
    await knx.setup_integration(
        {
            SceneSchema.PLATFORM: [
                {
                    CONF_NAME: "test",
                    SceneSchema.CONF_SCENE_NUMBER: 24,
                    KNX_ADDRESS: "1/1/1",
                    CONF_ENTITY_CATEGORY: EntityCategory.DIAGNOSTIC,
                },
            ]
        }
    )

    entity = entity_registry.async_get("scene.test")
    assert entity.entity_category is EntityCategory.DIAGNOSTIC
    assert entity.unique_id == "1/1/1_24"

    await hass.services.async_call(
        "scene", "turn_on", {"entity_id": "scene.test"}, blocking=True
    )

    # assert scene was called on bus
    await knx.assert_write("1/1/1", (0x17,))
