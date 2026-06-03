<script setup lang="ts">
import { computed } from 'vue'
import { TONE, type Tone } from '@/dock/status'

const props = withDefaults(
  defineProps<{ data: number[]; w?: number; h?: number; tone?: Tone; gap?: number }>(),
  { w: 120, h: 34, tone: 'accent', gap: 2 },
)

const bars = computed(() => {
  const { data, w, h, gap } = props
  const max = Math.max(...data) || 1
  const bw = (w - gap * (data.length - 1)) / data.length
  return data.map((v, i) => {
    const bh = Math.max(1, (v / max) * (h - 2))
    return {
      x: i * (bw + gap),
      y: h - bh,
      width: bw,
      height: bh,
      opacity: i === data.length - 1 ? 1 : 0.32 + 0.5 * (v / max),
    }
  })
})

const color = computed(() => TONE[props.tone])
</script>

<template>
  <svg :width="w" :height="h" :style="{ display: 'block' }">
    <rect
      v-for="(b, i) in bars"
      :key="i"
      :x="b.x"
      :y="b.y"
      :width="b.width"
      :height="b.height"
      rx="1"
      :fill="color"
      :opacity="b.opacity"
    />
  </svg>
</template>
