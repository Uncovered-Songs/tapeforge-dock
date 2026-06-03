# Build System

TapeForge uses CMake for C++ builds and pnpm for frontend packages.

## CMake presets

| Preset | Description |
|---|---|
| `x64-debug` | Debug build for Windows x64 |
| `x64-release` | Release build for Windows x64 |

```powershell
cmake --preset x64-release
cmake --build out/build/x64-release --target capstan
```

## add_tapeforge_app() macro

Defined in `shared/cmake/add_tapeforge_app.cmake`. Each app's `CMakeLists.txt` calls this macro:

```cmake
add_tapeforge_app(
  NAME            capstan
  DISPLAY_NAME    "Capstan"
  FRONTEND_DIR    "${CMAKE_CURRENT_SOURCE_DIR}/../frontend"
  SHARED
    tapeforge_utils
    tapeforge_config
    tapeforge_tape
    tapeforge_streaming
    tapeforge_audio
    tapeforge_web
    tapeforge_wizard
    tapeforge_license
  SOURCES
    src/main.cpp
    ...
)
```

The macro:
1. Creates the executable target with JUCE AppConsole
2. Links requested shared libraries
3. Auto-detects `frontend/package.json`:
   - **Present (Debug)**: `npm run build` as POST_BUILD step; serves from disk
   - **Present (Release)**: embeds `dist/` as `FrontendAssets.cpp` in the .exe
   - **Absent**: skips frontend integration; backend builds clean

## Frontend dependencies

```bash
pnpm install            # Install all workspace packages
pnpm build              # Build all app frontends
pnpm dev:capstan        # Dev server for Capstan
pnpm stories            # Histoire dev server for @tapeforge/ui
```

Workspace configured in `pnpm-workspace.yaml` (globs `packages/*` and `apps/*/frontend`).

## CI

GitHub Actions CI (`.github/workflows/ci.yml`) builds the Win + Mac + Linux matrix on every PR. Required-check gating blocks merges on cross-OS failure.

Current status: shared C++ libraries compile clean on all three OSes. Product code (apps) is Windows-only pending per-OS `main.cpp` port.

## Bundle script

```powershell
.\scripts\package.ps1
```

Produces a `TapeForge_vX.X.X.zip` with all four app binaries + README.

## Vendor dependencies

| Library | Location | Purpose |
|---|---|---|
| JUCE 8.0.12 | `vendor/JUCE/` | Audio framework |
| Crow (header-only) | `vendor/crow/` | HTTP/WebSocket server |
| ASIO standalone | `vendor/asio/` | Crow's asio dependency |
| Steinberg ASIO SDK | `vendor/asiosdk/` | ASIO audio driver (Windows-only) |
| GSAP 3.12+ | peer dependency | Animation (instrument runtime) |
