# Mixing Workflow

## Setup

1. **Launch Bus** — `Bus.exe --instance "D:\MyTapeForge"`
2. Bus auto-discovers its upstream source (Capstan or Bridge)
3. The mix panel renders with one strip per track

## Mixing

Each strip gives you:
- **VU meter** — vertical bar showing signal level
- **Pan knob** — stereo positioning
- **Fader** — level control (Shift+drag for fine adjustment)
- **Mute/Solo** — per-strip buttons

The master section provides:
- **Stereo VU** — left/right with analog ballistics
- **Master faders** — linked or independent L/R
- **Output routing**

## Source selection

Use `/api/input-source` or the UI to switch between:
- **Capstan** — direct from recorder
- **Bridge** — through VST processing
- **External** — from ASIO inputs

## ASIO monitoring

Bus drives ASIO monitor output directly. Your speakers/headphones connect to your interface's outputs as configured in Bus's monitor output routing.
