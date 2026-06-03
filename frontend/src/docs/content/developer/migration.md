# Migration Guide

This guide covers migrating from the v0 codebase and from the v3 data layout.

## v0 → v1 migration

The v0 codebase lives in sibling directories (`Capstan/`, `Bridge/`, `Bus/`, `tapeforge-ui/`). This monorepo is a clean rebuild against a unified design language.

### What ports forward

- **C++ audio core** — AudioEngine, SharedAudioStream, WebServer, VstHost, bug fixes
- **JUCE + Crow** — collapsed from three vendored copies to one
- **TypeScript/Vue** — composables refactored into `@tapeforge/composables`, protocol types → `@tapeforge/protocol`
- **openspec/** — specs and change archives

### What is rebuilt

- Every Vue component that renders pixels (new SVG-driven instrument language)
- `tapeforge-ui/` → `packages/ui/` (new visual contract)
- Build scripts → monorepo CMake + pnpm
- Repo structure → `shared/` + `vendor/` + `apps/` + `packages/`

### What is rethought

- Resource handling: per-app configs → shared machine config and tape-as-container model
- Protocol details: minor refinements

## v3 → portable instance (A.1)

The pre-A.1 layout used `%LOCALAPPDATA%\TapeForge\machine.json`. A.1 replaces this with per-(instance, machine, scenario) bindings on the dongle.

### Migration command

```powershell
Capstan.exe --migrate-from-localappdata
```

### What it does

1. Reads `%LOCALAPPDATA%\TapeForge\machine.json` (instanceRoot, roles, audio settings)
2. Reads `<instanceRoot>\.tapeforge\instance.json` (trackCount)
3. Reads current machine's `machineId`
4. Writes `<instanceRoot>\.tapeforge\machine-bindings\<machineId>\default.json` with migrated values

### Safety

- Refuses to overwrite an existing binding (idempotent)
- Leaves old `machine.json` in place (rollback possible)
- Refuses if source is unreadable or destination is unwritable

### After migration

```powershell
Capstan.exe --instance "<instanceRoot>"
```

All products use `--instance <path>` or rely on dongle auto-discovery.

## Key code migrations

| v0 path | v1 path |
|---|---|
| `Capstan/src/main.cpp` | `apps/capstan/backend/src/main.cpp` |
| `Bridge/src/main.cpp` | `apps/bridge/backend/src/main.cpp` |
| `Bus/src/main.cpp` | `apps/bus/backend/src/main.cpp` |
| `Capstan/src/core/Config.{h,cpp}` | (replaced by shared `MachineConfigStore` + `InstanceConfigStore` etc.) |
| `Bus/src/core/Prints.{h,cpp}` | `apps/bus/backend/src/core/Prints.{h,cpp}` (path migration) |
| `Bus/src/audio/PrintRecorder.{h,cpp}` | `apps/bus/backend/src/audio/PrintRecorder.{h,cpp}` (re-rooted) |

For the full file mapping, see `docs/porting-from-v0.md` in the repository.
