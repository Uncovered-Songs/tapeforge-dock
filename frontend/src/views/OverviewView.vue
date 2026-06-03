<script setup lang="ts">
import { computed, type CSSProperties } from 'vue'
import { useRouter } from 'vue-router'
import { L } from '@/design/tokens'
import { S, type Tone } from '@/dock/status'
import { sessions, systems, eventStream, crewRecs } from '@/dock/data'
import DCard from '@/components/kit/DCard.vue'
import Pill from '@/components/kit/Pill.vue'
import DockDot from '@/components/kit/DockDot.vue'
import Icon from '@/components/kit/Icon.vue'
import Spark from '@/components/kit/Spark.vue'
import Bars from '@/components/kit/Bars.vue'
import Badge from '@/components/kit/Badge.vue'
import SecLabel from '@/components/kit/SecLabel.vue'
import PageHead from '@/components/kit/PageHead.vue'
import Btn from '@/components/kit/Btn.vue'

const router = useRouter()
const live = computed(() => sessions.filter((s) => s.status === 'live'))
const recent = computed(() => eventStream.slice().reverse().slice(0, 6))

const stats = [
  { label: 'Active systems', value: '7', unit: '/ 8', tone: 'ok' as Tone, bars: [5, 6, 6, 7, 6, 7, 7, 8, 7, 7] },
  { label: 'Active sessions', value: '3', unit: 'live', tone: 'accent' as Tone, spark: [1, 1, 2, 2, 1, 3, 2, 3, 3, 3] },
  { label: 'Events · 24h', value: '671', unit: '', tone: 'info' as Tone, bars: [20, 32, 28, 41, 38, 52, 60, 48, 55, 71] },
  { label: 'Open issues', value: '2', unit: 'warn', tone: 'warn' as Tone, spark: [0, 1, 0, 2, 1, 1, 3, 2, 2, 2] },
]

function recAction(action: string) {
  router.push(action.includes('diagnostics') ? '/diagnostics' : action.includes('systems') ? '/systems' : '/crew')
}
function systemOf(id: string) {
  return systems.find((x) => x.id === id)
}
function bgFor(status: Tone): string {
  return status === 'crit' ? S.critBg : status === 'warn' ? S.warnBg : L.panel
}

const page: CSSProperties = { padding: '26px 28px', maxWidth: '1280px', margin: '0 auto' }
const statCard: CSSProperties = {
  flex: 1,
  minWidth: 0,
  padding: '15px 16px',
  background: L.panel,
  border: `1px solid ${L.border}`,
  borderRadius: '12px',
  boxShadow: '0 1px 2px rgba(16,24,40,0.04)',
}
const grid: CSSProperties = { display: 'grid', gridTemplateColumns: '1.5fr 1fr', gap: '16px', alignItems: 'start' }
const colStack: CSSProperties = { display: 'flex', flexDirection: 'column', gap: '16px' }
const linkAction: CSSProperties = { fontFamily: L.body, fontSize: '12.5px', fontWeight: 600, color: S.accentText, cursor: 'pointer' }
const aiTag: CSSProperties = { fontFamily: L.mono, fontSize: '9px', fontWeight: 600, color: S.accentText, background: S.accentBg, border: `1px solid ${S.accentBorder}`, borderRadius: '4px', padding: '2px 6px' }
</script>

