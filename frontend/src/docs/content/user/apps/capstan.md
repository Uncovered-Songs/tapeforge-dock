# Capstan — The Recorder

Capstan is the multitrack recorder. It captures audio from an ASIO interface onto a **tape** (a directory of raw 32-bit float per-track files).

## Architecture

Capstan's audio engine receives multi-channel audio from your ASIO interface and writes each channel to a separate `track_NN.rawf32` file inside the active tape directory. It also publishes the live multi-track stream via shared memory for Bridge and/or Bus to consume.

## Key features

- **Multi-track recording** — 8–16+ tracks (configurable via `trackCount` in MachineBinding)
- **Per-track controls** — arm, mute, solo, input/output routing
- **Transport** — PLAY, STOP, REC, REW, FF with tape-machine acceleration ramps
- **Tape management** — create, select, rename tapes
- **Calibration** — per-machine latency measurement
- **Direct monitoring** — zero-latency monitoring through ASIO direct outs
- **Output modes** — DirectASIO, ExternalStream, Hybrid

## Web UI

Capstan's frontend renders a product surface with:
- **Nameplate** — TapeForge logo, product wordmark, version, downstream connection LEDs
- **Tape pane** — tape selector, transport, position counter, reel visualization
- **Track cards** — per-track strip cards in a configurable grid
- **Status bar** — ONLINE indicator, sample rate, buffer size, CPU, xRuns

Open `http://localhost:8080` (or the port assigned at startup) to access the web interface.

## CLI flags

| Flag | Description |
|---|---|
| `--instance <path>` | Path to the instance root |
| `--migrate-from-localappdata` | One-shot v3 → portable instance migration |

## HTTP API

Capstan exposes a REST API on its web port:

| Endpoint | Method | Description |
|---|---|---|
| `/status` | GET | Full app status (tracks, tape, transport, audio) |
| `/tapes` | POST | Create a new tape |
| `/tapes` | GET | List available tapes |
| `/play` | POST | Start playback |
| `/record` | POST | Start/stop recording |
| `/stop` | POST | Stop transport |
| `/track/<n>/arm` | POST | Arm/disarm track |
| `/track/<n>/input` | POST | Set track input routing |
| `/api/calibrate` | POST | Run latency calibration |
| `/api/outputMode` | POST | Set output mode |
