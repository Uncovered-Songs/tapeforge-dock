# Portable Instance

TapeForge uses a **portable instance model**: everything — runtime binaries, config, projects, and audio — lives in a self-contained folder on a portable physical medium (USB stick, SSD, or fixed disk for headless deployments). The host machine contributes only its `machineId`.

The dongle is the source of truth. Nothing TapeForge-state-related lives in `%LOCALAPPDATA%` anymore.

## Canonical instance layout

```
TapeForge/                              ← the instance, on a dongle
├── runtime/                            Runtime binary + per-product binaries
├── .tapeforge/
│   ├── instance.json                   Instance UUID + name + licenseRef
│   ├── license.json                    Reserved (stub in dev mode)
│   ├── network.json                    Network membership (optional)
│   ├── network-state-cache.json        Network state cache (master only)
│   └── machine-bindings/<machineId>/
│       └── default.json                Per-(machine, scenario) binding
├── projects/<projectId>/
│   ├── project.json                    Project identity + track list
│   ├── tapes/<tapeId>/                 Audio data
│   └── .tapeforge/machine-state/
│       └── <machineId>/default.json    Per-(machine) project state
└── nodes/                              Reserved
```

## Bootstrap flow

1. Parse `--instance <path>` if supplied; otherwise enumerate mounted drives
2. Look for `.tapeforge/instance.json` at the volume root
3. Write a lock file to prevent multiple instances
4. Verify license (stub in dev mode)
5. Load machine binding for the current `machineId`
6. Start the app

## Multi-instance support

Each dongle is one instance. Multiple dongles on the same machine are allowed, but only one instance per dongle per machine. The patchbay agent coordinates multi-instance networking.
