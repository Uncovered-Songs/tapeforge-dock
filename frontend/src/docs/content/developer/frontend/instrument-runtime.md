# Instrument Runtime

The **SVG Assembly System** is how TapeForge builds reusable, interactive, animated SVG-based instrument surfaces. Instead of hand-coded Vue components for every surface, instruments are described as compositions of reusable SVG parts via JSON assemblies.

## Pipeline

```
SVG Parts (data-tf-motion / data-tf-binding / data-tf-role / ...)
    ↓
JSON Assemblies (composition + motionSequences + continuousMotion)
    ↓
Runtime Instances (resolves bindings + actions + motion targets)
    ↓
Bound Interactive Instruments (host mounts; runtime owns the SVG)
```

## Key modules

Under `packages/ui/src/runtime/`:

| Module | Purpose |
|---|---|
| `parts.ts` / `assemblies.ts` | JSON-Schema-validated loaders |
| `instantiate.ts` | Mount parts + bind context + wire actions |
| `motion-state.ts` | GSAP timelines for state sequences with priority preemption |
| `motion-continuous.ts` | While-expression-driven continuous tweens |
| `bindings.ts` | Dot-path resolver + Vue ref reactivity + rAF batching |
| `errors.ts` | Structured error taxonomy |
| `debug-overlay.ts` | Opt-in `<g class="tf-debug-overlay">` with labels |
| `runtime.ts` | Singleton + editor surface |

## Dual-form policy

Every hardware-surface element is EITHER:

- A Vue instrument under `packages/ui/src/instruments/`
- An SVG assembly under `packages/ui/src/parts/` + `assemblies/`

Both are first-class. Plain HTML+CSS for hardware surfaces is forbidden.

## GSAP

GSAP is a peer dependency. Consumers that mount instruments install `gsap ^3.12`. Chrome-only consumers skip it (motion modules tree-shake out).

## Data attributes

Reserved `data-tf-*` attribute namespace:

| Attribute | Status |
|---|---|
| `data-tf-motion` | Active |
| `data-tf-binding` | Active |
| `data-tf-hit` | Reserved-but-inactive |
| `data-tf-role` | Reserved-but-inactive |
| `data-tf-node` | Reserved-but-inactive |
| `data-tf-semantic` | Reserved-but-inactive |
| `data-tf-runtime-owned` | Runtime marker |

Adding a seventh requires a spec change.
