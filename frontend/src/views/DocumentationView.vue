<script setup lang="ts">
import { ref, type CSSProperties } from 'vue'
import { useRouter } from 'vue-router'
import { L } from '@/design/tokens'
import { S } from '@/dock/status'
import { docTree } from '@/dock/data'
import Pill from '@/components/kit/Pill.vue'
import Icon from '@/components/kit/Icon.vue'
import SecLabel from '@/components/kit/SecLabel.vue'
import Btn from '@/components/kit/Btn.vue'

const router = useRouter()

const active = ref('PTP & clocking')

const sections: [string, string][] = [
  [
    'Grandmaster priority',
    'When two PORT nodes are grandmaster-capable, assign explicit priority values. Equal priority causes failover loops under jitter.',
  ],
  [
    'Guard threshold',
    'Default offset guard is 40µs. CORE captures a topology snapshot and fails over to the next-priority grandmaster automatically.',
  ],
  [
    'Verifying lock',
    'Use SCOPE → Network to confirm PTP offset < 10µs and jitter < 0.3ms across all streams before going live.',
  ],
]

const root: CSSProperties = {
  flex: 1,
  minWidth: 0,
  display: 'flex',
  minHeight: 0,
  height: '100%',
}
const tree: CSSProperties = {
  width: '248px',
  flex: '0 0 248px',
  borderRight: `1px solid ${L.border}`,
  background: L.pageBg,
  overflowY: 'auto',
  padding: '18px 14px',
}
const treeSearch: CSSProperties = {
  display: 'flex',
  alignItems: 'center',
  gap: '8px',
  padding: '8px 10px',
  borderRadius: '8px',
  border: `1px solid ${L.border}`,
  background: L.panel,
  marginBottom: '14px',
}
const body: CSSProperties = {
  flex: 1,
  minWidth: 0,
  overflowY: 'auto',
  padding: '30px 40px',
}
const article: CSSProperties = { maxWidth: '720px', margin: '0 auto' }
const crumbs: CSSProperties = {
  display: 'flex',
  alignItems: 'center',
  gap: '8px',
  marginBottom: '16px',
  fontFamily: L.mono,
  fontSize: '10.5px',
  color: L.text3,
}
const h1Style: CSSProperties = {
  margin: '0 0 8px',
  fontFamily: L.body,
  fontSize: '28px',
  fontWeight: 700,
  letterSpacing: '-0.02em',
  color: L.text,
}
const lead: CSSProperties = {
  margin: '0 0 22px',
  fontFamily: L.body,
  fontSize: '15px',
  lineHeight: 1.6,
  color: L.text2,
}
const callout: CSSProperties = {
  display: 'flex',
  gap: '11px',
  padding: '13px 15px',
  background: S.accentBg,
  border: `1px solid ${S.accentBorder}`,
  borderRadius: '10px',
  marginBottom: '22px',
}
const footer: CSSProperties = {
  display: 'flex',
  gap: '10px',
  marginTop: '28px',
  paddingTop: '18px',
  borderTop: `1px solid ${L.border}`,
}

function treeItemStyle(it: string): CSSProperties {
  const on = active.value === it
  return {
    fontFamily: L.body,
    fontSize: '12.5px',
    fontWeight: on ? 700 : 500,
    color: on ? S.accentText : L.text2,
    padding: '6px 10px',
    borderRadius: '7px',
    cursor: 'pointer',
    background: on ? S.accentBg : 'transparent',
  }
}
</script>

<template>
  <div :style="root">
    <!-- doc tree -->
    <div :style="tree">
      <div :style="treeSearch">
        <Icon name="search" :size="13" :style="{ color: L.text3 }" />
        <span :style="{ fontFamily: L.body, fontSize: '12.5px', color: L.text3 }">Search docs…</span>
      </div>
      <div v-for="g in docTree" :key="g.group" :style="{ marginBottom: '16px' }">
        <SecLabel :style="{ marginBottom: '8px', paddingLeft: '6px' }">{{ g.group }}</SecLabel>
        <div v-for="it in g.items" :key="it" :style="treeItemStyle(it)" @click="active = it">{{ it }}</div>
      </div>
    </div>

    <!-- doc body -->
    <div :style="body">
      <div :style="article">
        <div :style="crumbs">
          <span>Network Audio</span>
          <Icon name="chevron" :size="11" />
          <span :style="{ color: L.text2 }">{{ active }}</span>
          <span :style="{ flex: 1 }" />
          <Pill tone="accent" :icon="false">Docusaurus · embedded</Pill>
        </div>

        <h1 :style="h1Style">{{ active }}</h1>
        <p :style="lead">
          Precision Time Protocol (PTP, IEEE 1588) keeps every PORT node sample-aligned across the
          network. CORE monitors grandmaster offset and triggers failover when drift exceeds the
          configured guard threshold.
        </p>

        <!-- crew callout -->
        <div :style="callout">
          <Icon name="spark" :size="15" fill="cur" :style="{ color: S.accentText, marginTop: '1px' }" />
          <div>
            <div :style="{ fontFamily: L.body, fontSize: '12.5px', fontWeight: 600, color: L.text, marginBottom: '3px' }">
              Crew context
            </div>
            <div :style="{ fontFamily: L.body, fontSize: '12.5px', lineHeight: 1.5, color: L.text2 }">
              This page was cited in
              <span
                :style="{ color: S.accentText, cursor: 'pointer', fontWeight: 600 }"
                @click="router.push('/sessions/S-2040')"
              >Session S-2040</span>
              after a grandmaster failover. Your org has had 3 related clock events this week.
            </div>
          </div>
        </div>

        <div v-for="(s, i) in sections" :key="i" :style="{ marginBottom: '20px' }">
          <h2 :style="{ margin: '0 0 7px', fontFamily: L.body, fontSize: '17px', fontWeight: 700, color: L.text }">{{ s[0] }}</h2>
          <p :style="{ margin: 0, fontFamily: L.body, fontSize: '14px', lineHeight: 1.6, color: L.text2 }">{{ s[1] }}</p>
        </div>

        <div :style="footer">
          <Btn sm icon="spark" primary @click="router.push('/crew')">Ask Crew about this</Btn>
          <Btn sm icon="ext">Open in new tab</Btn>
        </div>
      </div>
    </div>
  </div>
</template>
