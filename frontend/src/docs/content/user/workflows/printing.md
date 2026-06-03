# Printing Workflow

## Setup

1. **Launch Print** — `Print.exe --instance "D:\MyTapeForge"`
2. Print auto-discovers Bus via mDNS and attaches to the stereo stream
3. Select a tape (the same tape Capstan is recording to)

## Creating a mixtape

1. Open Print's web UI (port 8083)
2. **Enter a name** for the mixtape
3. Press **REC** → Print creates:
   - `<tape>/mixtapes/<name>/audio.wav` (16-bit stereo WAV)
   - `<tape>/mixtapes/<name>/print-metadata.json` (name, timestamps, source)
   - `<tape>/mixtapes/<name>/bus-state.json` (mixer state at print time)
   - `<tape>/mixtapes/<name>/bridge-state.json` (rack state at print time, if Bridge was attached)
4. Press **STOP** to finalize

## Archiving

Completed mixtapes appear in Print's archive list. You can:
- **Load** — select a mixtape for playback
- **Play** — play back the finalized mix through Bus's stream
- **Wind** — forward/rewind at varispeed (±8× max)

## Sidecar snapshots

At print start, Print performs `/status` round-trips to Bus and (if applicable) Bridge, capturing their exact state. This means you can recall the exact mix and processing that produced a mixtape.
