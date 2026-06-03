# Visual Language

TapeForge's visual language is a unified **technical / industrial** design system shared by all four apps. The goal: Capstan, Bridge, Bus, and Print should read as four modules of the same instrument — not four themed apps.

## Direction

TapeForge moves away from "modern audio software UI" (dark panels, localized skeuomorphism, plugin-like styling) toward:

- Front-panel-inspired layout (Studer, Neve, EMT, Dieter Rams)
- Swiss industrial typography and grid principles
- Monochrome / vector-first rendering
- Technical-drafting / schematic aesthetics
- SVG-driven instrument surfaces
- A line-weight and spacing system applied everywhere
- Unified motion grammar

## Six pillars

The language is defined by six pillars, each detailed in the [design specs](https://github.com/rssp7/tapeforge/tree/main/design):

| Pillar | Description |
|---|---|
| Geometry | Grid, panel proportions, spacing rhythm, machine-region composition |
| Typography | Type system, weights, label conventions, operational hierarchy |
| Line system | Stroke widths, dash patterns, hairlines, signal-path semantics |
| Motion | Easing curves, duration tiers, animation rules, idle-state discipline |
| Instrument primitives | The shared SVG vocabulary, color semantics, interaction philosophy |
| Signal language | Routing visualization, active-state semantics, stereo grouping |

## Rendering philosophy

- **HTML/CSS**: shell layout, docking, spacing, overlays, containers, scrolling
- **SVG**: instruments, panels, strips, meters, reels, scales, technical graphics
