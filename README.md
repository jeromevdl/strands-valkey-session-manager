# Strands Valkey / Redis Session Manager

[![Awesome Strands Agents](https://img.shields.io/badge/Awesome-Strands%20Agents-00FF77?style=flat-square&logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjkwIiBoZWlnaHQ9IjQ2MyIgdmlld0JveD0iMCAwIDI5MCA0NjMiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxwYXRoIGQ9Ik05Ny4yOTAyIDUyLjc4ODRDODUuMDY3NCA0OS4xNjY3IDcyLjIyMzQgNTYuMTM4OSA2OC42MDE3IDY4LjM2MTZDNjQuOTgwMSA4MC41ODQzIDcxLjk1MjQgOTMuNDI4MyA4NC4xNzQ5IDk3LjA1MDFMMjM1LjExNyAxMzkuNzc1QzI0NS4yMjMgMTQyLjc2OSAyNDYuMzU3IDE1Ni42MjggMjM2Ljg3NCAxNjEuMjI2TDMyLjU0NiAyNjAuMjkxQy0xNC45NDM5IDI4My4zMTYgLTkuMTYxMDcgMzUyLjc0IDQxLjQ4MzUgMzY3LjU5MUwxODkuNTUxIDQxMS4wMDlMMTkwLjEyNSA0MTEuMTY5QzIwMi4xODMgNDE0LjM3NiAyMTQuNjY1IDQwNy4zOTYgMjE4LjE5NiAzOTUuMzU1QzIyMS43ODQgMzgzLjEyMiAyMTQuNzc0IDM3MC4yOTYgMjAyLjU0MSAzNjYuNzA5TDU0LjQ3MzggMzIzLjI5MUM0NC4zNDQ3IDMyMC4zMjEgNDMuMTg3OSAzMDYuNDM2IDUyLjY4NTcgMzAxLjgzMUwyNTcuMDE0IDIwMi43NjZDMzA0LjQzMiAxNzkuNzc2IDI5OC43NTggMTEwLjQ4MyAyNDguMjMzIDk1LjUxMkw5Ny4yOTAyIDUyLjc4ODRaIiBmaWxsPSIjRkZGRkZGIi8+CjxwYXRoIGQ9Ik0yNTkuMTQ3IDAuOTgxODEyQzI3MS4zODkgLTIuNTc0OTggMjg0LjE5NyA0LjQ2NTcxIDI4Ny43NTQgMTYuNzA3NEMyOTEuMzExIDI4Ljk0OTIgMjg0LjI3IDQxLjc1NyAyNzIuMDI4IDQ1LjMxMzhMNzEuMTcyNyAxMDMuNjcxQzQwLjcxNDIgMTEyLjUyMSAzNy4xOTc2IDE1NC4yNjIgNjUuNzQ1OSAxNjguMDgzTDI0MS4zNDMgMjUzLjA5M0MzMDcuODcyIDI4NS4zMDIgMjk5Ljc5NCAzODIuNTQ2IDIyOC44NjIgNDAzLjMzNkwzMC40MDQxIDQ2MS41MDJDMTguMTcwNyA0NjUuMDg4IDUuMzQ3MDggNDU4LjA3OCAxLjc2MTUzIDQ0NS44NDRDLTEuODIzOSA0MzMuNjExIDUuMTg2MzcgNDIwLjc4NyAxNy40MTk3IDQxNy4yMDJMMjE1Ljg3OCAzNTkuMDM1QzI0Ni4yNzcgMzUwLjEyNSAyNDkuNzM5IDMwOC40NDkgMjIxLjIyNiAyOTQuNjQ1TDQ1LjYyOTcgMjA5LjYzNUMtMjAuOTgzNCAxNzcuMzg2IC0xMi43NzcyIDc5Ljk4OTMgNTguMjkyOCA1OS4zNDAyTDI1OS4xNDcgMC45ODE4MTJaIiBmaWxsPSIjRkZGRkZGIi8+Cjwvc3ZnPgo=&logoColor=white)](https://github.com/cagataycali/awesome-strands-agents)

A high-performance session manager for [Strands Agents](https://strandsagents.com) that uses Valkey / Redis for persistent storage. 
This enables agents to maintain conversation history and state across multiple interactions, even in distributed environments.

Tested with Elasticache Serverless ([Redis 7.1](https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/GettingStarted.serverless-redis.step1.html), [Valkey 8.1](https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/GettingStarted.serverless-valkey.step1.html)), 
Elasticache ([Redis 7.1](https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/SubnetGroups.designing-cluster-pre.redis.html), [Valkey 8.2](https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/SubnetGroups.designing-cluster-pre.valkey.html)) 
and [Upstash](https://upstash.com/).

## Features

- **Persistent Sessions**: Store agent conversations and state in Valkey/Redis
- **Distributed Ready**: Share sessions across multiple application instances
- **High Performance**: Leverage Valkey's speed for fast session operations
- **JSON Storage**: Native JSON support for complex data structures
- **Automatic Cleanup**: Built-in session management and cleanup capabilities

## Installation

```bash
pip install strands-valkey-session-manager
```

## Quick Start

```python
from strands import Agent
from strands_valkey_session_manager import ValkeySessionManager
from uuid import uuid4
import valkey

# Create a Valkey client
client = valkey.Valkey(host="localhost", port=6379, decode_responses=True)

# Create a session manager with a unique session ID
session_id = str(uuid4())
session_manager = ValkeySessionManager(
    session_id=session_id,
    client=client
)

# Create an agent with the session manager
agent = Agent(session_manager=session_manager)

# Use the agent - all messages are automatically persisted
agent("Hello! Tell me about Valkey.")

# The conversation is now stored in Valkey and can be resumed later, using the same session_id

# Display conversation history
print(f"\n{"=="*30}\n")
messages = session_manager.list_messages(session_id, agent.agent_id)
for msg in messages:
    role = msg.message["role"]
    content = msg.message["content"][0]["text"]
    print(f"** {role.upper()}**: {content}")
```

## Storage Structure

The ValkeySessionManager stores data using the following key structure:

```
session:<session_id>                                        # Session metadata
session:<session_id>:agent:<agent_id>                       # Agent state and metadata
session:<session_id>:agent:<agent_id>:message:<message_id>  # Individual messages
```

## API Reference

### ValkeySessionManager

```python
ValkeySessionManager(
    session_id: str,
    client: Union[valkey.Valkey, valkey.ValkeyCluster]
)
```

**Parameters:**
- `session_id`: Unique identifier for the session
- `client`: Configured Valkey client instance (only synchronous versions are supported)

**Methods** (Note that these methods are used transparently by Strands):
- `create_session(session)`: Create a new session
- `read_session(session_id)`: Retrieve session data
- `delete_session(session_id)`: Remove session and all associated data
- `create_agent(session_id, agent)`: Store agent in session
- `read_agent(session_id, agent_id)`: Retrieve agent data
- `update_agent(session_id, agent)`: Update agent state
- `create_message(session_id, agent_id, message)`: Store message
- `read_message(session_id, agent_id, message_id)`: Retrieve message
- `update_message(session_id, agent_id, message)`: Update message
- `list_messages(session_id, agent_id, limit=None)`: List all messages

## Contributing

### Setup

```bash
# Clone the repository
git clone https://github.com/jeromevdl/strands-valkey-session-manager
cd strands-valkey-session-manager

# Install in development mode with Hatch
hatch shell dev
```

### Running Tests

```bash
# Run unit tests only (default)
hatch run dev:test

# Run all tests including integration tests
hatch run dev:test-all

# Run with coverage
hatch run dev:test-cov
```

### Integration Tests

Integration tests require a running Valkey/Redis instance:

```bash
# Start Redis with JSON (Docker)
docker run -d -p 6379:6379 redislabs/rejson:latest

# Run integration tests
hatch run dev:test-integration
```

## Requirements

- Python 3.10+
- Valkey/Redis server
- strands-agents >= 1.0.0
- valkey >= 6.0.0

## License

MIT License - see [LICENSE](LICENSE) for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.