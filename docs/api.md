# MAYA Node – REST/grpc API Sketch

**Auth:** mTLS or token (local-first)

### Endpoints

- `GET /status` – SOC, temps, sources, loads
- `POST /dispatch` – Targets, constraints
- `POST /shed` – Control loads by priority
- `GET /telemetry` – History queries

Flexible for integrators; supports Modbus TCP, OPC UA.