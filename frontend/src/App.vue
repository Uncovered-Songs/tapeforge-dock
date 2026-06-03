<script setup lang="ts">
import { computed, ref, type CSSProperties } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AppSidebar from '@/components/shell/AppSidebar.vue'
import AppColumn from '@/components/shell/AppColumn.vue'
import CrewRail from '@/components/shell/CrewRail.vue'
import CommandPalette from '@/components/shell/CommandPalette.vue'
import { type Crumb } from '@/components/shell/TopBar.vue'
import { narrate, type DockRoute } from '@/dock/crew'

const route = useRoute()
const router = useRouter()

// Crew rail / palette state.
const railExpanded = ref(true)
const cover = ref(true) // rail spans full height, framing the whole app
const lastNav = ref<string | null>(null)
const paletteOpen = ref(false)

// Current location as a section + sub (decoupled from the URL).
const dockRoute = computed<DockRoute>(() => {
  const name = String(route.name ?? 'overview')
  if (name === 'session-detail') return { section: 'sessions', sub: String(route.params.id) }
  if (name === 'systems') return { section: 'systems', sub: route.params.id ? String(route.params.id) : null }
  return { section: name, sub: null }
})
const onCrew = computed(() => route.name === 'crew')
const full = computed(() => route.meta.full === true)

function pathFor(section: string, sub?: string): string {
  switch (section) {
    case 'sessions':
      return sub ? `/sessions/${sub}` : '/sessions'
    case 'systems':
      return sub ? `/systems/${sub}` : '/systems'
    case 'overview':
    case 'crew':
    case 'knowledge':
    case 'docs':
    case 'diagnostics':
      return `/${section}`
    default:
      return '/overview'
  }
}

// Plain navigation clears Crew's narration.
function go(section: string, sub?: string) {
  lastNav.value = null
  router.push(pathFor(section, sub))
}
// Crew-driven navigation narrates where it took you.
function railGo(section: string, sub?: string) {
  lastNav.value = narrate(section, sub)
  router.push(pathFor(section, sub))
}

const crumbs = computed<Crumb[]>(() => {
  if (route.name === 'session-detail') {
    return [{ label: 'Sessions', to: '/sessions' }, { label: String(route.params.id) }]
  }
  return [{ label: (route.meta.label as string) ?? 'Overview' }]
})

const app: CSSProperties = { display: 'flex', height: '100vh', width: '100vw', overflow: 'hidden' }
const coverWrap: CSSProperties = { flex: 1, minWidth: 0, display: 'flex', height: '100%' }
</script>

<template>
  <div :style="app">
    <!-- cover: the Crew rail frames the whole app (sidebar + top bar) -->
    <template v-if="cover && !onCrew">
      <CrewRail
        :route="dockRoute"
        :go="railGo"
        :expanded="railExpanded"
        :cover="cover"
        :last-nav="lastNav"
        @toggle-expanded="railExpanded = !railExpanded"
        @toggle-cover="cover = !cover"
        @expand="railExpanded = true"
      />
      <div :style="coverWrap">
        <AppSidebar />
        <AppColumn :crumbs="crumbs" :full="full" @open-palette="paletteOpen = true" />
      </div>
    </template>

    <!-- non-cover (or Crew workspace): rail sits beside the content -->
    <template v-else>
      <AppSidebar />
      <CrewRail
        v-if="!onCrew"
        :route="dockRoute"
        :go="railGo"
        :expanded="railExpanded"
        :cover="cover"
        :last-nav="lastNav"
        @toggle-expanded="railExpanded = !railExpanded"
        @toggle-cover="cover = !cover"
        @expand="railExpanded = true"
      />
      <AppColumn :crumbs="crumbs" :full="full" @open-palette="paletteOpen = true" />
    </template>

    <CommandPalette v-model:open="paletteOpen" :go="go" />
  </div>
</template>
