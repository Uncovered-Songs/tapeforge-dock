# Frontend Overview

The TypeScript / Vue side of the monorepo mirrors the C++ side: `packages/` for shared code, `apps/<name>/frontend/` for per-app shells.

## Workspace packages

| Package | Purpose |
|---|---|
| `@tapeforge/ui` (`packages/ui/`) | The design system. Vue 3 + SVG components, source-only (no build step). Instruments, chrome primitives, shell components, design tokens + atmospheres. |
| `@tapeforge/composables` (`packages/composables/`) | Runtime concerns shared by all apps. `useStatus`, `useWebSocket`, `useTransport`, `useMix`, `useRack`, `useTape`, `useTapeClock`. |
| `@tapeforge/protocol` (`packages/protocol/`) | Wire format types for HTTP + WebSocket. *(Forthcoming)* |
| `@tapeforge/wizard-ui` (`packages/wizard-ui/`) | First-run wizard Vue pages. |

## Per-app frontend

Each app's Vue shell sits in `apps/<name>/frontend/src/`. All four apps ship real shells composed against `@tapeforge/ui` primitives.

## Import convention

Every app's `src/style.css` opens with:

```css
@import "@tapeforge/ui/theme/tokens.css";
@import "@tapeforge/ui/theme/atmospheres/technical-light.css";
@import "./accent.css";
```

Switching atmospheres is a single-line `@import` swap.

## Dev run

```bash
# Start a single app's frontend dev server
pnpm dev:capstan
pnpm dev:bridge
pnpm dev:bus
```
