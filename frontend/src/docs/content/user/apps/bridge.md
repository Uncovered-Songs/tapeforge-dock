# Bridge — The Virtual Outboard Rack

Bridge is the virtual outboard rack. It receives multi-track audio from Capstan, applies a configurable VST plugin chain per track, and sends the processed result to Bus.

## Architecture

Bridge sits between Capstan and Bus in the signal chain:

```
Capstan → [Bridge] → Bus
```

Bridge consumes Capstan's shared-memory stream, processes each track through its plugin rack row-by-row, and publishes the processed multi-track stream for Bus to consume.

## Key features

- **Plugin rack** — configurable rows × tracks grid of VST3 plugins
- **Plugin types** — VST3 instruments and effects (via JUCE's VST3 hosting)
- **Per-row module types** — passthrough, trim/gain, VST host
- **Output modes** — DirectASIO, ExternalStream, Hybrid
- **Processing chain** — per-track signal flow through the rack
- **Template registry** — save and recall rack configurations

## Web UI

Bridge's frontend renders a product surface with:
- **Nameplate** — TapeForge logo, product wordmark, version, Capstan connection LED
- **Rack panel** — composition grid with track columns and row modules
- **Per-track headers** — track names from Capstan
- **Status bar** — ONLINE indicator, sample rate, buffer size, output mode, track count

## Roles

| Role | Description |
|---|---|
| `Disabled` | Bridge does nothing |
| `InternalProcessor` | Processes tracks internally, no ASIO I/O |
| `InternalProcessorWithDirectOuts` | Processes + sends to ASIO direct outputs |
| `AnalogToInternal` | Receives from ASIO inputs instead of Capstan stream |

## HTTP API

| Endpoint | Method | Description |
|---|---|---|
| `/status` | GET | Full rack status + audio config |
| `/rack/rows` | POST | Add a new rack row |
| `/rack/rows/<i>` | PUT/DELETE | Update or remove a row |
| `/rack/rows/<i>/module` | POST | Set module type for a row |
| `/track/<n>/output` | POST | Set track output routing |
| `/api/outputMode` | POST | Set output mode |
