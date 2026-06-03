# Developer Guide

This guide explains TapeForge's internal architecture, tooling, and development workflows. It is intended for contributors working on the codebase.

## Repository layout

```
tapeforge/
├── apps/                      Per-app C++ backends + Vue frontends
│   ├── capstan/               The recorder
│   ├── bridge/                The VST rack
│   ├── bus/                   The summing mixer
│   ├── print/                 The mastering deck
│   ├── patchbay/              The network agent
│   └── devtools/              Contributor dev tooling
├── packages/                  Shared workspace packages (TypeScript/Vue)
│   ├── ui/                    @tapeforge/ui — design system
│   ├── composables/           @tapeforge/composables — shared Vue state
│   ├── protocol/              @tapeforge/protocol — wire format types
│   └── wizard-ui/             First-run wizard pages
├── shared/
│   ├── cpp/                   Shared C++ core (10 static libraries)
│   └── cmake/                 Shared CMake helpers
├── vendor/                    Third-party deps (JUCE, Crow, ASIO SDK)
├── openspec/                  Specifications and change proposals
├── design/                    Written design-language docs
├── scripts/                   Build, package, dev-setup scripts
├── docs/                      Architecture + porting notes
└── docusaurus/                This documentation site
```

## Technology stack

- **C++**: Audio engine, IPC, networking, web server
- **TypeScript/Vue 3**: Frontend UI for each app
- **CMake**: Build system
- **pnpm**: Frontend package management
- **JUCE 8.0.12**: Audio framework (vendored)
- **Crow**: HTTP/WebSocket server (header-only, vendored)
- **GSAP 3.12+**: Animation (peer dependency for instrument runtime)

## Documentation structure

- **Architecture** — system architecture, app relationships, data flow
- **C++ Core** — shared libraries, app structure, IPC/streaming
- **Frontend** — design system, instrument runtime, composables
- **Build System** — CMake configuration, presets, CI
- **Protocol** — HTTP/WebSocket wire format, shared-memory layout
- **Openspec** — how changes are proposed, reviewed, and archived
- **Migration** — porting from v0, v3 → A.1 portable instance
