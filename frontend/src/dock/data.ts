/* data.ts — shared TypeScript types for the Dock domain.
   The data itself now comes from the backend API (see api.ts + stores/dock.ts);
   this module only defines the shapes. */
import type { Tone } from './status'

export interface DockSystem {
  id: string
  kind: string
  name: string
  loc: string
  ver: string
  status: Tone
  uptime: string
  cpu: number
  sessions: number
  note: string
}

export interface DockSession {
  id: string
  name: string
  type: string
  loc: string
  date: string
  start: string
  dur: string
  status: 'live' | 'review' | 'done'
  systems: string[]
  events: number
  issues: number
  engineer: string
}

export interface DockEvent {
  t: string
  tone: Tone
  src: string
  msg: string
}

export interface ConfigChange {
  t: string
  who: string
  what: string
  from: string
  to: string
}

export interface CrewRec {
  tone: Tone
  title: string
  body: string
  action: string
}

export interface KnowledgeItem {
  id: string
  kind: string
  title: string
  tags: string[]
  by: string
  updated: string
  cites: number
}

export interface DocGroup {
  group: string
  items: string[]
}

export interface CrewCite {
  t: string
  to: string
}

export interface CrewTurn {
  role: 'user' | 'crew'
  text: string
  cites?: CrewCite[]
  agents?: string[]
}

export interface Incident {
  tone: Tone
  sys: string
  issue: string
  when: string
  dur: string
}

export interface Diagnostics {
  clockOffset: number[]
  jitter: number[]
  latency: number[]
  packetLoss: number[]
  incidents: Incident[]
}

/** The full payload returned by the backend's `GET /bootstrap`. */
export interface DockBootstrap {
  systems: DockSystem[]
  sessions: DockSession[]
  eventStream: DockEvent[]
  configChanges: ConfigChange[]
  crewRecs: CrewRec[]
  knowledge: KnowledgeItem[]
  docTree: DocGroup[]
  crewThread: CrewTurn[]
  diagnostics: Diagnostics
}
