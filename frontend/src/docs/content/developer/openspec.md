# Openspec

TapeForge uses **openspec** for specification and change management. The `openspec/` directory contains all specs and change proposals.

## Structure

```
openspec/
├── specs/                          Published capability specs
│   ├── tapeforge-portable-instance/spec.md
│   ├── tapeforge-federated-patchbay/spec.md
│   ├── tapeforge-cpp-architecture/spec.md
│   ├── tapeforge-design-system/spec.md
│   ├── tapeforge-themes/spec.md
│   └── ... (20+ specs)
├── changes/                        Active change proposals
│   ├── tapeforge-aes67-and-patchbay-ui/
│   │   ├── proposal.md
│   │   ├── tasks.md
│   │   └── specs/                  Change-specific spec overrides
│   ├── tapeforge-runtime-supervisor-and-scenarios/
│   └── ... (current changes)
├── changes/archive/                Archived (completed) changes
│   └── 2026-05-20-*/              Date-prefixed, contains tasks.md + specs/
└── config.yaml                     Openspec config
```

## How changes work

1. **Proposal** (`proposal.md`) — describes the problem, solution, and scope
2. **Specs** (`specs/`) — detailed technical specifications
3. **Tasks** (`tasks.md`) — numbered implementation tasks with status tracking
4. **Implementation** — code changes are made in the repository
5. **Archive** — completed changes are moved to `changes/archive/`

## Key spec milestones

| Date | Spec | Status |
|---|---|---|
| 2026-05-15 | tapeforge-cpp-core-port | Archived |
| 2026-05-16 | capstan-mvp | Archived |
| 2026-05-18 | bus-mix-faders-frontend | Archived |
| 2026-05-19 | bus-print-split | Archived |
| 2026-05-19 | physical-product-interface | Archived |
| 2026-05-20 | tapeforge-portable-instance-foundations (A.1) | Archived |
| 2026-05-20 | tapeforge-federated-patchbay (A.2) | Archived |
| 2026-05-20 | tapeforge-distributed-pivot-plan | Archived |
| In flight | tapeforge-aes67-and-patchbay-ui (A.3) | Active |
| In flight | tapeforge-runtime-supervisor-and-scenarios (Stage B) | Active |
| In flight | tapeforge-license-enforcement | Active |

## Validation

```bash
openspec validate <change-name> --strict
```

Runs structural validation against the openspec schema. Used in CI and as a pre-archive gate.
