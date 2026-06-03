<script setup lang="ts">
import { computed } from 'vue'
import { TONE, type Tone } from '@/dock/status'

const props = withDefaults(
  defineProps<{ data: number[]; w?: number; h?: number; tone?: Tone; fillArea?: boolean }>(),
  { w: 120, h: 32, tone: 'accent', fillArea: true },
)

const geom = computed(() => {
  const { data, w, h } = props
  const max = Math.max(...data)
  const min = Math.min(...data)
  const rng = max - min || 1
  const pts = data.map(
    (v, i) => [(i / (data.length - 1)) * w, h - 2 - ((v - min) / rng) * (h - 4)] as const,
  )
  const line = pts.map((p, i) => `${i ? 'L' : 'M'}${p[0].toFixed(1)} ${p[1].toFixed(1)}`).join(' ')
  const area = `${line} L${w} ${h} L0 ${h} Z`
  const last = pts[pts.length - 1]
  return { line, area, last }
})

const color = computed(() => TONE[props.tone])
</script>

<template>
  <svg :width="w" :height="h" :style="{ display: 'block', overflow: 'visible' }">
    <path v-if="fillArea" :d="geom.area" :fill="color" opacity="0.08" />
    <path :d="geom.line" fill="none" :stroke="color" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
    <circle :cx="geom.last[0]" :cy="geom.last[1]" r="2" :fill="color" />
  </svg>
</template>
