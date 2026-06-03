<script setup lang="ts">
import { computed, type CSSProperties } from 'vue'
import { useRoute, RouterView } from 'vue-router'
import { L } from '@/design/tokens'
import AppSidebar from '@/components/shell/AppSidebar.vue'
import TopBar, { type Crumb } from '@/components/shell/TopBar.vue'

const route = useRoute()

// Sections that manage their own internal scroll / full-height layout.
const full = computed(() => route.meta.full === true)

const crumbs = computed<Crumb[]>(() => {
  const label = (route.meta.label as string) ?? 'Overview'
  // Session detail adds a trailing crumb for the session id.
  if (route.name === 'session-detail') {
    return [{ label: 'Sessions', to: '/sessions' }, { label: String(route.params.id) }]
  }
  return [{ label }]
})

const app: CSSProperties = {
  display: 'flex',
  height: '100vh',
  width: '100vw',
  overflow: 'hidden',
}
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
  overflowY: full.value ? 'hidden' : 'auto',
  background: full.value ? L.panel : L.pageBg,
  display: full.value ? 'flex' : 'block',
}))
</script>

<template>
  <div :style="app">
    <AppSidebar />
    <div :style="column">
      <TopBar :crumbs="crumbs" />
      <div class="dock-main" :style="main">
        <RouterView />
      </div>
    </div>
  </div>
</template>
