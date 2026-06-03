<script setup lang="ts">
import { computed, type CSSProperties } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { L, TWO } from '@/design/tokens'
import { useBreakpoint } from '@/composables/useBreakpoint'
import { S, TONE, type Tone } from '@/dock/status'
import { type DockSession, type DockSystem, type DockEvent } from '@/dock/data'
import { useDockStore } from '@/stores/dock'
import Pill from '@/components/kit/Pill.vue'
import DockDot from '@/components/kit/DockDot.vue'
import Icon from '@/components/kit/Icon.vue'
import SecLabel from '@/components/kit/SecLabel.vue'
import Btn from '@/components/kit/Btn.vue'

const route = useRoute()
const router = useRouter()
const { isMobile, isCompact } = useBreakpoint()
const { sessions, systems, eventStream, configChanges } = useDockStore()

const STATUS_TONE: Record<DockSession['status'], Tone> = { live: 'crit', review: 'warn', done: 'idle' }
const STATUS_LABEL: Record<DockSession['status'], string> = { live: 'LIVE', review: 'IN REVIEW', done: 'COMPLETE' }

const id = computed(() => String(route.params.id))
const s = computed<DockSession | undefined>(() => sessions.find((x) => x.id === id.value))

const sys = computed<DockSystem[]>(() =>
  s.value
    ? (s.value.systems.map((sid) => systems.find((x) => x.id === sid)).filter(Boolean) as DockSystem[])
    : [],
)

const relatedSessions = computed<DockSession[]>(() => {
  const cur = s.value
  if (!cur) return []
  return sessions
    .filter((x) => x.loc === cur.loc && x.id !== cur.id)
    .concat(sessions.filter((x) => x.type === cur.type && x.loc !== cur.loc))
    .slice(0, 3)
})

const crewInsights: Array<[Tone, string, string]> = [
  ['crit', 'Clock failover is the dominant risk', 'The 20:11 PTP failover matches a pattern seen in 3 recent Riverside/Civic sessions. Root cause: equal grandmaster priority.'],
  ['ok', 'Recovery was clean', 'No audio dropout detected; SCOPE loudness stayed within ±0.4 LU of target across the failover window.'],
  ['info', 'Suggested follow-up', 'Apply a fixed PTP priority hierarchy before the next Civic Theatre booking (Jun 9).'],
]

const relatedDocs: Array<[string, string]> = [
  ['PTP & clocking', 'docs'],
  ['AES67 setup', 'docs'],
  ['Troubleshooting jitter', 'docs'],
]

const postmortem: Array<[string, string]> = [
  ['What happened', 'At 20:11:14 the PTP grandmaster offset on PORT-Stage exceeded the 40µs guard threshold following a 0.9ms jitter spike on stream 12. CORE initiated automatic failover to grandmaster B.'],
  ['Impact', 'Clock domain re-locked in 48 seconds. No audio dropout or loudness deviation beyond ±0.4 LU. One configuration auto-change (buffer 64 → 128). Broadcast unaffected.'],
  ['Resolution & follow-up', 'Auto-recovered. Recommended: set a fixed PTP priority hierarchy (PORT-FOH primary). Crew drafted a clock topology playbook; assign before Jun 9 Civic booking.'],
]

// ── Topology mini-diagram geometry ──
const W = 520
const H = 230
const cx = W / 2
const cy = H / 2

interface TopoNode {
  s: DockSystem
  x: number
  y: number
}

const topo = computed<TopoNode[]>(() => {
  const list = sys.value
  const core = list.find((x) => x.kind === 'core') ?? list[0]
  const sats = list.filter((x) => x !== core)
  return sats.map((node, i) => {
    const a = ((-90 + (360 / sats.length) * i) * Math.PI) / 180
    return { s: node, x: cx + Math.cos(a) * 150, y: cy + Math.sin(a) * 78 }
  })
})

function wireStroke(status: Tone): string {
  return status === 'crit' ? S.crit : status === 'warn' ? S.warn : L.wire
}

// ── Timeline geometry ──
function toMin(t: string): number {
  const [h, m] = t.split(':')
  return +h * 60 + +m
}

interface TimelinePoint {
  e: DockEvent
  x: number
  y: number
}

