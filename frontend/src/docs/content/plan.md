# Documentation Plan

This document outlines the full scope of documentation needed for TapeForge, derived from reviewing the architecture docs, openspec specs/changes, design docs, and codebase.

## Current state

We have stub/overview pages for every topic in both the User and Developer guides. The existing docs/ directory (`architecture.md`, `migration-v0.md`, `porting-from-v0.md`) have been migrated into the Developer Guide. Each stub contains the high-level structure and key points extracted from the codebase.

## What needs to be fully written (in priority order)

### User Guide — high priority

#### Getting Started
- [x] **Overview** — done (stub with app table)
- [ ] **Installation** — stub written; needs screenshots, troubleshooting, OS-specific notes
- [ ] **First Run** — stub written; needs screenshots of wizard, walkthrough with ASIO setup
- [ ] **Quickstart** — stub written; needs end-to-end verification

#### The Four Apps
- [x] **Capstan** — detailed, covers key features, HTTP API, CLI
- [x] **Bridge** — detailed, covers roles, rack, API
- [x] **Bus** — detailed, covers mixing, source selection, API
- [x] **Print** — detailed, covers printing, archiving, sidecars

#### User Interface
- [ ] **Visual Language** — stub; needs images showing the technical aesthetic, design examples
- [ ] **Atmospheres** — stub; needs screenshots of each atmosphere
- [ ] **Instruments** — stub; needs interactive examples, keybinding reference

#### Workflows
- [x] **Recording** — detailed
- [x] **Processing** — detailed
- [x] **Mixing** — detailed
- [x] **Printing** — detailed

#### Configuration
- [x] **Portable Instance** — detailed with layout diagram
- [x] **Machine Binding** — detailed with schema reference
- [x] **Network** — detailed with API reference

#### Troubleshooting
- [ ] **Troubleshooting** — stub; needs expansion based on real user issues

### Developer Guide — high priority

#### Overview
- [x] **Overview** — comprehensive repository layout + tech stack

#### Architecture
- [x] **Architecture** — detailed with signal flow diagram (ASCII)

#### C++ Core
- [x] **Overview** — library dependency table, namespace strategy
- [x] **Shared Libraries** — per-library API survey
- [x] **App Structure** — bootstrap chain, per-app modules
- [ ] **IPC & Streaming** — detailed; needs wire format diagram, code examples

#### Frontend
- [x] **Overview** — workspace packages, dev run
- [x] **Design System** — tokens, components, stories
- [x] **Instrument Runtime** — pipeline, modules, data attributes
- [x] **Composables** — full API reference with types

#### Build System
- [x] **Build System** — CMake presets, macro, pnpm, CI

#### Protocol
- [x] **Protocol** — wire format, ports, WebSocket events, mDNS schema

#### Openspec
- [x] **Openspec** — structure, change workflow, spec milestones

#### Migration
- [x] **Migration** — v0→v1, v3→A.1, file mapping table

## Medium priority — new topics needed

### User Guide
- **[App Signals]** — Understanding signal flow between the four apps (diagram-heavy)
- **[Keyboard Shortcuts]** — Global shortcuts for transport, navigation
- **[CLI Reference]** — Comprehensive CLI flags for all 5 binaries
- **[FAQ]** — Common questions collected from development experience
- **[Release Notes]** — Per-version changelog

### Developer Guide
- **[Contributing]** — How to set up dev environment, coding standards, PR workflow
- **[Testing]** — How to run tests, smoke test procedures
- **[Design Docs Index]** — Auto-generated or curated index of all design/ docs
- **[Glossary]** — TapeForge terminology (tape, mixtape, instance, machine binding, scenario, etc.)

## Lower priority — nice to have

- **Video tutorials** — Quickstart walkthrough video
- **API Reference** — Auto-generated OpenAPI/Swagger from the HTTP routes
- **Troubleshooting by error code** — Error code → resolution table
- **Architecture Decision Records (ADRs)** — Key decisions and rationale
- **Per-OS notes** — Windows vs macOS vs Linux differences in setup, limitations

## Sources to mine for content

