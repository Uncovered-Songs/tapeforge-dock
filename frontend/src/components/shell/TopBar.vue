<script setup lang="ts">
import type { CSSProperties } from 'vue'
import { RouterLink } from 'vue-router'
import { L } from '@/design/tokens'
import { S } from '@/dock/status'
import Icon from '@/components/kit/Icon.vue'

export interface Crumb {
  label: string
  to?: string
}

defineProps<{ crumbs: Crumb[] }>()
const emit = defineEmits<{ 'open-palette': [] }>()

const bar: CSSProperties = {
  height: '64px',
  flex: '0 0 64px',
  background: L.pageBg,
  borderBottom: `1px solid ${L.border}`,
  display: 'flex',
  alignItems: 'center',
  gap: '14px',
  padding: '0 22px',
}
const search: CSSProperties = {
  display: 'flex',
  alignItems: 'center',
  gap: '8px',
  width: '260px',
  padding: '7px 11px',
  borderRadius: '8px',
  border: `1px solid ${L.border}`,
  background: L.panel,
  color: L.text3,
  cursor: 'text',
}
const kbd: CSSProperties = {
  fontFamily: L.mono,
  fontSize: '9.5px',
  border: `1px solid ${L.border}`,
  borderRadius: '4px',
  padding: '1px 5px',
}
const iconBtn: CSSProperties = {
  width: '30px',
  height: '30px',
  borderRadius: '8px',
  border: `1px solid ${L.border}`,
  background: L.panel,
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  color: L.text2,
  cursor: 'pointer',
}
const avatar: CSSProperties = {
  width: '30px',
  height: '30px',
  borderRadius: '50%',
  background: S.info,
  color: '#fff',
  fontFamily: L.body,
  fontSize: '12px',
  fontWeight: 700,
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
}

function crumbStyle(last: boolean, link: boolean): CSSProperties {
  return {
    fontFamily: L.body,
    fontSize: '14px',
    fontWeight: last ? 700 : 500,
    color: last ? L.text : L.text2,
    cursor: link ? 'pointer' : 'default',
    whiteSpace: 'nowrap',
    textDecoration: 'none',
  }
}
</script>

<template>
  <div :style="bar">
    <div :style="{ display: 'flex', alignItems: 'center', gap: '8px', minWidth: 0 }">
      <template v-for="(c, i) in crumbs" :key="i">
        <span v-if="i > 0" :style="{ color: L.text3, display: 'flex' }"><Icon name="chevron" :size="13" /></span>
        <RouterLink v-if="c.to" :to="c.to" :style="crumbStyle(i === crumbs.length - 1, true)">{{ c.label }}</RouterLink>
        <span v-else :style="crumbStyle(i === crumbs.length - 1, false)">{{ c.label }}</span>
      </template>
    </div>

    <div :style="{ flex: 1 }" />

    <div :style="search" @click="emit('open-palette')">
      <Icon name="search" :size="14" />
      <span :style="{ fontFamily: L.body, fontSize: '13px', flex: 1 }">Search or ask Crew…</span>
      <span :style="kbd">⌘K</span>
    </div>

    <div :style="iconBtn"><Icon name="bell" :size="15" /></div>
    <div :style="avatar">JC</div>
  </div>
</template>
