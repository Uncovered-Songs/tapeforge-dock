<script setup lang="ts">
import { computed, type CSSProperties } from 'vue'
import { useRouter } from 'vue-router'
import { L } from '@/design/tokens'
import { S, TONE, type Tone } from '@/dock/status'
import { diagnostics } from '@/dock/data'
import DCard from '@/components/kit/DCard.vue'
import Pill from '@/components/kit/Pill.vue'
import DockDot from '@/components/kit/DockDot.vue'
import Icon from '@/components/kit/Icon.vue'
import SecLabel from '@/components/kit/SecLabel.vue'
import PageHead from '@/components/kit/PageHead.vue'
import Btn from '@/components/kit/Btn.vue'

const router = useRouter()
const dg = diagnostics

/* summary tiles: [label, value, tone] */
const tiles: Array<[string, string, Tone]> = [
  ['Incidents · 7d', '4', 'warn'],
  ['Clock failovers', '3', 'warn'],
  ['Avg latency', '2.1 ms', 'ok'],
  ['Mean recovery', '38 s', 'info'],
]

/* trend charts: [title, data, unit, threshold|null, thLabel|null, tone] */
interface TrendCfg {
  title: string
  data: number[]
  unit: string
  threshold: number | null
  thLabel: string | null
  tone: Tone
}
const trends: TrendCfg[] = [
  { title: 'PTP clock offset', data: dg.clockOffset, unit: 'µs', threshold: 40, thLabel: '40µs guard', tone: 'warn' },
  { title: 'Network jitter', data: dg.jitter, unit: 'ms', threshold: 0.8, thLabel: '0.8ms', tone: 'warn' },
  { title: 'Transport latency', data: dg.latency, unit: 'ms', threshold: null, thLabel: null, tone: 'ok' },
  { title: 'Packet loss', data: dg.packetLoss, unit: '%', threshold: 0.05, thLabel: '0.05%', tone: 'info' },
]

/* ── Trend chart geometry (inline SVG line chart with threshold band) ── */
const TW = 540
const TH = 120
const TLABELS = ['18:00', '19:00', '20:00', '21:00', '22:00']

interface TrendGeom {
  line: string
  area: string
  thY: number | null
  lastX: number
  lastY: number
  hits: Array<{ x: number; y: number }>
  color: string
}

function trendGeom(t: TrendCfg): TrendGeom {
  const data = t.data
  const max = Math.max(...data, t.threshold ?? 0) * 1.15
  const min = 0
  const rng = max - min || 1
  const X = (i: number): number => (i / (data.length - 1)) * TW
  const Y = (v: number): number => TH - 6 - ((v - min) / rng) * (TH - 14)
  const line = data.map((v, i) => `${i ? 'L' : 'M'}${X(i).toFixed(1)} ${Y(v).toFixed(1)}`).join(' ')
  const area = `${line} L${TW} ${TH} L0 ${TH} Z`
  const hits: Array<{ x: number; y: number }> = []
  if (t.threshold != null) {
    data.forEach((v, i) => {
      if (v >= (t.threshold as number)) hits.push({ x: X(i), y: Y(v) })
    })
  }
  return {
    line,
    area,
    thY: t.threshold != null ? Y(t.threshold) : null,
    lastX: X(data.length - 1),
    lastY: Y(data[data.length - 1]),
    hits,
    color: TONE[t.tone],
  }
}

function labelX(i: number): number {
  return (i / (TLABELS.length - 1)) * TW
}
function labelAnchor(i: number): string {
  return i === 0 ? 'start' : i === TLABELS.length - 1 ? 'end' : 'middle'
}

function trendNow(t: TrendCfg): string {
  return `${t.data[t.data.length - 1]}${t.unit} now`
}

function incidentLabel(tone: Tone): string {
  return tone === 'crit' ? 'CRITICAL' : tone === 'warn' ? 'WARNING' : 'INFO'
}

const page: CSSProperties = { padding: '26px 28px', maxWidth: '1280px', margin: '0 auto' }
const tile: CSSProperties = {
  flex: 1,
  padding: '14px 16px',
  background: L.panel,
  border: `1px solid ${L.border}`,
  borderRadius: '12px',
  boxShadow: '0 1px 2px rgba(16,24,40,0.04)',
}
const grid: CSSProperties = { display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginBottom: '16px' }
const trendNowStyle: CSSProperties = { fontFamily: L.mono, fontSize: '11px', color: L.text2 }
const ROWGRID = '90px 1fr 1fr 120px 90px'
const headerRow: CSSProperties = {
  display: 'grid',
  gridTemplateColumns: ROWGRID,
  gap: '12px',
  padding: '10px 18px',
  borderBottom: `1px solid ${L.border}`,
  background: '#FCFCFD',
}
const crewBox: CSSProperties = {
  display: 'flex',
  gap: '12px',
  padding: '15px 18px',
  background: S.accentBg,
  border: `1px solid ${S.accentBorder}`,
  borderRadius: '12px',
  marginTop: '16px',
}

const trendGeoms = computed(() => trends.map((t) => trendGeom(t)))
</script>

