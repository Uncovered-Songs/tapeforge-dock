# IPC & Streaming

How audio frames and control messages move between the five processes. For how
PATCH *uses* these streams each buffer (the scheduling/alignment algorithms), see
[Audio Engine & Algorithms](./audio-engine.md).

## Audio frames: lock-free shared-memory rings

Each mono audio "pipe" is a **lock-free ring buffer** in a named OS shared-memory
section:

| OS | Backend | Name example |
|---|---|---|
| Windows | `CreateFileMapping` | `Local\tf_chin_3` |
| macOS / Linux | `shm_open` + `mmap` | `/tf_chin_3` |

Abstracted by `SharedMemoryRegion` (`shared/cpp/streaming/src/`).

### Wire format — `'TFST'` v2

Defined in `shared/cpp/streaming/src/StreamLayout.h`:

```
┌────────────────────────────────────────────┐
│ StreamHeader                                 │
│   magic 'TFST', version, sampleRate,         │
│   channelCount, blockFrames, ringFrames,     │
│   writePosition, producerHeartbeat, …        │
├────────────────────────────────────────────┤
│ ConsumerSlot[8]                              │
│   connected, consumerId, readPosition,       │
│   heartbeat   (one per attached reader)      │
├────────────────────────────────────────────┤
│ float32 ring  [channelCount][ringFrames]     │
└────────────────────────────────────────────┘
```

Layout changes must bump `kStreamVersion`; new fields append to the end of the
header. The shape is mirrored by `@tapeforge/protocol` for HTTP/WS surfaces.

### Producer — `SharedAudioStream`

One writer. `writeBlock()` copies a block into the ring and atomically advances
`writePosition`. A monitor thread reclaims consumer slots whose heartbeat has gone
stale. Exposes `writePosition()` / `consumerLag()` for diagnostics.

### Consumer — `GraphStreamReader` (PATCH-driven mode)

Claims a `ConsumerSlot`, tracks its own `readPosition`, updates a heartbeat per
read. Two read modes:

- `readBlock()` — sequential read from `readPosition`.
- `readLatestBlock()` — **read-latest / drop-backlog**: snaps to the newest block
  each cycle. This is what keeps channels sample-aligned and self-healing — see
  [Audio Engine §7](./audio-engine.md#7-alignment--the-core-algorithm-read-latest).

> **Standing depth** = `writePosition − readPosition`: written-but-unread frames
> for a reader. Surfaced per leg on `GET /patchbay/graph` for drift diagnosis.

> **Known caveat:** `GraphStreamReader` heartbeats use `GetTickCount64` while the
> producer's reclaim monitor uses `steady_clock` — different clock domains, so
> producer-side "connected consumers" / write-leg depth gauges can read wrong.
> Audio is unaffected (readers don't gate on the connected flag). Logged for a
> clock-unification fix.

### PATCH-owned per-channel streams

In PATCH-centric mode the routing streams are owned and named by PATCH (stable,
order-independent names so a reader can attach before the writer exists):

| Stream | Written by | Read by |
|---|---|---|
| `tf_chin_<n>` | PATCH | Bus (channel input) |
| `tf_psend_<n>` | PATCH | Bridge (insert send) |
| `tf_prec_<n>` | PATCH | Capstan (dry record tap) |
| `capstan track-out-<n>` | Capstan | PATCH (tape return / "B") |
| `bridge proc-out-<n>` | Bridge | PATCH (processed insert return) |

## Per-buffer scheduling: GraphSync

Audio rings carry *samples*; **GraphSync** (`shared/cpp/audio/src/GraphSync.h`)
carries *timing*. It's a cross-process barrier PATCH uses inside the audio
callback to signal a product ("inputs ready") and wait for it ("outputs ready"),
with a short timeout + backoff so one slow product can't wedge the callback. See
[Audio Engine §4](./audio-engine.md#4-cross-process-lockstep-graphsync).

## Control & status: HTTP / WebSocket

- **Patchbay**: HTTP `/patchbay/*` (graph, hardware+latency, telemetry, routing,
  members) and `WS /patchbay/events` for membership/master/network/graph pushes.
- **Products**: each runs a web server (status + control) and a WebSocket worker
  broadcasting meters/status at ~10 Hz.
- **Network proxy**: each product proxies `GET /network/peers` to the local
  patchbay agent (`127.0.0.1:9100/patchbay/members`), returning
  `{"patchbay": false}` when the agent isn't running.

> Local HTTP always uses `127.0.0.1` (IPv4): Crow binds IPv4-only and on Windows
> `localhost` can resolve to `::1` first and hang.

## Service discovery (multi-machine)

Peer discovery across machines uses mDNS / DNS-SD (`_tapeforge-patchbay._tcp`).
Discovery requires the peers to share an L2 segment (one switch) — it does not
cross a Wi-Fi/Ethernet boundary.
