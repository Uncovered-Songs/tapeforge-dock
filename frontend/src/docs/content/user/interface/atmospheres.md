# Atmospheres

Atmospheres are TapeForge's **material** — the color, luminance, and studio environment the instrument lives in. They swap in by replacing a single `@import` in each app's `style.css`.

## Available atmospheres

| Atmosphere | Intent | Mood |
|---|---|---|
| **Technical Light** (default) | Daylight studio, predominantly white. Swiss-editorial / lab-notebook | Bright, clean |
| **Graphite Dark** | Classic studio control room, deep gray-black. Studer / SSL in low light | Dark, focused |
| **Analog Green** | Broadcast / radar console. Phosphor green on gray-green | Vintage tech |
| **Deep Blue** | Night-mode studio, deep navy / blue-black. Submarine-console | Deep, calm |
| **Warm Paper** | Vintage technical manuals, warm cream + dark brown. Letterpress + blueprint | Warm, archival |

## Switching atmospheres

Each atmosphere is a single CSS file under `packages/ui/src/theme/atmospheres/`. To preview:

1. Open the web UI for any app
2. Find the atmosphere picker in the status bar (or append `?atmosphere=<name>` to the URL)
3. Select your preferred atmosphere

All atmospheres satisfy the same token contract — body text contrast ≥ 7:1, every token defined, no missing values.
