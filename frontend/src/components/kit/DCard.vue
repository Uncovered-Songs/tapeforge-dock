<script setup lang="ts">
import { computed, ref, type CSSProperties } from 'vue'
import { L } from '@/design/tokens'

/* Panel card with an optional title bar. Use the `action` slot for the
   right-aligned header control, default slot for the body. */
const props = withDefaults(
  defineProps<{
    title?: string
    pad?: number
    hover?: boolean
    clickable?: boolean
    bodyStyle?: CSSProperties
  }>(),
  { pad: 18 },
)

const emit = defineEmits<{ click: [] }>()
const slots = defineSlots<{ default(): unknown; action?(): unknown }>()

const hovered = ref(false)

const root = computed<CSSProperties>(() => ({
  background: L.panel,
  border: `1px solid ${props.hover && hovered.value ? L.border2 : L.border}`,
  borderRadius: '12px',
  boxShadow:
    props.hover && hovered.value
      ? '0 4px 16px rgba(16,24,40,0.07)'
      : '0 1px 2px rgba(16,24,40,0.04)',
  cursor: props.clickable ? 'pointer' : 'default',
  transition: 'box-shadow .16s, border-color .16s',
  display: 'flex',
  flexDirection: 'column',
}))

const head: CSSProperties = {
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'space-between',
  padding: '13px 16px',
  borderBottom: `1px solid ${L.border}`,
}
const titleStyle: CSSProperties = {
  fontFamily: L.body,
  fontSize: '13px',
  fontWeight: 700,
  letterSpacing: '0.01em',
  color: L.text,
}
const body = computed<CSSProperties>(() => ({
  padding: `${props.pad}px`,
  flex: 1,
  minHeight: 0,
  ...props.bodyStyle,
}))
</script>

<template>
  <div
    :style="root"
    @click="emit('click')"
    @mouseenter="hovered = true"
    @mouseleave="hovered = false"
  >
    <div v-if="title || slots.action" :style="head">
      <span :style="titleStyle">{{ title }}</span>
      <slot name="action" />
    </div>
    <div :style="body"><slot /></div>
  </div>
</template>
