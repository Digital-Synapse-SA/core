"""Provide common tests tools for conversation."""

from smarthub.components import conversation
from smarthub.core import SmartHub

from . import MockAgent

from tests.common import MockConfigEntry


def mock_conversation_agent_fixture_helper(hass: SmartHub) -> MockAgent:
    """Mock agent."""
    entry = MockConfigEntry(entry_id="mock-entry")
    entry.add_to_hass(hass)
    agent = MockAgent(entry.entry_id, ["smurfish"])
    conversation.async_set_agent(hass, entry, agent)
    return agent
