# Protocol

## Shared-memory wire format

The `'TFST'` v2 layout is the canonical wire format for inter-process audio transport:

| Offset | Size | Field |
|---|---|---|
| 0 | 4 | Magic (`'TFST'`) |
| 4 | 4 | Version (2) |
| 8 | 4 | Channel count |
| 12 | 4 | Sample rate |
| 16 | 8 | Frame count |
| 24 | varies | Audio data (interleaved float32) |

Defined in `shared/cpp/streaming/src/StreamLayout.h` (C++) and mirrored by `@tapeforge/protocol` (TypeScript).

## HTTP API conventions

All apps follow a common REST pattern:

- `/status` — GET full app status (live JSON document)
- Per-resource endpoints for mutations: `POST /<resource>/<action>`
- Request body: JSON `{ "value": T }` for scalar setters
- Responses: JSON with status and optional data

## Per-app ports

| App | Default port |
|---|---|
| Capstan | 8080 (auto-probes {80, 8080, 8888, 8000}) |
| Bridge | 8081 (auto-probes {8081, 8082, 9000, 9001}) |
| Bus | 8082 (auto-probes) |
| Print | 8083 |
| Patchbay | 9100 (`--port <int>` override) |

## Patchbay WebSocket events

The patchbay agent pushes events over `WS /patchbay/events`:

| Event | Payload | Trigger |
|---|---|---|
| `membership-changed` | full membership list | Peer join/leave/expire |
| `master-changed` | new master identity | Election result |
| `network-changed` | network state | Create/join/leave |
| `products-changed` | product list | Register/deregister |
| `state-updated` | full state doc | Master rebuild |
| `patchbay-shutting-down` | — | Graceful shutdown |

## mDNS service types

| Service | Type | Instance name |
|---|---|---|
| Per-app web UI | `_http._tcp` (implied) | `capstan`, `bridge`, `bus` |
| Patchbay peer | `_tapeforge-patchbay._tcp.local` | instance UUID |

## Patchbay TXT record schema

```
network=<networkUuid>
instance=<instanceUuid>
instance-name=<name>
master=<0|1>
rt-server=<0|1>
```
