/* crew.ts — data + helpers for the ambient Crew rail and command palette.
   Ported from dock-companion.jsx (SCENARIOS, suggestionsFor, seededReply,
   sectionLabel, the navigation-narration map). */
import type { Tone } from './status'
import { useDockStore } from '@/stores/dock'

/** App location, decoupled from the URL: a section + optional sub id. */
export interface DockRoute {
  section: string
  sub: string | null
}

export type NavTarget = [string, string?]

export interface Suggestion {
  t: string
  to: NavTarget
  say?: string
}

export interface ScenarioStep {
  say: string
  to: NavTarget
}

export interface Scenario {
  id: string
  icon: string
  title: string
  tone: Tone
  blurb: string
  steps: ScenarioStep[]
}

const SECTION_LABEL: Record<string, string> = {
  overview: 'Overview',
  sessions: 'Sessions',
  systems: 'Systems',
  crew: 'Crew',
  knowledge: 'Knowledge',
  docs: 'Documentation',
  diagnostics: 'Diagnostics',
}

export function sectionLabel(route: DockRoute): string {
  if (route.section === 'sessions' && route.sub) {
    const s = useDockStore().sessions.find((x) => x.id === route.sub)
    return s ? s.id : 'Session'
  }
  return SECTION_LABEL[route.section] ?? 'DOCK'
}

/** Crew's narration when IT drives navigation, keyed by `section:sub`. */
export const NARR: Record<string, string> = {
  'systems:scope-bc': 'Took you to SCOPE-Broadcast — it lost PTP lock at 18:02.',
  'sessions:S-2040': 'Opened session S-2040 — the 20:11 clock failover is on the timeline.',
  'sessions:S-2036': 'Opened the Civic rehearsal (S-2036) for comparison.',
  'diagnostics:': 'Pulled up Diagnostics — clock offset crossed the 40µs guard 3× this week.',
  'knowledge:': 'Here’s the clock topology playbook I drafted.',
  'docs:': 'Opened the PTP & clocking reference.',
  'sessions:': 'Here are all sessions — the Civic broadcast carries the open issues.',
  'systems:': 'Here’s the systems inventory — SCOPE-Broadcast is the one offline.',
}

export function narrate(section: string, sub?: string | null): string | null {
  return NARR[`${section}:${sub ?? ''}`] ?? null
}

/** Per-context suggestions Crew offers. */
export function suggestionsFor(route: DockRoute): Suggestion[] {
  const base: Record<string, Suggestion[]> = {
    overview: [
      { t: 'Investigate the SCOPE outage', to: ['systems', 'scope-bc'], say: 'SCOPE-Broadcast lost PTP lock at 18:02 — I opened it for you.' },
      { t: 'Why is PORT-Stage degraded?', to: ['diagnostics'], say: 'Pulled up Diagnostics — clock offset crossed the 40µs guard 3× this week.' },
      { t: 'Review last night’s broadcast', to: ['sessions', 'S-2040'], say: 'Here’s session S-2040 — one critical clock event, auto-recovered.' },
    ],
    diagnostics: [
      { t: 'Show the failover session', to: ['sessions', 'S-2040'], say: 'Opened S-2040 — the 20:11 failover is on the timeline.' },
      { t: 'Open the clock playbook', to: ['knowledge'], say: 'Here’s the clock topology playbook I drafted.' },
    ],
    systems: [
      { t: 'Which need a software update?', to: ['systems'], say: 'DESK-Studio-A is on v0.9.3 — one minor behind the fleet.' },
      { t: 'Read the PTP docs', to: ['docs'], say: 'Opened the PTP & clocking reference.' },
    ],
    sessions: [
      { t: 'Find sessions with clock issues', to: ['sessions'], say: '3 sessions at Riverside/Civic show clock drift — filtered for you.' },
      { t: 'Compare to the rehearsal', to: ['sessions', 'S-2036'], say: 'Opened the Civic rehearsal (S-2036) for comparison.' },
    ],
  }
  if (route.section === 'sessions' && route.sub) return base.sessions
  return base[route.section] ?? base.overview
}

