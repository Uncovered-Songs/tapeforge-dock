<script setup lang="ts">
import { computed, type CSSProperties } from 'vue'
import { TONE, type Tone } from '@/dock/status'

const props = withDefaults(
  defineProps<{ tone?: Tone; size?: number; pulse?: boolean }>(),
  { tone: 'idle', size: 7 },
)

const style = computed<CSSProperties>(() => {
  const c = TONE[props.tone] ?? TONE.idle
  return {
    width: `${props.size}px`,
    height: `${props.size}px`,
    borderRadius: `${props.size}px`,
    background: c,
    flex: '0 0 auto',
    boxShadow: props.pulse ? `0 0 0 3px ${c}22` : 'none',
  }
})
</script>

<template>
  <span :style="style" />
</template>
