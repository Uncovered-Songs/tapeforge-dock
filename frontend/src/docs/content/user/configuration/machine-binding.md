# Machine Binding

A **machine binding** defines how a specific instance behaves on a specific host machine. It replaces the old v3 `machine.json` model.

## Location

```
<instance>/.tapeforge/machine-bindings/<machineId>/default.json
```

## Schema (v1)

```json
{
  "schemaVersion": 1,
  "scenarioName": "default",
  "audioInterface": "<OS-specific device name>",
  "sampleRate": 48000,
  "bufferSize": 256,
  "trackCount": 16,
  "recordingPath": null,
  "perProductRoles": {
    "capstan": "Recorder",
    "bridge": "InternalProcessor",
    "bus": "InternalMixer",
    "print": "Printer"
  }
}
```

### Fields

| Field | Description |
|---|---|
| `schemaVersion` | Schema version (currently 1) |
| `scenarioName` | Scenario label (future multi-scenario support) |
| `audioInterface` | OS-specific audio device name |
| `sampleRate` | Sample rate in Hz |
| `bufferSize` | Buffer size in samples |
| `trackCount` | Number of tracks |
| `recordingPath` | Override for recording destination (null = dongle) |
| `perProductRoles` | Per-app role assignment |

### Roles

**Capstan**: `Disabled` | `Recorder`
**Bridge**: `Disabled` | `InternalProcessor` | `InternalProcessorWithDirectOuts` | `AnalogToInternal`
**Bus**: `InternalMixer` | `AnalogReceiver`
**Print**: `Disabled` | `Printer`

## First-run wizard

When no binding exists for the current `(instance, machineId)`, the app opens the first-run wizard. It writes the binding on `POST /api/setup/apply`.

## Migration from v3

If you're upgrading from the pre-A.1 layout:

```powershell
Capstan.exe --migrate-from-localappdata
```

This reads `%LOCALAPPDATA%\TapeForge\machine.json` and writes a new binding to the instance. The old file is left in place for rollback.
