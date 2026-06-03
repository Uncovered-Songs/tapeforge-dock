<script setup lang="ts">
import { computed, type CSSProperties } from 'vue'
import { L } from '@/design/tokens'
import { useBreakpoint } from '@/composables/useBreakpoint'

/* Page title + optional subtitle, with a `right` slot for actions.
   Stacks (title over actions) on phones. */
defineProps<{ title: string; sub?: string }>()

const { isMobile } = useBreakpoint()

const wrap = computed<CSSProperties>(() => ({
  display: 'flex',
  flexDirection: isMobile.value ? 'column' : 'row',
  alignItems: isMobile.value ? 'flex-start' : 'flex-end',
  justifyContent: 'space-between',
  gap: isMobile.value ? '12px' : '20px',
  marginBottom: '22px',
}))
const titleStyle = computed<CSSProperties>(() => ({
  margin: '0',
  fontFamily: L.body,
  fontSize: isMobile.value ? '21px' : '24px',
  fontWeight: 700,
  letterSpacing: '-0.02em',
  color: L.text,
}))
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
