# Installation

## From a release bundle

1. Download the latest `TapeForge_vX.X.X.zip` from the releases page.
2. Extract to a portable drive (USB stick or SSD).
3. Launch any app's `.exe` directly from the extracted folder.

Each release bundle contains four single-exe binaries (Capstan, Bridge, Bus, Print) plus the patchbay agent. No installer required — TapeForge is designed to run from a dongle.

## Building from source

### Prerequisites

- CMake 3.28+
- Visual Studio 2022 (Windows) or Xcode (macOS) or GCC/Clang (Linux)
- Node.js 18+ and pnpm 9+

### Steps

```powershell
# Clone the repository
git clone <repo-url>
cd tapeforge

# Install frontend dependencies
pnpm install

# Configure and build (release)
cmake --preset x64-release
cmake --build out/build/x64-release --target capstan

# Build all apps
cmake --build out/build/x64-release --target capstan
cmake --build out/build/x64-release --target bridge
cmake --build out/build/x64-release --target bus
cmake --build out/build/x64-release --target print

# (Optional) Bundle into a distribution zip
.\scripts\package.ps1
```

## System requirements

- **Windows**: ASIO-compatible audio interface recommended. Windows 10 or later.
- **macOS**: CoreAudio-compatible interface. macOS 12+ recommended.
- **Linux**: ALSA or JACK/PipeWire. Tested on Ubuntu 24.04+.

> **Note**: macOS and Linux builds currently verify the shared library surface only. Product binaries (with full audio engine and tray UI) are Windows-only pending the per-OS `main.cpp` port.
