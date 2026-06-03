<script setup lang="ts">
import { computed } from 'vue'
import { L, TF_LOGO } from '@/design/tokens'

const props = withDefaults(
  defineProps<{
    height?: number
    color?: string
  }>(),
  { height: 22, color: L.text },
)

const dims = computed(() => {
  const [, , vbW, vbH] = TF_LOGO.viewBox.split(' ').map(Number)
  return { w: props.height * (vbW / vbH), h: props.height }
})
</script>

<template>
  <svg
    :viewBox="TF_LOGO.viewBox"
    :height="dims.h"
    :width="dims.w"
    style="display: block"
    role="img"
    aria-label="TapeForge"
  >
    <path :fill="color" :d="TF_LOGO.d" />
  </svg>
</template>