<template>
  <div :style="page">
    <PageHead title="Diagnostics" sub="Historical trend analysis across the fleet — not realtime monitoring">
      <template #right>
        <div :style="{ display: 'flex', gap: '9px' }">
          <Btn icon="filter" sm>Last 6h</Btn>
          <Btn icon="spark" sm primary @click="router.push('/crew')">Analyze with Crew</Btn>
        </div>
      </template>
    </PageHead>

    <!-- summary tiles -->
    <div :style="{ display: 'flex', gap: '14px', marginBottom: '16px' }">
      <div v-for="t in tiles" :key="t[0]" :style="tile">
        <div :style="{ display: 'flex', alignItems: 'center', gap: '7px', marginBottom: '10px' }">
          <DockDot :tone="t[2]" />
          <SecLabel>{{ t[0] }}</SecLabel>
        </div>
        <div :style="{ fontFamily: L.body, fontSize: '24px', fontWeight: 700, color: L.text }">{{ t[1] }}</div>
      </div>
    </div>

    <!-- trend charts -->
    <div :style="grid">
      <DCard v-for="(t, ti) in trends" :key="t.title" :title="t.title">
        <template #action><span :style="trendNowStyle">{{ trendNow(t) }}</span></template>
        <svg
          :viewBox="`0 0 ${TW} ${TH + 16}`"
          width="100%"
          :style="{ display: 'block', overflow: 'visible' }"
        >
          <g v-if="trendGeoms[ti].thY != null">
            <line
              x1="0"
              :y1="trendGeoms[ti].thY ?? 0"
              :x2="TW"
              :y2="trendGeoms[ti].thY ?? 0"
              :stroke="S.crit"
              stroke-width="1"
              stroke-dasharray="4 4"
              opacity="0.6"
            />
            <text
              :x="TW"
              :y="(trendGeoms[ti].thY ?? 0) - 4"
              text-anchor="end"
              :font-family="L.mono"
              font-size="8.5"
              :fill="S.crit"
            >{{ t.thLabel }}</text>
          </g>
          <path :d="trendGeoms[ti].area" :fill="trendGeoms[ti].color" opacity="0.07" />
          <path
            :d="trendGeoms[ti].line"
            fill="none"
            :stroke="trendGeoms[ti].color"
            stroke-width="1.6"
            stroke-linejoin="round"
            stroke-linecap="round"
          />
          <circle
            v-for="(hit, hi) in trendGeoms[ti].hits"
            :key="hi"
            :cx="hit.x"
            :cy="hit.y"
            r="3"
            :fill="S.crit"
          />
          <circle :cx="trendGeoms[ti].lastX" :cy="trendGeoms[ti].lastY" r="2.5" :fill="trendGeoms[ti].color" />
          <text
            v-for="(l, li) in TLABELS"
            :key="l"
            :x="labelX(li)"
            :y="TH + 13"
            :text-anchor="labelAnchor(li)"
            :font-family="L.mono"
            font-size="8.5"
            :fill="L.text3"
          >{{ l }}</text>
        </svg>
      </DCard>
    </div>

    <!-- incident log -->
    <DCard title="Incident history" :pad="0">
      <template #action><SecLabel>last 7 days</SecLabel></template>
      <div :style="headerRow">
        <SecLabel v-for="h in ['Severity', 'System', 'Issue', 'When', 'Duration']" :key="h">{{ h }}</SecLabel>
      </div>
      <div
        v-for="(it, i) in dg.incidents"
        :key="i"
        :style="{
          display: 'grid',
          gridTemplateColumns: ROWGRID,
          gap: '12px',
          alignItems: 'center',
          padding: '12px 18px',
          borderTop: i ? `1px solid ${L.border}` : 'none',
        }"
      >
        <Pill :tone="it.tone">{{ incidentLabel(it.tone) }}</Pill>
        <span :style="{ fontFamily: L.mono, fontSize: '12px', fontWeight: 600, color: L.text }">{{ it.sys }}</span>
        <span :style="{ fontFamily: L.body, fontSize: '12.5px', color: L.text2 }">{{ it.issue }}</span>
        <span :style="{ fontFamily: L.mono, fontSize: '11px', color: L.text3 }">{{ it.when }}</span>
        <span :style="{ fontFamily: L.mono, fontSize: '11px', color: it.dur === 'ongoing' ? S.crit : L.text2 }">{{ it.dur }}</span>
      </div>
    </DCard>

    <!-- crew analysis -->
    <div :style="crewBox">
      <Icon name="spark" :size="17" fill="cur" :style="{ color: S.accentText, marginTop: '1px' }" />
      <div :style="{ flex: 1 }">
        <div :style="{ fontFamily: L.mono, fontSize: '9.5px', letterSpacing: '0.12em', color: S.accentText, marginBottom: '5px' }">CREW · TREND ANALYSIS</div>
        <p :style="{ margin: 0, fontFamily: L.body, fontSize: '13.5px', lineHeight: 1.55, color: L.text }">
          Clock offset and jitter spikes <b>co-occur on PORT-Stage</b> and correlate with grandmaster failover events (3 in 7 days, all at Riverside/Civic). Latency and packet loss remain nominal fleet-wide. Recommended fix: fixed PTP priority hierarchy — projected to eliminate ~90% of these incidents.
        </p>
        <div :style="{ marginTop: '10px' }"><Btn sm @click="router.push('/knowledge')">View playbook</Btn></div>
      </div>
    </div>
  </div>
</template>
