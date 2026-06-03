<script setup lang="ts">
import { computed, type CSSProperties } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { L } from '@/design/tokens'
import { S, type Tone } from '@/dock/status'
import { systems, sessions, type DockSystem } from '@/dock/data'
import DCard from '@/components/kit/DCard.vue'
import Pill from '@/components/kit/Pill.vue'
import DockDot from '@/components/kit/DockDot.vue'
import Icon from '@/components/kit/Icon.vue'
import Spark from '@/components/kit/Spark.vue'
import Badge from '@/components/kit/Badge.vue'
import SecLabel from '@/components/kit/SecLabel.vue'
import PageHead from '@/components/kit/PageHead.vue'
import Btn from '@/components/kit/Btn.vue'

const router = useRouter()
const route = useRoute()

const KIND_LABEL: Record<string, string> = {
  core: 'Control plane',
  port: 'Transport',
  desk: 'Mixing',
  rig: 'Processing',
  capstan: 'Recording',
  scope: 'Observability',
}

const sub = computed(() => (route.params.id ? String(route.params.id) : null))
const sy = computed<DockSystem | null>(() =>
  sub.value ? (systems.find((x) => x.id === sub.value) ?? null) : null,
)

interface Metric {
  label: string
  value: string | number
  data: number[] | null
  tone: Tone
}
const metrics = computed<Metric[]>(() => {
  const s = sy.value
  if (!s) return []
  return [
    {
      label: 'CPU load',
      value: s.cpu + '%',
      data: [s.cpu - 8, s.cpu - 3, s.cpu + 5, s.cpu - 2, s.cpu, s.cpu + 3, s.cpu],
      tone: (s.cpu > 55 ? 'warn' : 'accent') as Tone,
    },
    { label: 'Active sessions', value: s.sessions, data: null, tone: 'info' as Tone },
    { label: 'Software', value: 'v' + s.ver, data: null, tone: 'idle' as Tone },
  ]
})

const capabilities = computed<string[]>(() => {
  const s = sy.value
  if (!s) return []
  return [...s.note.split(' · '), 'AES67', 'PTP', 'shared-mem']
})

interface HistoryRow {
  tone: Tone
  text: string
  when: string
}
const history = computed<HistoryRow[]>(() => {
  const s = sy.value
  if (!s) return []
  const joined = sessions.find((ss) => ss.systems.includes(s.id))?.id || 'S-2041'
  return [
    { tone: 'ok' as Tone, text: 'Joined session ' + joined, when: 'now' },
    { tone: 'info' as Tone, text: 'Software updated to v' + s.ver, when: '2d ago' },
    {
      tone: s.status,
      text: s.status === 'crit' ? 'Lost PTP lock' : 'Health check passed',
      when: s.status === 'crit' ? '4h ago' : '6h ago',
    },
  ]
})

const statusLabel = (t: Tone): string => (t === 'ok' ? 'HEALTHY' : t === 'warn' ? 'DEGRADED' : 'OFFLINE')

const byLoc = computed<[string, DockSystem[]][]>(() => {
  const map: Record<string, DockSystem[]> = {}
  systems.forEach((s) => {
    ;(map[s.loc] = map[s.loc] || []).push(s)
  })
  return Object.entries(map)
})

function borderFor(status: Tone): string {
  return status === 'crit' ? S.critBorder : status === 'warn' ? S.warnBorder : L.border
}

const MONO = L.mono
const BODY = L.body

const detailPage: CSSProperties = { padding: '24px 28px', maxWidth: '1100px', margin: '0 auto' }
const listPage: CSSProperties = { padding: '26px 28px', maxWidth: '1280px', margin: '0 auto' }
</script>

