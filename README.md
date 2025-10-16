# Strands Valkey / Redis Session Manager

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
client = valkey.Valkey(host="host", port=6379, decode_responses=True)

# Create a session manager with a unique session ID
session_manager = ValkeySessionManager(
    session_id=str(uuid4()),
    client=client
)

# Create an agent with the session manager
agent = Agent(session_manager=session_manager)

# Use the agent - all messages and state are automatically persisted
agent("Hello! Tell me about Valkey.")

# The conversation is now stored in Valkey and can be resumed later
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