# First Run

## Launch order

When running multiple apps, launch them in signal-flow order:

1. **Capstan** — the recorder
2. **Bridge** (optional) — the processor
3. **Bus** — the mixer
4. **Print** — the archive deck

## Bootstrap flow

On first launch, each app performs the following handshake:

1. **Instance discovery** — scans mounted volumes for a TapeForge instance (a folder containing `.tapeforge/instance.json`).
2. **Single-instance check** — ensures only one copy of each app is running per machine.
3. **License check** — currently a no-op stub (returns OK in dev mode).
4. **Machine binding** — reads the per-(instance, machine) binding. If none exists, the first-run wizard opens.
5. **App start** — audio engine initializes, web server starts, product surface renders.

## Instance discovery

TapeForge operates on the **portable instance model**: the instance — runtime binaries, config, projects, and audio — lives in a self-contained folder. The host machine contributes only its `machineId`.

You can specify the instance path explicitly:

```powershell
Capstan.exe --instance "D:\TapeForge"
Bridge.exe --instance "D:\TapeForge"
```

Without `--instance`, each app scans mounted drive letters for a valid instance root.

## First-run wizard

When no machine binding exists for the current `(instance, machineId)`, the app forks into setup mode and opens the first-run wizard in your default browser. The wizard guides you through:

- Per-app role selection (Recorder, InternalProcessor, InternalMixer, etc.)
- ASIO/CoreAudio device selection
- Sample rate and buffer size configuration
- Network setup (join or create a TapeForge network)

After applying, the app exits. Re-launch it normally to use your configured setup.
