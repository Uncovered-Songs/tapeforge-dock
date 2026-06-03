<script setup lang="ts">
import { computed, type CSSProperties } from 'vue'

/* 16px stroke icons (currentColor). Set `fill="cur"` for filled glyphs.
   Path set ported verbatim from dock-kit.jsx. */
const PATHS: Record<string, string> = {
  overview: 'M2 2h5v5H2zM9 2h5v5H9zM2 9h5v5H2zM9 9h5v5H9z',
  sessions: 'M2 4.5h12M2 8h12M2 11.5h12',
  systems: 'M2 3.2h12v3.4H2zM2 9.4h12v3.4H2zM4.4 4.9h.01M4.4 11.1h.01',
  crew: 'M2.5 3h11v7h-7l-3 2.6z',
  knowledge: 'M3 2.5h7a2 2 0 0 1 2 2v9H5a2 2 0 0 1-2-2zM12 4.5h1.5v9H5',
  docs: 'M4 2h5l3 3v9H4zM9 2v3h3',
  diagnostics: 'M2 8.5h3l1.6-4 2.4 8 1.6-4H14',
  search: 'M7 12.5a5.5 5.5 0 1 0 0-11 5.5 5.5 0 0 0 0 11zM11 11l3 3',
  bell: 'M4 6.5a4 4 0 0 1 8 0c0 3 1.2 4 1.2 4H2.8S4 9.5 4 6.5zM6.4 13a1.8 1.8 0 0 0 3.2 0',
  chevron: 'M6 4l4 4-4 4',
  chevronD: 'M4 6l4 4 4-4',
  ext: 'M6 3H3v10h10v-3M9.5 2.5H13.5V6.5M13 3l-5.5 5.5',
  spark: 'M8 1.5l1.6 4.2 4.4.3-3.4 2.8 1.1 4.3L8 10.8 4.3 13l1.1-4.3L2 5.9l4.4-.3z',
  plus: 'M8 3v10M3 8h10',
  dot3: 'M4 8h.01M8 8h.01M12 8h.01',
  clock: 'M8 4v4l2.5 1.5M8 1.5a6.5 6.5 0 1 0 0 13 6.5 6.5 0 0 0 0-13z',
  pin: 'M8 1.5a4 4 0 0 1 4 4c0 3-4 9-4 9s-4-6-4-9a4 4 0 0 1 4-4zM8 7a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3z',
  arrowR: 'M3 8h10M9 4l4 4-4 4',
  check: 'M3 8.5l3.5 3.5L13 4.5',
  link: 'M6.5 9.5l3-3M5.5 7.5L4 9a2.5 2.5 0 0 0 3.5 3.5L9 11M10.5 8.5L12 7a2.5 2.5 0 0 0-3.5-3.5L7 5',
  filter: 'M2 3.5h12l-4.5 5v4l-3 1.5v-5.5z',
  cube: 'M8 1.8l5.5 3v6.4L8 14.2 2.5 11.2V4.8zM2.7 4.9L8 8l5.3-3.1M8 8v6',
  wave: 'M2 8h2l1.5-4 2 8 1.5-5 1.2 3H14',
}

const props = withDefaults(
  defineProps<{
    name: string
    size?: number
    stroke?: number
    /** 'cur' = filled with currentColor; otherwise stroked. */
    fill?: string
  }>(),
  { size: 16, stroke: 1.5, fill: 'none' },
)

const filled = computed(() => props.fill === 'cur')
const svgStyle: CSSProperties = { display: 'block', flex: '0 0 auto' }
</script>

<template>
  <svg
    :width="size"
    :height="size"
    viewBox="0 0 16 16"
    :fill="filled ? 'currentColor' : 'none'"
    :stroke="filled ? 'none' : 'currentColor'"
    :stroke-width="stroke"
    stroke-linecap="round"
    stroke-linejoin="round"
    :style="svgStyle"
  >
    <path :d="PATHS[name]" />
  </svg>
</template>
