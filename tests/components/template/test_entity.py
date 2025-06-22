"""Test abstract template entity."""

import pytest

from smarthub.components.template import entity as abstract_entity
from smarthub.core import SmartHub


async def test_template_entity_not_implemented(hass: SmartHub) -> None:
    """Test abstract template entity raises not implemented error."""

    entity = abstract_entity.AbstractTemplateEntity(None)
    with pytest.raises(NotImplementedError):
        _ = entity.referenced_blueprint

    with pytest.raises(NotImplementedError):
        entity._render_script_variables()