<template>
  <!-- DETAIL -->
  <div v-if="sy" :style="detailPage">
    <div
      :style="{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '16px', fontFamily: BODY, fontSize: '13px' }"
    >
      <span :style="{ color: L.text2, cursor: 'pointer', fontWeight: 600 }" @click="router.push('/systems')">Systems</span>
      <span :style="{ color: L.text3, display: 'flex' }"><Icon name="chevron" :size="13" /></span>
      <span :style="{ color: L.text, fontWeight: 700 }">{{ sy.name }}</span>
    </div>

    <div :style="{ display: 'flex', alignItems: 'flex-start', gap: '16px', marginBottom: '18px' }">
      <Badge :id="sy.kind" :size="48" :fs="17" />
      <div :style="{ flex: 1 }">
        <div :style="{ display: 'flex', alignItems: 'center', gap: '11px' }">
          <h1 :style="{ margin: 0, fontFamily: BODY, fontSize: '23px', fontWeight: 700, color: L.text }">{{ sy.name }}</h1>
          <Pill :tone="sy.status">{{ statusLabel(sy.status) }}</Pill>
        </div>
        <div :style="{ fontFamily: MONO, fontSize: '11px', color: L.text2, marginTop: '6px' }">
          {{ KIND_LABEL[sy.kind] }} · {{ sy.loc }} · v{{ sy.ver }} · up {{ sy.uptime }}
        </div>
      </div>
      <Btn icon="spark" sm @click="router.push('/crew')">Ask Crew</Btn>
    </div>

    <div
      :style="{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '14px', marginBottom: '16px' }"
    >
      <DCard v-for="m in metrics" :key="m.label" :pad="15">
        <SecLabel :style="{ marginBottom: '10px' }">{{ m.label }}</SecLabel>
        <div :style="{ display: 'flex', alignItems: 'flex-end', justifyContent: 'space-between' }">
          <span :style="{ fontFamily: BODY, fontSize: '24px', fontWeight: 700, color: L.text }">{{ m.value }}</span>
          <Spark v-if="m.data" :data="m.data" :w="96" :h="30" :tone="m.tone" />
        </div>
      </DCard>
    </div>

    <div :style="{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }">
      <DCard title="Capabilities">
        <div :style="{ display: 'flex', flexWrap: 'wrap', gap: '8px' }">
          <Pill v-for="(c, i) in capabilities" :key="i" tone="idle" :icon="false">{{ c }}</Pill>
        </div>
      </DCard>

      <DCard title="Recent history">
        <div
          v-for="(h, i) in history"
          :key="i"
          :style="{ display: 'flex', alignItems: 'center', gap: '9px', padding: '8px 0', borderTop: i ? `1px solid ${L.border}` : 'none' }"
        >
          <DockDot :tone="h.tone" />
          <span :style="{ fontFamily: BODY, fontSize: '12.5px', color: L.text2, flex: 1 }">{{ h.text }}</span>
          <span :style="{ fontFamily: MONO, fontSize: '10px', color: L.text3 }">{{ h.when }}</span>
        </div>
      </DCard>
    </div>
  </div>

  <!-- INVENTORY LIST -->
  <div v-else :style="listPage">
    <PageHead title="Systems" :sub="`${systems.length} deployed systems across 4 locations`">
      <template #right>
        <div :style="{ display: 'flex', gap: '9px' }">
          <Btn icon="filter" sm>All kinds</Btn>
          <Btn icon="plus" sm>Register system</Btn>
        </div>
      </template>
    </PageHead>

    <div v-for="[loc, list] in byLoc" :key="loc" :style="{ marginBottom: '22px' }">
      <div :style="{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '11px' }">
        <span :style="{ color: L.text3, display: 'flex' }"><Icon name="pin" :size="13" fill="cur" /></span>
        <span :style="{ fontFamily: BODY, fontSize: '13.5px', fontWeight: 700, color: L.text }">{{ loc }}</span>
        <span :style="{ fontFamily: MONO, fontSize: '10px', color: L.text3 }">{{ list.length }} systems</span>
      </div>

      <div :style="{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '12px' }">
        <DCard
          v-for="s in list"
          :key="s.id"
          hover
          clickable
          :pad="15"
          :style="{ borderColor: borderFor(s.status) }"
          @click="router.push(`/systems/${s.id}`)"
        >
          <div :style="{ display: 'flex', alignItems: 'center', gap: '9px', marginBottom: '12px' }">
            <Badge :id="s.kind" :size="28" :fs="11" />
            <div :style="{ flex: 1, minWidth: 0 }">
              <div :style="{ fontFamily: BODY, fontSize: '13px', fontWeight: 700, color: L.text, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }">{{ s.name }}</div>
              <div :style="{ fontFamily: MONO, fontSize: '9px', color: L.text3 }">{{ KIND_LABEL[s.kind] }}</div>
            </div>
            <DockDot :tone="s.status" :pulse="s.status !== 'ok'" />
          </div>
          <div :style="{ fontFamily: MONO, fontSize: '10.5px', color: L.text2, lineHeight: 1.6 }">{{ s.note }}</div>
          <div
            :style="{ display: 'flex', justifyContent: 'space-between', marginTop: '12px', paddingTop: '10px', borderTop: `1px solid ${L.border}`, fontFamily: MONO, fontSize: '9.5px', color: L.text3 }"
          >
            <span>v{{ s.ver }}</span>
            <span>{{ s.cpu }}% CPU</span>
            <span>{{ s.uptime }}</span>
          </div>
        </DCard>
      </div>
    </div>
  </div>
</template>
