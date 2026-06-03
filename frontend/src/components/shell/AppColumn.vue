<script setup lang="ts">
import { computed, type CSSProperties } from 'vue'
import { RouterView } from 'vue-router'
import { L } from '@/design/tokens'
import TopBar, { type Crumb } from './TopBar.vue'

const props = defineProps<{ crumbs: Crumb[]; full: boolean }>()
const emit = defineEmits<{ 'open-palette': [] }>()

const column: CSSProperties = {
  flex: 1,
  minWidth: 0,
  display: 'flex',
  flexDirection: 'column',
  height: '100%',
  position: 'relative',
}
const main = computed<CSSProperties>(() => ({
  flex: 1,
  minHeight: 0,
  overflowY: props.full ? 'hidden' : 'auto',
  background: props.full ? L.panel : L.pageBg,
  display: props.full ? 'flex' : 'block',
}))
</script>

<template>
  <div :style="column">
    <TopBar :crumbs="crumbs" @open-palette="emit('open-palette')" />
    <div class="dock-main" :style="main">
      <RouterView />
    </div>
  </div>
</template>
