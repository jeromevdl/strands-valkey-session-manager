"""Tests for ValkeySessionManager."""

import json
from unittest.mock import MagicMock, patch

import pytest
import valkey
from strands.agent.conversation_manager.null_conversation_manager import NullConversationManager
from strands.types.content import ContentBlock
from strands.types.exceptions import SessionException
from strands.types.session import Session, SessionAgent, SessionMessage, SessionType

from strands_valkey_session_manager import ValkeySessionManager


@pytest.fixture
def mock_valkey_client():
    """Mock Valkey client for testing."""
    client = MagicMock(spec=valkey.Valkey)
    # Default behavior: return None for JSON.GET (non-existent keys)
    client.execute_command.return_value = None
    client.exists.return_value = False
    client.scan.return_value = (0, [])
    return client


@pytest.fixture
def valkey_manager(mock_valkey_client):
    """Create ValkeySessionManager with mocked client."""
    # Mock the session repository methods during initialization
    with (
        patch.object(ValkeySessionManager, "read_session", return_value=None),
        patch.object(ValkeySessionManager, "create_session"),
    ):
        return ValkeySessionManager(session_id="test", client=mock_valkey_client)


@pytest.fixture
def sample_session():
    """Create sample session for testing."""
    return Session(
        session_id="test-session-123",
        session_type=SessionType.AGENT,
    )


@pytest.fixture
def sample_agent():
    """Create sample agent for testing."""
    return SessionAgent(
        agent_id="test-agent-456",
        state={"key": "value"},
        conversation_manager_state=NullConversationManager().get_state(),
    )


@pytest.fixture
def sample_message():
    """Create sample message for testing."""
    return SessionMessage.from_message(
        message={
            "role": "user",
            "content": [ContentBlock(text="test_message")],
        },
        index=0,
    )


def test_create_session(valkey_manager, sample_session, mock_valkey_client):
    """Test creating a session in Valkey."""
    mock_valkey_client.exists.return_value = False

    result = valkey_manager.create_session(sample_session)

    assert result == sample_session
    mock_valkey_client.execute_command.assert_called_once()
    args = mock_valkey_client.execute_command.call_args[0]
    assert args[0] == "JSON.SET"
    assert args[1] == "session:test-session-123"
    assert args[2] == "$"


def test_create_session_already_exists(valkey_manager, sample_session, mock_valkey_client):
    """Test creating a session that already exists."""
    mock_valkey_client.exists.return_value = True

    with pytest.raises(SessionException, match="already exists"):
        valkey_manager.create_session(sample_session)


def test_read_session(valkey_manager, sample_session, mock_valkey_client):
    """Test reading a session from Valkey."""
    session_data = json.dumps(sample_session.to_dict())
    mock_valkey_client.execute_command.return_value = session_data

    result = valkey_manager.read_session(sample_session.session_id)

    assert result.session_id == sample_session.session_id
    assert result.session_type == sample_session.session_type


def test_read_nonexistent_session(valkey_manager, mock_valkey_client):
    """Test reading a session that doesn't exist."""
    mock_valkey_client.execute_command.return_value = None

    result = valkey_manager.read_session("nonexistent-session")

    assert result is None


def test_delete_session(valkey_manager, sample_session, mock_valkey_client):
    """Test deleting a session from Valkey."""
    mock_valkey_client.scan.return_value = (0, [b"session:test-session-123", b"session:test-session-123:agent:test"])

    valkey_manager.delete_session(sample_session.session_id)

    assert mock_valkey_client.delete.call_count == 2


def test_delete_nonexistent_session(valkey_manager, mock_valkey_client):
    """Test deleting a session that doesn't exist."""
    mock_valkey_client.scan.return_value = (0, [])

    with pytest.raises(SessionException, match="does not exist"):
        valkey_manager.delete_session("nonexistent")


def test_create_agent(valkey_manager, sample_session, sample_agent, mock_valkey_client):
    """Test creating an agent in Valkey."""
    valkey_manager.create_agent(sample_session.session_id, sample_agent)

    mock_valkey_client.execute_command.assert_called_once()
    args = mock_valkey_client.execute_command.call_args[0]
    assert args[0] == "JSON.SET"
    assert args[1] == "session:test-session-123:agent:test-agent-456"


