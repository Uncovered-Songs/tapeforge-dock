<script setup lang="ts">
import { computed, ref, type CSSProperties } from 'vue'
import { useRouter } from 'vue-router'
import { L } from '@/design/tokens'
import { useBreakpoint } from '@/composables/useBreakpoint'
import { S, type Tone } from '@/dock/status'
import { knowledge } from '@/dock/data'
import DCard from '@/components/kit/DCard.vue'
import Pill from '@/components/kit/Pill.vue'
import DockDot from '@/components/kit/DockDot.vue'
import Icon from '@/components/kit/Icon.vue'
import PageHead from '@/components/kit/PageHead.vue'
import Btn from '@/components/kit/Btn.vue'

const router = useRouter()
const { isMobile, isCompact } = useBreakpoint()

const KIND_TONE: Record<string, Tone> = {
  Generated: 'accent',
  Note: 'idle',
  Troubleshooting: 'warn',
  Imported: 'info',
}

const q = ref('')

const tags = computed(() => [...new Set(knowledge.flatMap((k) => k.tags))])

const filtered = computed(() =>
  knowledge.filter(
    (k) =>
      !q.value ||
      k.title.toLowerCase().includes(q.value.toLowerCase()) ||
      k.tags.some((t) => t.includes(q.value.toLowerCase())),
  ),
)

const graphRows = computed<[string, number, Tone][]>(() => [
  ['Generated', knowledge.filter((k) => k.kind === 'Generated').length, 'accent'],
  ['Troubleshooting', knowledge.filter((k) => k.kind === 'Troubleshooting').length, 'warn'],
  ['Notes', knowledge.filter((k) => k.kind === 'Note').length, 'idle'],
  ['Imported', knowledge.filter((k) => k.kind === 'Imported').length, 'info'],
])

function openCard(cites: number): void {
  if (cites) router.push('/crew')
}

const page = computed<CSSProperties>(() => ({
  padding: isMobile.value ? '18px 14px' : '26px 28px',
  maxWidth: '1280px',
  margin: '0 auto',
}))
const grid = computed<CSSProperties>(() => ({
  display: 'grid',
  gridTemplateColumns: isCompact.value ? '1fr' : '1fr 280px',
  gap: '16px',
  alignItems: 'start',
}))
const searchBar: CSSProperties = {
  display: 'flex',
  alignItems: 'center',
  gap: '9px',
  padding: '10px 13px',
  borderRadius: '10px',
  border: `1px solid ${L.border}`,
  background: L.panel,
  marginBottom: '14px',
}
const searchInput: CSSProperties = {
  flex: 1,
  border: 'none',
  outline: 'none',
  fontFamily: L.body,
  fontSize: '13.5px',
  color: L.text,
  background: 'transparent',
}
const aiSearchTag: CSSProperties = {
  fontFamily: L.mono,
  fontSize: '9px',
  fontWeight: 600,
  color: S.accentText,
  background: S.accentBg,
  border: `1px solid ${S.accentBorder}`,
  borderRadius: '4px',
  padding: '2px 6px',
}
const tagChip: CSSProperties = {
  fontFamily: L.mono,
  fontSize: '9.5px',
  color: L.text3,
  background: L.pageBg,
  border: `1px solid ${L.border}`,
  borderRadius: '5px',
  padding: '2px 7px',
}
const railTag: CSSProperties = {
  fontFamily: L.mono,
  fontSize: '10.5px',
  color: L.text2,
  background: L.pageBg,
  border: `1px solid ${L.border}`,
  borderRadius: '6px',
  padding: '4px 9px',
  cursor: 'pointer',
}
</script>

<template>
  <div :style="page">
    <PageHead title="Knowledge" sub="Organizational memory — imported, generated and operator-authored">
      <template #right>
        <Btn icon="plus" sm primary>New entry</Btn>
      </template>
    </PageHead>

    <div :style="grid">
      <div>
        <div :style="searchBar">
          <Icon name="search" :size="15" :style="{ color: L.text3 }" />
          <input
            v-model="q"
            placeholder="Search knowledge — Crew indexes every entry…"
            :style="searchInput"
          />
          <span :style="aiSearchTag">AI SEARCH</span>
        </div>

        <div :style="{ display: 'flex', flexDirection: 'column', gap: '10px' }">
          <DCard
            v-for="k in filtered"
            :key="k.id"
            hover
            :pad="15"
            :clickable="!!k.cites"
            @click="openCard(k.cites)"
          >
            <div :style="{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '9px' }">
              <Pill :tone="KIND_TONE[k.kind]" :icon="false">{{ k.kind }}</Pill>
              <span :style="{ flex: 1 }" />
              <span
                v-if="k.cites > 0"
                :style="{ display: 'inline-flex', alignItems: 'center', gap: '5px', fontFamily: L.mono, fontSize: '10px', color: L.text3 }"
              >
                <Icon name="link" :size="12" />{{ k.cites }} cites
              </span>
              <span :style="{ fontFamily: L.mono, fontSize: '10px', color: L.text3 }">{{ k.updated }}</span>
            </div>
            <div :style="{ fontFamily: L.body, fontSize: '14.5px', fontWeight: 700, color: L.text, marginBottom: '9px' }">
              {{ k.title }}
            </div>
            <div :style="{ display: 'flex', alignItems: 'center', gap: '7px' }">
              <span v-for="t in k.tags" :key="t" :style="tagChip">{{ t }}</span>
              <span :style="{ flex: 1 }" />
              <span :style="{ fontFamily: L.mono, fontSize: '10px', color: L.text3 }">by {{ k.by }}</span>
              <span v-if="k.by === 'Crew'" :style="{ color: S.accentText }"><Icon name="spark" :size="12" fill="cur" /></span>
            </div>
          </DCard>
        </div>
      </div>

      <!-- right rail -->
      <div :style="{ display: 'flex', flexDirection: 'column', gap: '16px' }">
        <DCard v-if="!isMobile" title="Knowledge graph">
          <div :style="{ display: 'flex', flexDirection: 'column', gap: '11px' }">
            <div v-for="r in graphRows" :key="r[0]" :style="{ display: 'flex', alignItems: 'center', gap: '9px' }">
              <DockDot :tone="r[2]" />
              <span :style="{ fontFamily: L.body, fontSize: '12.5px', color: L.text2, flex: 1 }">{{ r[0] }}</span>
              <span :style="{ fontFamily: L.mono, fontSize: '12px', fontWeight: 600, color: L.text }">{{ r[1] }}</span>
            </div>
          </div>
        </DCard>

        <DCard title="Tags">
          <div :style="{ display: 'flex', flexWrap: 'wrap', gap: '7px' }">
            <span v-for="t in tags" :key="t" :style="railTag" @click="q = t">{{ t }}</span>
          </div>
        </DCard>
      </div>
    </div>
  </div>
</template>
