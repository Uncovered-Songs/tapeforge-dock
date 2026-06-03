# TapeForge Dock

The online operating platform for **TapeForge**.

Dock is where you run your TapeForge environment from the browser:

- **Overview** — organization-wide operational summary.
- **Sessions** — every session, with detail, timeline and event stream.
- **Systems** — inventory and per-system detail across locations.
- **Crew** — the built-in AI assistant for working the system.
- **Knowledge** — generated playbooks, notes and references.
- **Documentation & FAQs** — full product reference.
- **Diagnostics** — clock/jitter/latency trends and incident history.

> Status: first UI pass. The interface is a faithful Vue 3 port of the design,
> running on **mock data** (`frontend/src/dock/data.ts`); a real backend/API
> will follow.

## Monorepo

| Path        | Stack                            | Purpose                  |
| ----------- | -------------------------------- | ------------------------ |
| `frontend/` | Vite + Vue 3 + TypeScript (SPA)  | The Dock console UI      |

The stack, design tokens and self-hosted fonts mirror the
[tapeforge-website](https://github.com/Uncovered-Songs/tapeforge-website) project.

## Frontend

```bash
cd frontend
pnpm install
pnpm dev          # dev server at http://localhost:5174
pnpm build        # type-check (vue-tsc) + production build to dist/
pnpm lint         # oxlint + eslint
```

### Structure

```
frontend/src/
  design/tokens.ts        # design tokens (shared with the website)
  dock/data.ts            # mock operational data (sessions, systems, …)
  dock/status.ts          # status palette + tones
  components/kit/          # design-system primitives (Card, Pill, Icon, charts…)
  components/shell/        # AppSidebar + TopBar (the app chrome)
  views/                   # one view per section, lazy-loaded via the router
  router/index.ts          # section routes
```
