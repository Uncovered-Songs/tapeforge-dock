# Network

TapeForge instances can form a **federated patchbay network** — a peer-to-peer coordination layer on a LAN with no centralized coordinator.

## How it works

The **patchbay agent** (`patchbay.exe`) runs alongside the four product apps on each instance. It handles:

- **mDNS service discovery** — instances find each other automatically on the LAN
- **Network lifecycle** — create, join, or leave a network
- **Leader election** — deterministic lowest-UUID-wins (with RT-server priority)
- **Membership tracking** — peers expire after ~15 seconds of silence
- **State broadcasting** — master maintains the authoritative network state

## Setup

During the first-run wizard (or via the patchbay's HTTP API), you can:

- **Create** — start a new network (your instance becomes the initial master)
- **Join** — enter a network UUID to join an existing network
- **Skip** — run in local-only mode (no federation)

## Patchbay API

The patchbay agent listens on `http://127.0.0.1:9100`:

| Endpoint | Method | Description |
|---|---|---|
| `/patchbay/status` | GET | Full network state document |
| `/patchbay/members` | GET | Peer list with last-heard timestamps |
| `/patchbay/identity` | GET | Local network identity |
| `/patchbay/election` | GET | Current master + election history |
| `/patchbay/network/create` | POST | Create a new network |
| `/patchbay/network/join` | POST | Join an existing network |
| `/patchbay/network/leave` | POST | Leave the network |
| `/patchbay/register` | POST | Register a product (auto-done by each app) |
| `/patchbay/deregister` | POST | Deregister a product |
| `/patchbay/events` | WS | Real-time event feed |

## Per-product proxy

Each product app also exposes `GET /network/peers` on its own web server. This proxies the patchbay's `/patchbay/members` endpoint (or returns `{"patchbay": false}` if the agent isn't running).

## CLI flags

```powershell
patchbay.exe --instance "D:\TapeForge" --port 9100 --discovery-window 10
```

| Flag | Description |
|---|---|
| `--port <int>` | Override the default port (9100) |
| `--discovery-window <sec>` | mDNS browse duration on NoNetwork startup (0 to skip) |

## mDNS service

The patchbay agent advertises `_tapeforge-patchbay._tcp.local.` with TXT records containing:

```
network=<networkUuid>
instance=<instanceUuid>
instance-name=<name>
master=<0|1>
rt-server=<0|1>
```

Members are filtered by the `network` value — different networks on the same LAN coexist independently.
