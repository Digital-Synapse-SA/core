"""Tests for conversation entity."""

from unittest.mock import patch

from smarthub.components import conversation
from smarthub.core import Context, SmartHub, State
from smarthub.helpers import intent
from smarthub.setup import async_setup_component
from smarthub.util import dt as dt_util

from tests.common import mock_restore_cache


async def test_state_set_and_restore(hass: SmartHub) -> None:
    """Test we set and restore state in the integration."""
    entity_id = "conversation.home_assistant"
    timestamp = "2023-01-01T23:59:59+00:00"
    mock_restore_cache(hass, (State(entity_id, timestamp),))

    await async_setup_component(hass, "smarthub", {})
    await async_setup_component(hass, "conversation", {})

    state = hass.states.get(entity_id)
    assert state
    assert state.state == timestamp

    now = dt_util.utcnow()
    context = Context()

    with (
        patch(
            "smarthub.components.conversation.default_agent.DefaultAgent.async_process"
        ) as mock_process,
        patch("smarthub.util.dt.utcnow", return_value=now),
    ):
        intent_response = intent.IntentResponse(language="en")
        intent_response.async_set_speech("response text")
        mock_process.return_value = conversation.ConversationResult(
            response=intent_response,
        )
        await hass.services.async_call(
            "conversation",
            "process",
            {"text": "Hello"},
            context=context,
            blocking=True,
        )

    assert len(mock_process.mock_calls) == 1

    state = hass.states.get(entity_id)
    assert state
    assert state.state == now.isoformat()
    assert state.context is context