<template>
  <div :style="page">
    <PageHead title="Overview" sub="Northgate Audio · operational summary across 4 locations">
      <template #right>
        <div :style="{ display: 'flex', gap: '9px' }">
          <Btn icon="filter" sm>Last 24h</Btn>
          <Btn icon="spark" sm primary @click="router.push('/crew')">Ask Crew</Btn>
        </div>
      </template>
    </PageHead>

    <!-- stat row -->
    <div :style="{ display: 'flex', gap: '14px', marginBottom: '16px' }">
      <div v-for="st in stats" :key="st.label" :style="statCard">
        <div :style="{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px' }">
          <SecLabel>{{ st.label }}</SecLabel>
          <span :style="{ marginLeft: 'auto' }"><DockDot :tone="st.tone" /></span>
        </div>
        <div :style="{ display: 'flex', alignItems: 'flex-end', justifyContent: 'space-between', gap: '10px' }">
          <div :style="{ fontFamily: L.body, fontSize: '28px', fontWeight: 700, letterSpacing: '-0.02em', color: L.text, lineHeight: 1 }">
            {{ st.value }}<span :style="{ fontFamily: L.mono, fontSize: '12px', fontWeight: 500, color: L.text3, marginLeft: '4px' }">{{ st.unit }}</span>
          </div>
          <Spark v-if="st.spark" :data="st.spark" :w="92" :h="30" :tone="st.tone" />
          <Bars v-else-if="st.bars" :data="st.bars" :w="92" :h="30" :tone="st.tone" />
        </div>
      </div>
    </div>

    <div :style="grid">
      <!-- left column -->
      <div :style="colStack">
        <DCard title="Active sessions" :pad="0">
          <template #action><span :style="linkAction" @click="router.push('/sessions')">View all →</span></template>
          <div
            v-for="(s, i) in live"
            :key="s.id"
            :style="{ display: 'flex', alignItems: 'center', gap: '14px', padding: '13px 16px', borderTop: i ? `1px solid ${L.border}` : 'none', cursor: 'pointer' }"
            @click="router.push(`/sessions/${s.id}`)"
          >
            <DockDot tone="crit" pulse />
            <div :style="{ flex: 1, minWidth: 0 }">
              <div :style="{ fontFamily: L.body, fontSize: '13.5px', fontWeight: 700, color: L.text }">{{ s.name }}</div>
              <div :style="{ fontFamily: L.mono, fontSize: '10.5px', color: L.text3, marginTop: '2px' }">{{ s.id }} · {{ s.type }} · {{ s.loc }} · since {{ s.start }}</div>
            </div>
            <div :style="{ display: 'flex' }">
              <span v-for="(sid, j) in s.systems.slice(0, 4)" :key="sid" :style="{ marginLeft: j ? '-6px' : '0' }">
                <Badge :id="systemOf(sid)?.kind ?? 'core'" :size="22" />
              </span>
            </div>
            <Pill :tone="s.issues ? 'warn' : 'ok'">{{ s.issues ? s.issues + ' issues' : 'clean' }}</Pill>
            <span :style="{ color: L.text3 }"><Icon name="chevron" :size="14" /></span>
          </div>
        </DCard>

        <DCard title="Systems health" :body-style="{ padding: '14px' }">
          <template #action><span :style="linkAction" @click="router.push('/systems')">Inventory →</span></template>
          <div :style="{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '10px' }">
            <div
              v-for="sy in systems"
              :key="sy.id"
              :style="{ display: 'flex', flexDirection: 'column', gap: '8px', padding: '11px 12px', border: `1px solid ${L.border}`, borderRadius: '10px', cursor: 'pointer', background: bgFor(sy.status) }"
              @click="router.push(`/systems/${sy.id}`)"
            >
              <div :style="{ display: 'flex', alignItems: 'center', gap: '7px' }">
                <Badge :id="sy.kind" :size="20" :fs="8.5" />
                <DockDot :tone="sy.status" />
              </div>
              <div :style="{ fontFamily: L.mono, fontSize: '11px', fontWeight: 600, color: L.text, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }">{{ sy.name }}</div>
              <div :style="{ fontFamily: L.mono, fontSize: '9px', color: L.text3 }">{{ sy.cpu }}% · {{ sy.uptime }}</div>
            </div>
          </div>
        </DCard>
      </div>

      <!-- right column -->
      <div :style="colStack">
        <DCard title="Crew recommendations" :pad="0">
          <template #action><span :style="aiTag">AI</span></template>
          <div v-for="(r, i) in crewRecs" :key="i" :style="{ padding: '13px 16px', borderTop: i ? `1px solid ${L.border}` : 'none' }">
            <div :style="{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '6px' }">
              <DockDot :tone="r.tone" /><span :style="{ fontFamily: L.body, fontSize: '13px', fontWeight: 700, color: L.text }">{{ r.title }}</span>
            </div>
            <p :style="{ margin: '0 0 9px', fontFamily: L.body, fontSize: '12.5px', lineHeight: 1.5, color: L.text2 }">{{ r.body }}</p>
            <span :style="{ fontFamily: L.body, fontSize: '12px', fontWeight: 600, color: S.accentText, cursor: 'pointer', display: 'inline-flex', alignItems: 'center', gap: '5px' }" @click="recAction(r.action)">
              {{ r.action }} <Icon name="arrowR" :size="12" />
            </span>
          </div>
        </DCard>

        <DCard title="Recent events" :pad="0">
          <template #action><SecLabel>live</SecLabel></template>
          <div v-for="(e, i) in recent" :key="i" :style="{ display: 'flex', alignItems: 'baseline', gap: '10px', padding: '9px 16px', borderTop: i ? `1px solid ${L.border}` : 'none' }">
            <span :style="{ marginTop: '4px' }"><DockDot :tone="e.tone" :size="6" /></span>
            <span :style="{ fontFamily: L.mono, fontSize: '10px', color: L.text3, flex: '0 0 auto' }">{{ e.t }}</span>
            <span :style="{ fontFamily: L.body, fontSize: '12.5px', color: L.text2, lineHeight: 1.4 }"><b :style="{ color: L.text, fontWeight: 600 }">{{ e.src }}</b> {{ e.msg }}</span>
          </div>
        </DCard>
      </div>
    </div>
  </div>
</template>
