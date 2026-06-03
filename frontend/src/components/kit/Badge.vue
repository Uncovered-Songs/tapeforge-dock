<script setup lang="ts">
import { computed, type CSSProperties } from 'vue'
import { L, TWO } from '@/design/tokens'
import { S } from '@/dock/status'

/* Two-letter product badge (CO/DO/DE/RI/CA/SC/CR…). */
const props = withDefaults(
  defineProps<{ id?: string; size?: number; fs?: number }>(),
  { size: 22, fs: 9.5 },
)

const label = computed(() => TWO[props.id ?? ''] ?? (props.id ?? '··').slice(0, 2).toUpperCase())

const style = computed<CSSProperties>(() => ({
  width: `${props.size}px`,
  height: `${props.size}px`,
  borderRadius: '5px',
  flex: '0 0 auto',
  background: S.accentBg,
  border: `1px solid ${S.accentBorder}`,
  color: S.accentText,
  fontFamily: L.mono,
  fontSize: `${props.fs}px`,
  fontWeight: 600,
  display: 'inline-flex',
  alignItems: 'center',
  justifyContent: 'center',
  letterSpacing: '0.02em',
}))
</script>

<template>
  <span :style="style">{{ label }}</span>
</template>
