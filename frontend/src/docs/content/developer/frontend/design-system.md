# Design System

`@tapeforge/ui` is the TapeForge design system — a shared visual language for all apps.

## Layout

```
packages/ui/src/
├── theme/
│   ├── tokens.css               Atmosphere-independent design tokens
│   └── atmospheres/             5 atmospheres (one CSS file each)
├── primitives/                  Generic chrome: UiButton, UiPanel, UiInput, etc.
├── instruments/                 Audio surfaces: UiKnob, UiFader, UiVuMeter, etc.
├── shell/                       UiStatusBar, UiTopBar, UiMachineSection
├── svg/                         Shared SVG drawing primitives
└── index.ts                     Re-exports
```

## Tokens

The atmosphere token surface is locked. Every atmosphere defines exactly the contract tokens:

```
Backgrounds:   --tf-bg, --tf-bg-deep, --tf-bg-elevated, --tf-bg-stage
Lines:         --tf-line-primary, --tf-line-emphasis, --tf-line-hairline
               --tf-line-accent, --tf-line-accent-base
               --tf-line-alert, --tf-line-success, --tf-line-info
Text:          --tf-text, --tf-text-strong, --tf-text-muted, --tf-text-dim
Glows:         --tf-glow-accent, --tf-glow-accent-base
               --tf-glow-success, --tf-glow-alert, --tf-glow-info
Motion:        --tf-motion-scale, --tf-motion-opacity
```

Run `pwsh scripts/audit-atmospheres.ps1` to verify all atmospheres satisfy the contract.

## Component inventory

Production-ready: `UiTransport`, `UiLed`, `UiLedMeter`, `UiMachineSection`, `UiButton`, `UiPanel`, `UiIndicator`, `UiStripFrame`, `UiTopBar`, `UiStatusBar`.

Skeleton (props/events frozen, placeholder render): `UiKnob`, `UiFader`, `UiVuMeter`, `UiMeterScale`, `UiReel`, `UiCassette`, `UiToggle`, `UiDropdown`, `UiInput`.

## Product shell primitives

Four primitives carry the product enclosure model:

- **`UiProductViewport`** — outermost container; fills the shell's main flex slot, centers the product, owns click-drag pan
- **`UiProductPanZoomSurface`** — auto-fit-to-window scaling with Ctrl+wheel zoom override
- **`UiProductEnclosure`** — the rounded chassis with nameplate slot, corner screws, edge shading + drop shadow
- **`UiProductFrame`** — internal panel sub-division primitive

## Stories

```bash
pnpm stories
```

Launches the Histoire dev server. Every instrument and primitive has a story under `stories/` exercising variants in isolation against each of the five atmospheres.
