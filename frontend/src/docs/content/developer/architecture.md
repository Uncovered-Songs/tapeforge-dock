# Architecture

> **For the runtime audio algorithms** (the scheduler, lockstep, alignment, PDC,
> latency, telemetry), read **[Audio Engine & Algorithms](./cpp-core/audio-engine.md)**.
> This page is the high-level map.

## The four apps + the patchbay

TapeForge is **one technical instrument** built as five cooperating processes:

- **Capstan** — the tape deck. Records incoming audio to per-track float-32 tape
  files; plays tape back.
- **Bridge** — the insert processor. Runs a per-channel VST/FX chain on channels
  whose insert is engaged.
- **Bus** — the mixer/console. Sums all channels to the main + monitor outputs.
- **Print** — the mastering stage. Final stereo before the speakers; writes
  finalized mixtapes.
- **PATCH** (patchbay) — the conductor. Owns the soundcard, drives the whole
  audio graph, owns routing, and coordinates the network.

## PATCH-centric model (the important shift)

Earlier versions wired the products together with fixed point-to-point streams
(Capstan → Bridge → Bus → Print) and let each open its own audio device. The
current design is **PATCH-centric**:

- **PATCH is the single ASIO/CoreAudio owner.** It runs the one audio callback.
- Each buffer, PATCH **drives every product in lockstep** and routes their audio
  through **PATCH-owned per-channel shared-memory streams**. The products no
  longer talk to each other directly or open the device themselves — they run
  exactly once per buffer, when PATCH signals them.
- Routing is a **graph** PATCH enacts (and the operator edits in the patchbay
  graph UI), not hardwired links.

This is what gives cross-process audio a single clock and keeps every channel
sample-aligned. The full mechanism is in
[Audio Engine & Algorithms](./cpp-core/audio-engine.md).

## Signal flow (per channel)

```
                 ┌──────── PATCH owns ASIO + drives everything ────────┐
 ASIO in ─(A)──► │  source select (A live / B tape)                    │
                 │     │                                                │
 Capstan tape ─(B)─────┤                                                │
                 │     ├─ dry tap ─────────────► Capstan  (record)      │
                 │     │                                                │
                 │     └─ insert? ─► Bridge ─► (processed return) ─┐    │
                 │                                                  ▼    │
                 │                                       Bus (sum) ──► Print ─► ASIO out
                 └─────────────────────────────────────────────────────┘
```

Each channel independently chooses its source (A/B) and whether to run through
the insert. Everything resolves within one audio buffer (the insert is
"inline" / zero added buffers).

## IPC between processes

- **Audio frames**: lock-free **ring buffers** in named OS shared memory
  (Windows file mappings / POSIX `shm`), wire format `'TFST'` v2
  (`shared/cpp/streaming/src/StreamLayout.h`). See
  [IPC & Streaming](./cpp-core/ipc-streaming.md).
- **Per-buffer scheduling**: a cross-process barrier, **GraphSync**, lets PATCH
  signal a product and wait for it within the audio callback.
- **Control / status**: HTTP + WebSocket per app; the patchbay exposes
  `/patchbay/*` (graph, hardware, telemetry, routing).

## Portable instance model

The instance — binaries, config, projects, audio — lives in a self-contained
folder on a portable medium. The host contributes only its `machineId`; device +
sample-rate + buffer settings live in the per-machine **MachineBinding**. See
[Portable Instance](../user/configuration/portable-instance.md).

## Federated patchbay (multi-machine)

Beyond owning local audio, the patchbay agent provides peer-to-peer network
coordination (mDNS discovery + HTTP/WS) so multiple machines can see each other
and share streams (AES67). That federation layer coordinates *who is on the
network and what they offer* — distinct from the local audio graph.

## Source layout

1. **vendor/** — third-party deps (JUCE, Crow, ASIO SDK).
2. **shared/cpp/** — focused static libraries shared by all apps (streaming,
   audio/GraphSync, network, plugins, tape, …).
3. **apps/&lt;name&gt;/backend/** — per-app C++; **apps/&lt;name&gt;/frontend/** — per-app Vue UI.

Frontend deps use pnpm workspaces (`packages/*` + `apps/*/frontend`).