const LANES: Record<Tone, number> = { info: 0, ok: 1, warn: 2, crit: 2, idle: 0, accent: 0 }

const timeline = computed(() => {
  const events = eventStream
  const t0 = toMin(events[0].t)
  const t1 = toMin(events[events.length - 1].t)
  const span = t1 - t0 || 1
  const points: TimelinePoint[] = events.map((e) => {
    const x = ((toMin(e.t) - t0) / span) * 100
    const lane = LANES[e.tone]
    const y = 6 + lane * 20
    return { e, x, y }
  })
  const ticks = [0, 0.25, 0.5, 0.75, 1].map((f) => ({
    f,
    label: events[Math.round(f * (events.length - 1))].t.slice(0, 5),
  }))
  return { points, ticks }
})

const timelineLegend: Array<[Tone, string]> = [
  ['info', 'info'],
  ['ok', 'ok'],
  ['warn', 'warn/crit'],
]

const page = computed<CSSProperties>(() => ({
  padding: isMobile.value ? '18px 14px' : '24px 28px',
  maxWidth: '1320px',
  margin: '0 auto',
}))
const grid = computed<CSSProperties>(() => ({
  display: 'grid',
  gridTemplateColumns: isCompact.value ? '1fr' : '1fr 1fr 1fr',
  gap: '16px',
  alignItems: 'start',
}))

function panelStyle(span?: number): CSSProperties {
  return {
    // On a single-column (compact) grid there is no column 3 to span, so collapse to auto.
    gridColumn: span && !isCompact.value ? `span ${span}` : 'auto',
    background: L.panel,
    border: `1px solid ${L.border}`,
    borderRadius: '12px',
    boxShadow: '0 1px 2px rgba(16,24,40,0.04)',
    display: 'flex',
    flexDirection: 'column',
  }
}
const panelHead: CSSProperties = {
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'space-between',
  padding: '12px 16px',
  borderBottom: `1px solid ${L.border}`,
}
const panelTitle: CSSProperties = { fontFamily: L.body, fontSize: '13px', fontWeight: 700, color: L.text }
const panelBody: CSSProperties = { padding: '16px', flex: 1 }
// Header: row on desktop, stacked (title above actions) on mobile so the action buttons don't squeeze.
const headerRow = computed<CSSProperties>(() => ({
  display: 'flex',
  alignItems: isMobile.value ? 'stretch' : 'flex-start',
  flexDirection: isMobile.value ? 'column' : 'row',
  justifyContent: 'space-between',
  gap: isMobile.value ? '14px' : '20px',
  marginBottom: '20px',
}))
// Postmortem "What/Impact/Resolution" columns stack on compact.
const postmortemGrid = computed<CSSProperties>(() => ({
  display: 'grid',
  gridTemplateColumns: isCompact.value ? '1fr' : '1fr 1fr 1fr',
  gap: isCompact.value ? '16px' : '18px',
}))
</script>

