<script setup lang="ts">
import { computed, type CSSProperties } from 'vue'
import { L } from '@/design/tokens'
import { S } from '@/dock/status'
import Icon from './Icon.vue'

const props = withDefaults(
  defineProps<{ primary?: boolean; sm?: boolean; icon?: string }>(),
  {},
)
const emit = defineEmits<{ click: [] }>()

const style = computed<CSSProperties>(() => ({
  display: 'inline-flex',
  alignItems: 'center',
  gap: '7px',
  fontFamily: L.body,
  fontSize: props.sm ? '12.5px' : '13px',
  fontWeight: 600,
  cursor: 'pointer',
  padding: props.sm ? '6px 11px' : '8px 14px',
  borderRadius: '8px',
  whiteSpace: 'nowrap',
  border: `1px solid ${props.primary ? S.accent : L.border2}`,
  background: props.primary ? S.accent : L.panel,
  color: props.primary ? '#fff' : L.text2,
}))
</script>

<template>
  <button :style="style" @click="emit('click')">
    <Icon v-if="icon" :name="icon" :size="14" />
    <slot />
  </button>
</template>
