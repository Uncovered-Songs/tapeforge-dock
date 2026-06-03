<script setup lang="ts">
import { computed, type CSSProperties } from 'vue'
import { L } from '@/design/tokens'
import { TONE, type Tone } from '@/dock/status'

const props = withDefaults(
  defineProps<{ value: number; size?: number; tone?: Tone; label?: string }>(),
  { size: 56, tone: 'ok' },
)

const geom = computed(() => {
  const r = props.size / 2 - 4
  const c = 2 * Math.PI * r
  return { r, c, dash: `${(props.value / 100) * c} ${c}` }
})

const wrap = computed<CSSProperties>(() => ({
  position: 'relative',
  width: `${props.size}px`,
  height: `${props.size}px`,
}))
const center: CSSProperties = {
  position: 'absolute',
  inset: '0',
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  justifyContent: 'center',
  lineHeight: '1',
}
const valStyle = computed<CSSProperties>(() => ({
  fontFamily: L.mono,
  fontSize: props.size > 48 ? '14px' : '11px',
  fontWeight: 600,
  color: L.text,
}))
</script>

<template>
  <div :style="wrap">
    <svg :width="size" :height="size" :style="{ transform: 'rotate(-90deg)' }">
      <circle :cx="size / 2" :cy="size / 2" :r="geom.r" fill="none" :stroke="L.border" stroke-width="4" />
      <circle
        :cx="size / 2"
        :cy="size / 2"
        :r="geom.r"
        fill="none"
        :stroke="TONE[tone]"
        stroke-width="4"
        stroke-linecap="round"
        :stroke-dasharray="geom.dash"
      />
    </svg>
    <div :style="center">
      <span :style="valStyle">{{ value }}</span>
      <span v-if="label" :style="{ fontFamily: L.mono, fontSize: '7px', color: L.text3, marginTop: '2px' }">{{ label }}</span>
    </div>
  </div>
</template>
