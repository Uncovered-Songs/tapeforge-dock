<script setup lang="ts">
import { computed, ref, type CSSProperties } from 'vue'
import { useRouter } from 'vue-router'
import { L } from '@/design/tokens'
import { useBreakpoint } from '@/composables/useBreakpoint'
import { S, type Tone } from '@/dock/status'
import { sessions, systems, type DockSession } from '@/dock/data'
import DCard from '@/components/kit/DCard.vue'
import Pill from '@/components/kit/Pill.vue'
import DockDot from '@/components/kit/DockDot.vue'
import Badge from '@/components/kit/Badge.vue'
import SecLabel from '@/components/kit/SecLabel.vue'
import PageHead from '@/components/kit/PageHead.vue'
import Btn from '@/components/kit/Btn.vue'

const router = useRouter()
const { isMobile, isCompact } = useBreakpoint()

const STATUS_TONE: Record<DockSession['status'], Tone> = { live: 'crit', review: 'warn', done: 'idle' }
const STATUS_LABEL: Record<DockSession['status'], string> = { live: 'LIVE', review: 'IN REVIEW', done: 'COMPLETE' }

const types = ['All', 'Live Sound', 'Studio', 'Broadcast', 'Rehearsal']
const filter = ref('All')
const rows = computed(() => sessions.filter((s) => filter.value === 'All' || s.type === filter.value))

function systemOf(id: string) {
  return systems.find((x) => x.id === id)
}

// Desktop: full table. Tablet: drop Duration column (least essential — live rows show "—").
const COLS_DESKTOP = '1.7fr 1fr 0.9fr 0.7fr 0.7fr 110px'
const COLS_TABLET = '1.7fr 1fr 0.9fr 0.7fr 104px'
const cols = computed(() => (isCompact.value ? COLS_TABLET : COLS_DESKTOP))
// Header labels mirror the active column set (Duration hidden on tablet).
const headers = computed(() =>
  isCompact.value
    ? ['Session', 'Location', 'Date', 'Events', 'Status']
    : ['Session', 'Location', 'Date', 'Duration', 'Events', 'Status'],
)

const page = computed<CSSProperties>(() => ({
  padding: isMobile.value ? '18px 14px' : '26px 28px',
  maxWidth: '1280px',
  margin: '0 auto',
}))
const headerRow = computed<CSSProperties>(() => ({
  display: 'grid',
  gridTemplateColumns: cols.value,
  gap: '12px',
  padding: '10px 18px',
  borderBottom: `1px solid ${L.border}`,
  background: '#FCFCFD',
}))
const tabRow = computed<CSSProperties>(() => ({
  display: 'flex',
  gap: '7px',
  marginBottom: '16px',
  // Let filter tabs scroll horizontally on mobile instead of overflowing/wrapping awkwardly.
  overflowX: isMobile.value ? 'auto' : 'visible',
  flexWrap: isMobile.value ? 'nowrap' : 'wrap',
  paddingBottom: isMobile.value ? '4px' : '0',
}))

function tabStyle(t: string): CSSProperties {
  const on = filter.value === t
  return {
    fontFamily: L.body,
    fontSize: '12.5px',
    fontWeight: 600,
    cursor: 'pointer',
    whiteSpace: 'nowrap',
    flex: '0 0 auto',
    padding: '6px 13px',
    borderRadius: '8px',
    border: `1px solid ${on ? S.accent : L.border}`,
    background: on ? S.accentBg : L.panel,
    color: on ? S.accentText : L.text2,
  }
}
</script>

<template>
  <div :style="page">
    <PageHead title="Sessions" sub="Every show, recording, rehearsal and deployment — captured as a session">
      <template #right>
        <Btn icon="plus" sm primary>New session</Btn>
      </template>
    </PageHead>

    <div :style="tabRow">
      <button v-for="t in types" :key="t" :style="tabStyle(t)" @click="filter = t">{{ t }}</button>
    </div>

    <!-- mobile: stacked cards (table doesn't fit) -->
    <div v-if="isMobile" :style="{ display: 'flex', flexDirection: 'column', gap: '10px' }">
      <DCard
        v-for="s in rows"
        :key="s.id"
        :pad="0"
        clickable
        @click="router.push(`/sessions/${s.id}`)"
      >
        <div :style="{ display: 'flex', alignItems: 'center', gap: '11px', padding: '13px 14px' }">
          <DockDot v-if="s.status === 'live'" tone="crit" pulse />
          <Badge v-else :id="systemOf(s.systems[0])?.kind ?? 'core'" :size="24" />
          <div :style="{ minWidth: 0, flex: 1 }">
            <div :style="{ fontFamily: L.body, fontSize: '13.5px', fontWeight: 700, color: L.text, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }">{{ s.name }}</div>
            <div :style="{ fontFamily: L.mono, fontSize: '10px', color: L.text3, marginTop: '2px' }">{{ s.id }} · {{ s.type }}</div>
          </div>
          <Pill :tone="STATUS_TONE[s.status]">{{ STATUS_LABEL[s.status] }}</Pill>
        </div>
        <div :style="{ display: 'flex', flexWrap: 'wrap', gap: '6px 16px', padding: '0 14px 13px', fontFamily: L.mono, fontSize: '11px', color: L.text2 }">
          <span>{{ s.loc }}</span>
          <span>{{ s.date }}</span>
          <span>{{ s.dur === 'live' ? 'live' : s.dur }}</span>
          <span>{{ s.events }} events</span>
        </div>
      </DCard>
    </div>

    <!-- tablet & desktop: table (tablet drops Duration column) -->
    <DCard v-else :pad="0">
      <div :style="headerRow">
        <SecLabel v-for="h in headers" :key="h">{{ h }}</SecLabel>
      </div>
      <div
        v-for="(s, i) in rows"
        :key="s.id"
        :style="{ display: 'grid', gridTemplateColumns: cols, gap: '12px', alignItems: 'center', padding: '13px 18px', borderTop: i ? `1px solid ${L.border}` : 'none', cursor: 'pointer' }"
        @click="router.push(`/sessions/${s.id}`)"
      >
        <div :style="{ display: 'flex', alignItems: 'center', gap: '11px', minWidth: 0 }">
          <DockDot v-if="s.status === 'live'" tone="crit" pulse />
          <Badge v-else :id="systemOf(s.systems[0])?.kind ?? 'core'" :size="24" />
          <div :style="{ minWidth: 0 }">
            <div :style="{ fontFamily: L.body, fontSize: '13.5px', fontWeight: 700, color: L.text, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }">{{ s.name }}</div>
            <div :style="{ fontFamily: L.mono, fontSize: '10px', color: L.text3, marginTop: '2px' }">{{ s.id }} · {{ s.type }} · {{ s.engineer }}</div>
          </div>
        </div>
        <span :style="{ fontFamily: L.body, fontSize: '12.5px', color: L.text2 }">{{ s.loc }}</span>
        <span :style="{ fontFamily: L.mono, fontSize: '11px', color: L.text2 }">{{ s.date }}</span>
        <span v-if="!isCompact" :style="{ fontFamily: L.mono, fontSize: '11px', color: L.text2 }">{{ s.dur === 'live' ? '—' : s.dur }}</span>
        <span :style="{ fontFamily: L.mono, fontSize: '11px', color: L.text2 }">{{ s.events }}</span>
        <Pill :tone="STATUS_TONE[s.status]">{{ STATUS_LABEL[s.status] }}</Pill>
      </div>
    </DCard>
  </div>
</template>
