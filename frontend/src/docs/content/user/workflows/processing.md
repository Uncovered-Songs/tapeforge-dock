# Processing Workflow

## Setup

1. **Ensure Capstan is running** with a loaded tape
2. **Launch Bridge** — `Bridge.exe --instance "D:\MyTapeForge"`
3. Bridge auto-discovers Capstan via mDNS and attaches to the stream

## Adding processing

1. Open Bridge's web UI (port 8081)
2. **Add a rack row** — click the + bar below the grid
3. **Select a plugin type** — passthrough, trim, or a VST3 plugin from your library
4. **Configure parameters** — each module exposes its controls

## Rack structure

Bridge's rack is a rows × tracks grid:
- Each row is a processing stage
- Each track column processes one channel
- Signal flows top-to-bottom through rows

## Monitoring

- Bridge's status bar shows output mode and track count
- Use the debug view (`?debug`) to see raw `/status` JSON
- Track output routing can be overridden per-track
