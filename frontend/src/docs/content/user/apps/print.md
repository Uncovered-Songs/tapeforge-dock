# Print — The Mastering / Archive Deck

Print is the mastering and archive deck. It consumes Bus's stereo output and writes finalized mixtapes (audio.wav + JSON sidecars) into the active tape directory.

## Architecture

Print is a pure consumer — it has no audio device of its own:

```
Bus → Print → mixtapes/<name>/audio.wav
```

A software `recordingLoop` thread drains Bus's shared-memory stereo stream at ~1-buffer cadence into `PrintRecorder` when recording.

## Key features

- **Stereo recording** — writes 16-bit WAV files from the 32-bit float stream
- **Print metadata** — captures bus-state and bridge-state at print time
- **Archive management** — list, load, play back completed mixtapes
- **Varispeed playback** — ±8× wind with configurable acceleration
- **Sidecar snapshots** — bus-state.json, bridge-state.json captured at print start

## Web UI

Print's frontend renders a product surface with:
- **Nameplate** — TapeForge logo, "PRINT" wordmark, Bus connection LED
- **Tape window** — cassette/reel focal area with timecode
- **Transport row** — REC, PLAY, STOP, FF, REW keys
- **Archive list** — completed mixtapes with status
- **Status bar** — ONLINE indicator, sample rate, source, atmosphere picker

## HTTP API

| Endpoint | Method | Description |
|---|---|---|
| `/status` | GET | Full print status (current tape, transport, archive) |
| `/print/start` | POST | Start printing (creates mixtape directory + begins recording) |
| `/print/stop` | POST | Stop printing and finalize WAV |
| `/print/play` | POST | Play back a loaded mixtape |
| `/print/list` | GET | List archived mixtapes for a tape |
| `/print/load` | POST | Load a mixtape for playback |
| `/print/forward` | POST | Wind forward |
| `/print/rewind` | POST | Wind backward |
| `/print/unload` | POST | Unload current mixtape |
