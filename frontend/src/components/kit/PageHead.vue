<script setup lang="ts">
import type { CSSProperties } from 'vue'
import { L } from '@/design/tokens'

/* Page title + optional subtitle, with a `right` slot for actions. */
defineProps<{ title: string; sub?: string }>()

const wrap: CSSProperties = {
  display: 'flex',
  alignItems: 'flex-end',
  justifyContent: 'space-between',
  gap: '20px',
  marginBottom: '22px',
}
const titleStyle: CSSProperties = {
  margin: '0',
  fontFamily: L.body,
  fontSize: '24px',
  fontWeight: 700,
  letterSpacing: '-0.02em',
  color: L.text,
}
const subStyle: CSSProperties = {
  margin: '6px 0 0',
  fontFamily: L.body,
  fontSize: '14px',
  color: L.text2,
}
</script>

<template>
  <div :style="wrap">
    <div>
      <h1 :style="titleStyle">{{ title }}</h1>
      <p v-if="sub" :style="subStyle">{{ sub }}</p>
    </div>
    <slot name="right" />
  </div>
</template>
