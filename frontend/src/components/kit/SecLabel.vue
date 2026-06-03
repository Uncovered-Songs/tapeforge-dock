<script setup lang="ts">
import type { CSSProperties } from 'vue'
import { L } from '@/design/tokens'

/* Small uppercase mono section label. Parent :style merges via fallthrough. */
const style: CSSProperties = {
  fontFamily: L.mono,
  fontSize: '10px',
  letterSpacing: '0.14em',
  color: L.text3,
  textTransform: 'uppercase',
}
</script>

<template>
  <div :style="style"><slot /></div>
</template>
