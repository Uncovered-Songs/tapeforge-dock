# Bus — The Summing Mixer

Bus is the summing mixer. It receives multi-track audio (from Capstan or Bridge), sums it to a post-master stereo bus, drives ASIO monitor output, and publishes the stereo mix for Print to consume.

## Architecture

Bus consumes a producer stream and publishes a stereo output:

```
Capstan ──┬──→ Bus → ASIO monitor out
          │        │
Bridge  ──┘        └──→ Print (stereo)
```

## Key features

- **Per-strip mixing** — fader, pan, mute, solo per input channel
- **Master section** — stereo master fader with link/unlink
- **VU metering** — analog-style ballistics on each strip and master
- **Input source selection** — Capstan, Bridge, or External (ASIO)
- **Stereo bus output** — published via shared memory for Print
- **Multi-client ASIO** — simultaneous use with Capstan on supported drivers

## Web UI

Bus's frontend renders a product surface with:
- **Nameplate** — TapeForge logo, "BUS" wordmark, source-discovered LEDs
- **Mix panel** — per-strip vertical rack with VU, pan knob, fader, mute/solo
- **Master section** — stereo VU, master faders, output routing
- **Status bar** — ONLINE indicator, sample rate, source app, ASIO device

## Roles

| Role | Description |
|---|---|
| `InternalMixer` | Sums from upstream (Capstan or Bridge) shared-memory stream |
| `AnalogReceiver` | Receives from ASIO inputs directly |

## HTTP API

| Endpoint | Method | Description |
|---|---|---|
| `/status` | GET | Full mixer status (strips, master, source) |
| `/strip/<n>/fader` | POST | Set strip fader level |
| `/strip/<n>/pan` | POST | Set strip pan |
| `/strip/<n>/mute` | POST | Toggle strip mute |
| `/strip/<n>/solo` | POST | Toggle strip solo |
| `/master/fader` | POST | Set master fader level |
| `/master/linked` | POST | Set master link state |
| `/api/input-source` | POST | Switch input source |
| `/network/peers` | GET | Network peer info (via patchbay) |
