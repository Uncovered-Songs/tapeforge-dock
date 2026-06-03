# App Structure

Each app follows the same pattern:

```
apps/<name>/backend/
├── CMakeLists.txt              (~50 lines, calls add_tapeforge_app)
├── src/
│   ├── main.cpp                JUCE app + tray icon
│   ├── core/Application.{h,cpp}    Wires shared libs + per-app modules
│   ├── audio/AudioEngine.{h,cpp}   Subclass of tapeforge::AudioEngineBase
│   ├── web/HttpRoutes.{h,cpp}      App-specific HTTP routes
│   └── (app-specific subsystems)
```

## Common bootstrap chain

Every app's `main()` runs the same ordered handshake:

1. Parse `--instance <path>` if supplied; otherwise discover
2. `InstanceDiscovery::discoverActiveInstance()` — enumerate mounted volumes
3. `InstanceSentinel::claim()` — single-instance lock
4. `LicenseChecker::verify()` — stub (returns Ok)
5. `MachineBindingStore::loadDefault()` — load per-(machine, scenario) binding
6. `Application::start(instanceRoot, binding, machineId, reconfigure)` — app-specific init

## Frontend integration

CMake auto-detects each app's `frontend/package.json`:

- **Debug**: `npm run build` as POST_BUILD step, `frontend/` served from disk
- **Release**: `dist/` compiled into `FrontendAssets.cpp` under `tapeforge::<app>::frontend`, self-contained .exe
- **Absent**: frontend integration skipped, backend still builds

## Per-app specifics

### Capstan

`apps/capstan/backend/src/`
- **tape/** — `TapeManager`, `TapeMachine`, `TapeStorage`, `TapeTrack`, `MemoryMappedTapeFile`
- **transport/** — transport state machine
- **monitoring/** — direct monitoring
- **audio/Calibrator** — latency calibration

### Bridge

`apps/bridge/backend/src/`
- **processing/** — `ProcessingChain`, `ProcessingRow`, `ModuleFactory`, `TemplateRegistry`, `PluginLibrary`, `modules/`
- **core/CapstanClient** — upstream connection
- **streaming/StreamConsumer** — stream drain

### Bus

`apps/bus/backend/src/`
- **core/SourceClient** — upstream source connection
- **streaming/StreamConsumer** — stream drain
- Stereo `SharedAudioStream` producer for `Local\bus_main_output`

### Print

`apps/print/backend/src/`
- **core/** — `BusClient`, `Prints`, `MixTape`
- **audio/** — `PrintRecorder`, `PrintPlayer`, `WavWriter`, `WavReader`
- **streaming/StreamConsumer** — stereo stream drain

### Patchbay

`apps/patchbay/backend/src/`
- **PatchbayAgent** — federation lifecycle (NoNetwork/InNetwork state machine)
- **PatchbayRoutes** — HTTP + WS API registrar
- No audio engine, no Vue surface
