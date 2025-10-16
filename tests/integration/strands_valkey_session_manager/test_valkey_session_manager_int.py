from uuid import uuid4

import pytest
from strands import Agent
from valkey import Valkey

from strands_valkey_session_manager import ValkeySessionManager


@pytest.mark.integration
def test_agent_with_valkey_session():
    """
    You need to have a valkey/redis cluster/serverless available
    """
    valkey_client = Valkey(
        host="localhost",
        port="6379",
        decode_responses=True
    ) #, ssl=True, ssl_cert_reqs="none")
    # valkey_client = Valkey.from_url("rediss://default:key@credible-mastiff-14987.upstash.io:6379")

    test_session_id = str(uuid4())
    session_manager = ValkeySessionManager(session_id=test_session_id, client=valkey_client)
    try:
        agent = Agent(session_manager=session_manager)
        agent("Hello!")
        assert len(session_manager.list_messages(test_session_id, agent.agent_id)) == 2

        valkey_client_2 = Valkey(
            host="localhost",
            port="6379",
            decode_responses=True
        ) #, ssl=True, ssl_cert_reqs="none")
        # valkey_client_2 = Valkey.from_url("rediss://default:key@credible-mastiff-14987.upstash.io:6379")

        session_manager_2 = ValkeySessionManager(session_id=test_session_id, client=valkey_client_2)
        agent_2 = Agent(session_manager=session_manager_2)
        assert len(agent_2.messages) == 2
        agent_2("Hello!")
        assert len(agent_2.messages) == 4
        assert len(session_manager_2.list_messages(test_session_id, agent_2.agent_id)) == 4

        message = session_manager_2.read_message(test_session_id, agent_2.agent_id, 0)
        assert message.message["content"][0]["text"] == "Hello!"

        message.message["content"][0]["text"] = "Hello World!"
        session_manager_2.update_message(test_session_id, agent_2.agent_id, message)
        message = session_manager_2.read_message(test_session_id, agent_2.agent_id, 0)
        assert message.message["content"][0]["text"] == "Hello World!"

    finally:
        session_manager.delete_session(test_session_id)
        assert session_manager.read_session(test_session_id) is None
