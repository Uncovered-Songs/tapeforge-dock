<script setup lang="ts">
import { computed, type CSSProperties } from 'vue'
import { L } from '@/design/tokens'
import { TONE, TONE_BG, type Tone } from '@/dock/status'
import DockDot from './DockDot.vue'

const props = withDefaults(
  defineProps<{ tone?: Tone; icon?: boolean }>(),
  { tone: 'idle', icon: true },
)

const style = computed<CSSProperties>(() => {
  const [bg, bd] = TONE_BG[props.tone] ?? TONE_BG.idle
  return {
    display: 'inline-flex',
    alignItems: 'center',
    gap: '6px',
    fontFamily: L.mono,
    fontSize: '10.5px',
    fontWeight: 600,
    letterSpacing: '0.04em',
    color: TONE[props.tone],
    background: bg,
    border: `1px solid ${bd}`,
    borderRadius: '6px',
    padding: '3px 8px',
    whiteSpace: 'nowrap',
  }
})
</script>

<template>
  <span :style="style">
    <DockDot v-if="icon" :tone="tone" :size="6" />
    <slot />
  </span>
</template>
