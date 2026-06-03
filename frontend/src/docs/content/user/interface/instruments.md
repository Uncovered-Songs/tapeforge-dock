# Instruments

The shared SVG vocabulary for audio surfaces. Every instrument primitive renders in SVG with `vector-effect="non-scaling-stroke"` and uses `--tf-*` design tokens — never hard-coded values.

## Instrument primitives

| Primitive | Purpose |
|---|---|
| `UiKnob` | Rotary control (continuous + stepped) |
| `UiFader` | Linear control |
| `UiVuMeter` | Analog-needle level meter |
| `UiLedMeter` | Segmented LED bar meter |
| `UiMeterScale` | Tick / label scale next to a meter |
| `UiTransport` | Transport-key cluster (REW / STOP / PLAY / REC / FF) |
| `UiReel` | Tape reel (animatable) |
| `UiCassette` | Cassette-deck face |
| `UiStripFrame` | Chassis for channel strips and rack modules |
| `UiLed` | Single status LED |
| `UiMachineSection` | Labelled subdivision of a front panel |

## Chrome primitives

| Primitive | Purpose |
|---|---|
| `UiButton` | Text / icon button |
| `UiToggle` | Boolean control |
| `UiDropdown` | Single-select |
| `UiInput` | Text / number input |
| `UiPanel` | Framed container |
| `UiIndicator` | Status pill (LIVE / ONLINE / etc.) |
| `UiStatusBar` | Bottom status strip |
| `UiTopBar` | Top shell with optional sidebar |

## Product shell primitives

| Primitive | Purpose |
|---|---|
| `UiProductViewport` | Outermost container, centers the product, owns click-drag pan |
| `UiProductPanZoomSurface` | Auto-fit-to-window scaling with Ctrl+wheel zoom |
| `UiProductEnclosure` | Rounded chassis with nameplate slot and edge shading |
| `UiProductFrame` | Internal panel sub-division with engraved-line zone |

## Interaction rules

- **Drag gestures** are vertical-only for knobs and faders
- **Modifier keys**: Shift = fine adjustment, Double-click = reset to default
- **Wheel**: captured on instruments (don't scroll the page)
- **Focused controls** accept keyboard input (arrows, PageUp/Down)

## Color semantics

| Meaning | Token | Use |
|---|---|---|
| Record | `--tf-line-alert` | REC-armed, recording, clip warnings |
| Monitoring | `--tf-line-emphasis` | SOLO, monitored channel, cue routing |
| Safe | `--tf-line-success` | Engaged-without-issue |
| Routing active | `--tf-line-accent` | Active signal path, focused control |
| Clipping | `--tf-line-alert` | Over-limit, clip LEDs |
| Disabled | `--tf-line-hairline` + 50% opacity | Bypassed, disabled |