<template>
  <div v-if="!s" :style="page">
    <p :style="{ fontFamily: L.body, fontSize: '14px', color: L.text2 }">
      Session <span :style="{ fontFamily: L.mono }">{{ id }}</span> not found.
      <span :style="{ color: S.accentText, cursor: 'pointer', fontWeight: 600 }" @click="router.push('/sessions')">Back to sessions</span>
    </p>
  </div>

  <div v-else :style="page">
    <!-- header -->
    <div :style="headerRow">
      <div>
        <div :style="{ display: 'flex', alignItems: 'center', gap: '11px', marginBottom: '8px' }">
          <Pill :tone="STATUS_TONE[s.status]">{{ STATUS_LABEL[s.status] }}</Pill>
          <span :style="{ fontFamily: L.mono, fontSize: '11px', color: L.text3 }">{{ s.id }}</span>
        </div>
        <h1 :style="{ margin: 0, fontFamily: L.body, fontSize: '24px', fontWeight: 700, letterSpacing: '-0.02em', color: L.text }">{{ s.name }}</h1>
        <div :style="{ display: 'flex', flexWrap: 'wrap', gap: '6px 16px', marginTop: '9px', fontFamily: L.mono, fontSize: '11px', color: L.text2 }">
          <span>{{ s.type }}</span><span>· {{ s.loc }}</span><span>· {{ s.date }} {{ s.start }}</span><span>· {{ s.dur === 'live' ? 'in progress' : s.dur }}</span><span>· {{ s.engineer }}</span>
        </div>
      </div>
      <div :style="{ display: 'flex', gap: '9px' }">
        <Btn icon="spark" sm @click="router.push('/crew')">Ask Crew</Btn>
        <Btn icon="ext" sm>Export</Btn>
      </div>
    </div>

    <!-- generated summary banner -->
    <div :style="{ display: 'flex', gap: '12px', padding: '15px 18px', background: S.accentBg, border: `1px solid ${S.accentBorder}`, borderRadius: '12px', marginBottom: '16px' }">
      <span :style="{ color: S.accentText, marginTop: '1px' }"><Icon name="spark" :size="17" fill="cur" /></span>
      <div>
        <div :style="{ fontFamily: L.mono, fontSize: '9.5px', letterSpacing: '0.12em', color: S.accentText, marginBottom: '5px' }">CREW · GENERATED SUMMARY</div>
        <p :style="{ margin: 0, fontFamily: L.body, fontSize: '13.5px', lineHeight: 1.55, color: L.text }">
          3h 12m broadcast across 2 systems. One <b>critical clock event</b> at 20:11 — PTP grandmaster failover on PORT-Stage, auto-recovered in 48s with no audible dropout. Loudness held at -23 LUFS throughout. Archive verified (318 GB). <b>5 events flagged</b>; recurring clock drift recommended for follow-up.
        </p>
      </div>
    </div>

    <!-- grid -->
    <div :style="grid">
      <!-- timeline — full width -->
      <div :style="panelStyle(3)">
        <div :style="panelHead">
          <span :style="panelTitle">Session timeline</span>
          <SecLabel>19:00 – 22:13</SecLabel>
        </div>
        <div :style="panelBody">
          <div :style="{ position: 'relative', height: '92px' }">
            <!-- axis -->
            <div :style="{ position: 'absolute', left: 0, right: 0, top: '70px', height: '1px', background: L.border }" />
            <div
              v-for="(tk, i) in timeline.ticks"
              :key="i"
              :style="{ position: 'absolute', top: '74px', left: `${tk.f * 100}%`, transform: 'translateX(-50%)', fontFamily: L.mono, fontSize: '9px', color: L.text3 }"
            >{{ tk.label }}</div>
            <div
              v-for="(p, i) in timeline.points"
              :key="i"
              :title="`${p.e.t} ${p.e.src}: ${p.e.msg}`"
              :style="{ position: 'absolute', left: `${p.x}%`, top: `${p.y}px`, transform: 'translateX(-50%)' }"
            >
              <div :style="{ width: (p.e.tone === 'crit' ? 11 : 9) + 'px', height: (p.e.tone === 'crit' ? 11 : 9) + 'px', borderRadius: '3px', background: TONE[p.e.tone], border: '2px solid #fff', boxShadow: p.e.tone === 'crit' ? `0 0 0 3px ${S.crit}22` : 'none' }" />
              <div v-if="i > 0" :style="{ position: 'absolute', left: '4px', top: '11px', width: '1px', height: `${70 - p.y}px`, background: L.border }" />
            </div>
            <div :style="{ position: 'absolute', right: 0, top: 0, display: 'flex', gap: '10px' }">
              <span
                v-for="l in timelineLegend"
                :key="l[0]"
                :style="{ display: 'flex', alignItems: 'center', gap: '5px', fontFamily: L.mono, fontSize: '9px', color: L.text3 }"
              ><DockDot :tone="l[0]" :size="6" />{{ l[1] }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- topology -->
      <div :style="panelStyle()">
        <div :style="panelHead">
          <span :style="panelTitle">Topology snapshot</span>
          <SecLabel>20:11 · auto</SecLabel>
        </div>
        <div :style="panelBody">
          <svg :viewBox="`0 0 ${W} ${H}`" width="100%" :style="{ display: 'block', maxWidth: '520px', margin: '0 auto' }">
            <line
              v-for="(p, i) in topo"
              :key="`l${i}`"
              :x1="cx" :y1="cy" :x2="p.x" :y2="p.y"
              :stroke="wireStroke(p.s.status)"
              :stroke-width="p.s.status === 'ok' ? 1.2 : 1.6"
              :stroke-dasharray="p.s.status === 'crit' ? '3 3' : 'none'"
            />
            <g v-for="(p, i) in topo" :key="`g${i}`">
              <circle :cx="p.x" :cy="p.y" r="20" :fill="L.panel" :stroke="p.s.status === 'crit' ? S.crit : p.s.status === 'warn' ? S.warn : L.border2" stroke-width="1.2" />
              <text :x="p.x" :y="p.y + 3" text-anchor="middle" :font-family="L.mono" font-size="9" font-weight="600" :fill="S.accentText">{{ TWO[p.s.kind] }}</text>
              <text :x="p.x" :y="p.y + 33" text-anchor="middle" :font-family="L.mono" font-size="8" :fill="L.text3">{{ p.s.name.replace(/^[A-Z]+-/, '') }}</text>
            </g>
            <circle :cx="cx" :cy="cy" r="27" :fill="S.accentBg" :stroke="S.accent" stroke-width="1.4" />
            <text :x="cx" :y="cy - 1" text-anchor="middle" :font-family="L.mono" font-size="11" font-weight="600" :fill="S.accentText">CORE</text>
            <text :x="cx" :y="cy + 11" text-anchor="middle" :font-family="L.mono" font-size="7" :fill="S.accentText">resolver</text>
          </svg>
          <div :style="{ display: 'flex', gap: '7px', marginTop: '8px', flexWrap: 'wrap' }">
            <Pill v-for="sy in sys" :key="sy.id" :tone="sy.status">{{ sy.name }}</Pill>
          </div>
        </div>
      </div>

      <!-- event stream -->
      <div :style="panelStyle()">
        <div :style="panelHead">
          <span :style="panelTitle">Event stream</span>
          <SecLabel>{{ s.events }} total</SecLabel>
        </div>
        <div :style="panelBody">
          <div :style="{ maxHeight: '248px', overflowY: 'auto', margin: '-4px 0' }">
            <div
              v-for="(e, i) in eventStream"
              :key="i"
              :style="{ display: 'flex', gap: '9px', padding: '7px 0', borderTop: i ? `1px solid ${L.border}` : 'none' }"
            >
              <span :style="{ marginTop: '4px' }"><DockDot :tone="e.tone" :size="6" /></span>
              <div :style="{ minWidth: 0 }">
                <div :style="{ fontFamily: L.mono, fontSize: '9.5px', color: L.text3 }">{{ e.t }} · {{ e.src }}</div>
                <div :style="{ fontFamily: L.body, fontSize: '12px', color: L.text2, lineHeight: 1.4, marginTop: '1px' }">{{ e.msg }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- config changes -->
      <div :style="panelStyle()">
        <div :style="panelHead">
          <span :style="panelTitle">Configuration changes</span>
          <SecLabel>{{ configChanges.length }}</SecLabel>
        </div>
        <div :style="panelBody">
          <div
            v-for="(c, i) in configChanges"
            :key="i"
            :style="{ padding: '9px 0', borderTop: i ? `1px solid ${L.border}` : 'none' }"
          >
            <div :style="{ display: 'flex', justifyContent: 'space-between', gap: '8px' }">
              <span :style="{ fontFamily: L.body, fontSize: '12.5px', fontWeight: 600, color: L.text }">{{ c.what }}</span>
              <span :style="{ fontFamily: L.mono, fontSize: '10px', color: L.text3, flex: '0 0 auto' }">{{ c.t }}</span>
            </div>
            <div :style="{ display: 'flex', alignItems: 'center', gap: '7px', marginTop: '4px', fontFamily: L.mono, fontSize: '10.5px' }">
              <span :style="{ color: L.text3, textDecoration: 'line-through' }">{{ c.from }}</span>
              <span :style="{ color: L.text3, display: 'flex' }"><Icon name="arrowR" :size="11" /></span>
              <span :style="{ color: S.accentText, fontWeight: 600 }">{{ c.to }}</span>
              <span :style="{ marginLeft: 'auto', color: L.text3 }">{{ c.who }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- crew insights -->
      <div :style="{ background: L.panel, border: `1px solid ${S.accentBorder}`, borderRadius: '12px', boxShadow: '0 1px 2px rgba(16,24,40,0.04)', display: 'flex', flexDirection: 'column' }">
        <div :style="{ display: 'flex', alignItems: 'center', gap: '8px', padding: '12px 16px', borderBottom: `1px solid ${L.border}`, background: S.accentBg, borderRadius: '12px 12px 0 0' }">
          <span :style="{ color: S.accentText, display: 'flex' }"><Icon name="spark" :size="15" fill="cur" /></span>
          <span :style="{ fontFamily: L.body, fontSize: '13px', fontWeight: 700, color: L.text }">Crew insights</span>
          <span :style="{ marginLeft: 'auto', fontFamily: L.mono, fontSize: '8.5px', fontWeight: 600, color: S.accentText, border: `1px solid ${S.accentBorder}`, borderRadius: '4px', padding: '1px 5px' }">3 AGENTS</span>
        </div>
        <div :style="{ padding: '16px' }">
          <div
            v-for="(r, i) in crewInsights"
            :key="i"
            :style="{ display: 'flex', gap: '9px', padding: '8px 0', borderTop: i ? `1px solid ${L.border}` : 'none' }"
          >
            <span :style="{ marginTop: '3px' }"><DockDot :tone="r[0]" /></span>
            <div>
              <div :style="{ fontFamily: L.body, fontSize: '12.5px', fontWeight: 600, color: L.text }">{{ r[1] }}</div>
              <div :style="{ fontFamily: L.body, fontSize: '11.5px', color: L.text2, lineHeight: 1.45, marginTop: '2px' }">{{ r[2] }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- related docs -->
      <div :style="panelStyle()">
        <div :style="panelHead">
          <span :style="panelTitle">Related documentation</span>
        </div>
        <div :style="panelBody">
          <div
            v-for="(d, i) in relatedDocs"
            :key="i"
            :style="{ display: 'flex', alignItems: 'center', gap: '9px', padding: '9px 0', borderTop: i ? `1px solid ${L.border}` : 'none', cursor: 'pointer' }"
            @click="router.push('/docs')"
          >
            <span :style="{ color: L.text3, display: 'flex' }"><Icon name="docs" :size="14" /></span>
            <span :style="{ fontFamily: L.body, fontSize: '12.5px', color: L.text2, flex: 1 }">{{ d[0] }}</span>
            <span :style="{ color: L.text3, display: 'flex' }"><Icon name="arrowR" :size="12" /></span>
          </div>
        </div>
      </div>

      <!-- related sessions -->
      <div :style="panelStyle()">
        <div :style="panelHead">
          <span :style="panelTitle">Related sessions</span>
        </div>
        <div :style="panelBody">
          <div
            v-for="(r, i) in relatedSessions"
            :key="r.id"
            :style="{ display: 'flex', alignItems: 'center', gap: '9px', padding: '9px 0', borderTop: i ? `1px solid ${L.border}` : 'none', cursor: 'pointer' }"
            @click="router.push(`/sessions/${r.id}`)"
          >
            <DockDot :tone="STATUS_TONE[r.status]" />
            <div :style="{ flex: 1, minWidth: 0 }">
              <div :style="{ fontFamily: L.body, fontSize: '12.5px', fontWeight: 600, color: L.text, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }">{{ r.name }}</div>
              <div :style="{ fontFamily: L.mono, fontSize: '9.5px', color: L.text3 }">{{ r.date }} · {{ r.issues }} issues</div>
            </div>
            <span :style="{ color: L.text3, display: 'flex' }"><Icon name="arrowR" :size="12" /></span>
          </div>
        </div>
      </div>

      <!-- postmortem — full width -->
      <div :style="panelStyle(3)">
        <div :style="panelHead">
          <span :style="panelTitle">Postmortem analysis</span>
          <Pill tone="warn">1 action item</Pill>
        </div>
        <div :style="panelBody">
          <div :style="postmortemGrid">
            <div v-for="(c, i) in postmortem" :key="i">
              <SecLabel :style="{ marginBottom: '8px' }">{{ c[0] }}</SecLabel>
              <p :style="{ margin: 0, fontFamily: L.body, fontSize: '12.5px', lineHeight: 1.55, color: L.text2 }">{{ c[1] }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