def test_read_agent(valkey_manager, sample_session, sample_agent, mock_valkey_client):
    """Test reading an agent from Valkey."""
    agent_data = json.dumps(sample_agent.to_dict())
    mock_valkey_client.execute_command.return_value = agent_data

    result = valkey_manager.read_agent(sample_session.session_id, sample_agent.agent_id)

    assert result.agent_id == sample_agent.agent_id
    assert result.state == sample_agent.state


def test_read_nonexistent_agent(valkey_manager, sample_session, mock_valkey_client):
    """Test reading an agent that doesn't exist."""
    mock_valkey_client.execute_command.return_value = None

    result = valkey_manager.read_agent(sample_session.session_id, "nonexistent_agent")

    assert result is None


def test_update_agent(valkey_manager, sample_session, sample_agent, mock_valkey_client):
    """Test updating an agent in Valkey."""
    # Mock reading existing agent
    agent_data = json.dumps(sample_agent.to_dict())
    mock_valkey_client.execute_command.return_value = agent_data

    sample_agent.state = {"updated": "value"}
    valkey_manager.update_agent(sample_session.session_id, sample_agent)

    # Should call JSON.GET then JSON.SET
    assert mock_valkey_client.execute_command.call_count == 2


def test_update_nonexistent_agent(valkey_manager, sample_session, sample_agent, mock_valkey_client):
    """Test updating an agent that doesn't exist."""
    mock_valkey_client.execute_command.return_value = None

    with pytest.raises(SessionException, match="does not exist"):
        valkey_manager.update_agent(sample_session.session_id, sample_agent)


def test_create_message(valkey_manager, sample_session, sample_agent, sample_message, mock_valkey_client):
    """Test creating a message in Valkey."""
    valkey_manager.create_message(sample_session.session_id, sample_agent.agent_id, sample_message)

    mock_valkey_client.execute_command.assert_called_once()
    args = mock_valkey_client.execute_command.call_args[0]
    assert args[0] == "JSON.SET"
    assert args[1] == "session:test-session-123:agent:test-agent-456:message:0"


def test_read_message(valkey_manager, sample_session, sample_agent, sample_message, mock_valkey_client):
    """Test reading a message from Valkey."""
    message_data = json.dumps(sample_message.to_dict())
    mock_valkey_client.execute_command.return_value = message_data

    result = valkey_manager.read_message(sample_session.session_id, sample_agent.agent_id, sample_message.message_id)

    assert result.message_id == sample_message.message_id
    assert result.message["role"] == sample_message.message["role"]


def test_read_nonexistent_message(valkey_manager, sample_session, sample_agent, mock_valkey_client):
    """Test reading a message that doesn't exist."""
    mock_valkey_client.execute_command.return_value = None

    result = valkey_manager.read_message(sample_session.session_id, sample_agent.agent_id, 999)

    assert result is None


def test_update_message(valkey_manager, sample_session, sample_agent, sample_message, mock_valkey_client):
    """Test updating a message in Valkey."""
    # Mock reading existing message
    message_data = json.dumps(sample_message.to_dict())
    mock_valkey_client.execute_command.return_value = message_data

    sample_message.message["content"] = [ContentBlock(text="Updated content")]
    valkey_manager.update_message(sample_session.session_id, sample_agent.agent_id, sample_message)

    # Should call JSON.GET then JSON.SET
    assert mock_valkey_client.execute_command.call_count == 2


def test_update_nonexistent_message(valkey_manager, sample_session, sample_agent, sample_message, mock_valkey_client):
    """Test updating a message that doesn't exist."""
    mock_valkey_client.execute_command.return_value = None

    with pytest.raises(SessionException, match="does not exist"):
        valkey_manager.update_message(sample_session.session_id, sample_agent.agent_id, sample_message)


def test_list_messages_all(valkey_manager, sample_session, sample_agent, mock_valkey_client):
    """Test listing all messages from Valkey."""
    # Mock scan response
    mock_valkey_client.scan.return_value = (
        0,
        [
            b"session:test-session-123:agent:test-agent-456:message:0",
            b"session:test-session-123:agent:test-agent-456:message:1",
        ],
    )

    # Mock JSON.GET responses for each message
    mock_valkey_client.execute_command.side_effect = [
        json.dumps({"message_id": 0, "message": {"role": "user", "content": [{"text": "msg1"}]}}),
        json.dumps({"message_id": 1, "message": {"role": "assistant", "content": [{"text": "msg2"}]}}),
    ]

    result = valkey_manager.list_messages(sample_session.session_id, sample_agent.agent_id)

    assert len(result) == 2
    assert result[0].message_id == 0
    assert result[1].message_id == 1
