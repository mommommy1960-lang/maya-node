# Networking Service

Peer-to-peer networking infrastructure for MAYA Node.

## Purpose

Provides decentralized networking capabilities:
- Node discovery and peer management
- Encrypted point-to-point communication
- Mesh network topology
- Message routing and relaying
- NAT traversal

## Key Components

- `mesh.py` - Mesh network coordination
- `p2p.py` - Peer-to-peer protocol
- `discovery.py` - Node discovery mechanisms
- `transport.py` - Transport layer encryption

## Features

- **Decentralized**: No central server required
- **Encrypted**: All traffic encrypted by default
- **Resilient**: Multiple redundant paths
- **Scalable**: Efficient routing algorithms
- **Privacy-Preserving**: Minimal metadata exposure

## Usage

```python
from services.networking import MeshNetwork

network = MeshNetwork()
network.join()
network.send_message(peer_id, data)
```

## License

CERL-1.0