| Source | Content |
|---|---|
| `docs/architecture.md` (543 lines) | Full architecture, IPC, resource layout, frontend structure |
| `docs/porting-from-v0.md` (343 lines) | Migration log, file mappings, cross-app smoke tests |
| `docs/migration-v0.md` (57 lines) | v0→v1 data migration script contract |
| `openspec/specs/` (20+ specs) | Detailed specs for every system component |
| `openspec/changes/` | Implementation proposals and task tracking |
| `design/` (10 files) | Visual language, geometry, typography, motion, instruments |
| `packages/ui/README.md` | Design system reference, component inventory |
| `packages/composables/README.md` | Composable API surface |
| `packages/protocol/README.md` | Protocol type reference |
| `shared/cpp/README.md` | Shared C++ library overview |
| Code header comments | Inline documentation in source files |

## Task list for filling stubs

1. **Screenshots**: Capture each app's web UI in each atmosphere (5 atmospheres × 4 apps = 20 images)
2. **Flow diagrams**: Generate SVG/PNG diagrams for signal flow (Capstan→Bridge→Bus→Print, IPC ring buffer, patchbay network)
3. **Installation walkthrough**: Verify on clean Windows, macOS, Linux; document differences
4. **Wizard walkthrough**: Step-by-step with screenshots for each wizard page
5. **API completeness audit**: Cross-reference every HTTP route across all 5 binaries; add any missing to docs
6. **CLI audit**: Cross-reference every CLI flag; add comprehensive reference
7. **Design doc integration**: For each design pillar (geometry, typography, etc.), add a developer-facing summary
8. **Spec index**: Generate a cross-reference from openspec specs → code locations → documentation pages
9. **Troubleshooting expansion**: Catalog all error messages in the codebase; write resolution for each
10. **Keyboard shortcuts**: Define and document a complete keyboard navigation scheme

## How pages map to source

| Doc page | Source files |
|---|---|
| User: Capstan | `apps/capstan/backend/`, `openspec/specs/capstan-*`, `design/instruments.md` (transport) |
| User: Bridge | `apps/bridge/backend/`, `openspec/specs/bridge-*`, `openspec/specs/bridge-rack-*` |
| User: Bus | `apps/bus/backend/`, `openspec/specs/bus-*`, `openspec/specs/bus-mix-*` |
| User: Print | `apps/print/backend/`, `openspec/changes/bus-print-split/` |
| User: Visual Language | `design/language.md`, `design/geometry.md`, `design/typography.md`, `design/line-weights.md` |
| User: Atmospheres | `design/atmospheres/`, `packages/ui/src/theme/atmospheres/`, `openspec/specs/tapeforge-themes/` |
| User: Instruments | `design/instruments.md`, `packages/ui/src/instruments/` |
| User: Portable Instance | `docs/architecture.md` (§Portable instance model), `openspec/specs/tapeforge-portable-instance/` |
| User: Machine Binding | `docs/architecture.md` (§Resource layout), `openspec/specs/tapeforge-machine-config/` |
| User: Network | `docs/architecture.md` (§Federated patch bay), `openspec/specs/tapeforge-federated-patchbay/` |
| Dev: Architecture | `docs/architecture.md` (full) |
| Dev: C++ Shared Libs | `shared/cpp/`, `docs/architecture.md` (§C++ source layout) |
| Dev: App Structure | `apps/*/backend/`, `shared/cmake/add_tapeforge_app.cmake` |
| Dev: IPC & Streaming | `shared/cpp/streaming/`, `docs/architecture.md` (§IPC between apps) |
| Dev: Design System | `packages/ui/`, `design/` |
| Dev: Instrument Runtime | `packages/ui/src/runtime/`, `design/assembly-system.md` |
| Dev: Composables | `packages/composables/` |
| Dev: Build System | `CMakeLists.txt`, `CMakePresets.json`, `shared/cmake/`, `scripts/` |
| Dev: Protocol | `packages/protocol/`, `shared/cpp/streaming/src/StreamLayout.h` |
| Dev: Openspec | `openspec/` |
| Dev: Migration | `docs/migration-v0.md`, `docs/porting-from-v0.md` |