/** A believable narrated reply seeded by where the user is. */
export function seededReply(route: DockRoute): string {
  const s = route.section
  if (s === 'diagnostics') return 'Clock offset and jitter co-occur on PORT-Stage — 3 failovers in 7 days, all at Riverside/Civic. Latency is nominal fleet-wide. Want me to open the worst session?'
  if (s === 'systems' && route.sub) {
    const sy = useDockStore().systems.find((x) => x.id === route.sub)
    return sy ? `${sy.name} is ${sy.status === 'ok' ? 'healthy' : sy.status === 'warn' ? 'degraded' : 'offline'} — ${sy.note}.` : ''
  }
  if (s === 'systems') return 'SCOPE-Broadcast is offline (no PTP lock since 18:02). DESK-Studio-A is one minor version behind. Everything else is healthy.'
  if (s === 'sessions' && route.sub) return 'This session had one critical clock event at 20:11 — auto-recovered in 48s, no audible dropout. Loudness held at -23 LUFS. Shall I show related sessions?'
  if (s === 'sessions') return '6 sessions this week across 4 locations. The Civic broadcast (S-2040) carries the only open issues. Want me to open it?'
  if (s === 'knowledge') return 'I’ve generated 3 of the 6 knowledge entries — the clock topology playbook is the most cited (4 refs).'
  if (s === 'docs') return 'This page was cited after last night’s failover. I can walk you through PTP grandmaster priority if useful.'
  return 'All systems nominal across 4 locations. One warning (PORT-Stage clock drift) and one critical (SCOPE-Broadcast offline) are open. Want me to take you to either?'
}

/** Guided scenarios — Crew working as the manager of Dock. */
export const SCENARIOS: Scenario[] = [
  {
    id: 'triage', icon: 'overview', title: 'Morning triage', tone: 'warn',
    blurb: 'Crew walks you through what needs attention, in priority order.',
    steps: [
      { say: 'Good morning. Two things need you today — I’ll take the critical one first.', to: ['overview'] },
      { say: 'SCOPE-Broadcast is offline — no PTP lock since 18:02. This is the critical one.', to: ['systems', 'scope-bc'] },
      { say: 'It dropped during last night’s Civic broadcast. Here’s that session — the 20:11 event.', to: ['sessions', 'S-2040'] },
      { say: 'Root cause is recurring clock drift. I drafted a playbook to prevent it.', to: ['knowledge'] },
      { say: 'That’s the priority. The second item — PORT-Stage at 61% CPU — can wait. Want me to schedule the fix before the Jun 9 Civic booking?', to: ['diagnostics'] },
    ],
  },
  {
    id: 'failover', icon: 'diagnostics', title: 'Investigate clock failover', tone: 'crit',
    blurb: 'Trace the PORT-Stage PTP failover from event to root cause.',
    steps: [
      { say: 'Let’s trace the 20:11 failover. Here it is on the session timeline.', to: ['sessions', 'S-2040'] },
      { say: 'Offset crossed the 40µs guard 3 times this week — see the trend and the threshold line.', to: ['diagnostics'] },
      { say: 'The cause: two grandmaster-capable PORT nodes at equal priority. The fix is documented here.', to: ['docs'] },
      { say: 'I can apply a fixed priority hierarchy (PORT-FOH primary). Shall I prepare the change?', to: ['systems', 'dock-stage'] },
    ],
  },
  {
    id: 'readiness', icon: 'sessions', title: 'Pre-show readiness — Riverside', tone: 'info',
    blurb: 'Crew checks the live rig before doors and flags risks.',
    steps: [
      { say: 'Riverside Arena FOH is live now. Let me run a readiness pass.', to: ['sessions', 'S-2041'] },
      { say: 'PORT-Stage is at 61% CPU with early clock drift — the one thing I’d watch tonight.', to: ['systems', 'dock-stage'] },
      { say: 'I’d set a fixed PTP priority before the next show. Here’s the procedure.', to: ['docs'] },
      { say: 'Everything else is nominal across the 4 active systems. You’re clear for doors.', to: ['overview'] },
    ],
  },
]

/** Command-palette entries: static sections + a few sessions/systems. */
export function paletteItems(): { label: string; hint?: string; to: NavTarget; icon: string }[] {
  const { sessions, systems } = useDockStore()
  return [
    { label: 'Overview', to: ['overview'], icon: 'overview' },
    { label: 'Sessions', to: ['sessions'], icon: 'sessions' },
    { label: 'Systems', to: ['systems'], icon: 'systems' },
    { label: 'Crew workspace', to: ['crew'], icon: 'crew' },
    { label: 'Knowledge', to: ['knowledge'], icon: 'knowledge' },
    { label: 'Documentation', to: ['docs'], icon: 'docs' },
    { label: 'Diagnostics', to: ['diagnostics'], icon: 'diagnostics' },
    ...sessions.slice(0, 4).map((s) => ({ label: s.name, hint: s.id, to: ['sessions', s.id] as NavTarget, icon: 'sessions' })),
    ...systems.slice(0, 4).map((s) => ({ label: s.name, hint: s.loc, to: ['systems', s.id] as NavTarget, icon: 'systems' })),
  ]
}
