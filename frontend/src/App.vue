<script setup lang="ts">
import { computed, onMounted, ref, watch, type CSSProperties } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { L } from '@/design/tokens'
import { S } from '@/dock/status'
import { useBreakpoint } from '@/composables/useBreakpoint'
import { useDockStore } from '@/stores/dock'
import AppSidebar from '@/components/shell/AppSidebar.vue'
import AppColumn from '@/components/shell/AppColumn.vue'
import CrewRail from '@/components/shell/CrewRail.vue'
import CrewPanel from '@/components/shell/CrewPanel.vue'
import CommandPalette from '@/components/shell/CommandPalette.vue'
import Wordmark from '@/components/kit/Wordmark.vue'
import Icon from '@/components/kit/Icon.vue'
import { type Crumb } from '@/components/shell/TopBar.vue'
import { narrate, type DockRoute } from '@/dock/crew'

const route = useRoute()
const router = useRouter()
const { isDesktop } = useBreakpoint()

// Load the operational dataset once, before rendering the console.
const store = useDockStore()
onMounted(() => {
  if (!store.loaded) store.load()
})

// Desktop Crew rail state.
const railExpanded = ref(true)
const cover = ref(true) // rail spans full height, framing the whole app
// Compact (tablet/phone) overlays.
const navOpen = ref(false) // sidebar drawer
const crewOpen = ref(false) // Crew panel overlay
const paletteOpen = ref(false)
const lastNav = ref<string | null>(null)

// Close transient overlays whenever the route changes (e.g. drawer nav tap).
watch(
  () => route.fullPath,
  () => {
    navOpen.value = false
  },
)

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

// Compact overlay chrome.
const scrim: CSSProperties = {
  position: 'fixed',
  inset: '0',
  zIndex: 70,
  background: 'rgba(20,24,28,0.38)',
  backdropFilter: 'blur(1px)',
}
const drawer: CSSProperties = {
  position: 'fixed',
  top: '0',
  left: '0',
  height: '100%',
  zIndex: 71,
  display: 'flex',
  boxShadow: '0 0 40px rgba(16,24,40,0.18)',
}
const crewOverlay = computed<CSSProperties>(() => ({
  position: 'fixed',
  top: '0',
  right: '0',
  height: '100%',
  width: '100%',
  maxWidth: '520px',
  zIndex: 71,
  display: 'flex',
  boxShadow: '0 0 40px rgba(16,24,40,0.18)',
}))
const fab: CSSProperties = {
  position: 'fixed',
  right: '18px',
  bottom: '18px',
  zIndex: 60,
  width: '52px',
  height: '52px',
  borderRadius: '16px',
  border: 'none',
  background: S.accent,
  color: '#fff',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  cursor: 'pointer',
  boxShadow: '0 8px 24px rgba(60,122,111,0.4)',
}

// Loading / error gate (shown until the dataset is in).
const gate: CSSProperties = {
  height: '100vh',
  width: '100vw',
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  justifyContent: 'center',
  gap: '18px',
  background: L.pageBg,
}
const spinner: CSSProperties = {
  width: '30px',
  height: '30px',
  borderRadius: '50%',
  border: `3px solid ${L.border}`,
  borderTopColor: S.accent,
  animation: 'dock-spin 0.8s linear infinite',
}
const gateMsg: CSSProperties = {
  margin: 0,
  fontFamily: L.mono,
  fontSize: '12px',
  letterSpacing: '0.06em',
  color: L.text3,
}
const retryBtn: CSSProperties = {
  fontFamily: L.body,
  fontSize: '13px',
  fontWeight: 600,
  cursor: 'pointer',
  padding: '8px 16px',
  borderRadius: '8px',
  border: `1px solid ${S.accent}`,
  background: S.accent,
  color: '#fff',
}
</script>

<template>
  <!-- ===================== Loading / error gate ===================== -->
  <div v-if="!store.loaded" :style="gate">
    <template v-if="store.error">
      <Wordmark :height="30" :color="L.text" />
      <p :style="gateMsg">{{ store.error }}</p>
      <button :style="retryBtn" @click="store.load()">Retry</button>
    </template>
    <template v-else>
      <div :style="spinner" />
      <p :style="gateMsg">Loading Dock…</p>
    </template>
  </div>

  <!-- ===================== Desktop ===================== -->
  <div v-else-if="isDesktop" :style="app">
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

  <!-- ===================== Tablet / phone ===================== -->
  <div v-else :style="app">
    <AppColumn
      :crumbs="crumbs"
      :full="full"
      @open-palette="paletteOpen = true"
      @open-nav="navOpen = true"
    />

    <!-- sidebar drawer -->
    <template v-if="navOpen">
      <div :style="scrim" @click="navOpen = false" />
      <div :style="drawer"><AppSidebar @navigate="navOpen = false" /></div>
    </template>

    <!-- floating Crew button -->
    <button v-if="!onCrew && !crewOpen" :style="fab" aria-label="Open Crew" @click="crewOpen = true">
      <Icon name="spark" :size="22" fill="cur" />
      <span :style="{ position: 'absolute', top: '8px', right: '8px', width: '9px', height: '9px', borderRadius: '5px', background: S.warn, border: `1.5px solid ${S.accent}` }" />
    </button>

    <!-- Crew panel overlay -->
    <template v-if="crewOpen">
      <div :style="scrim" @click="crewOpen = false" />
      <div :style="crewOverlay">
        <CrewPanel :route="dockRoute" :go="railGo" :last-nav="lastNav" @close="crewOpen = false" />
      </div>
    </template>

    <CommandPalette v-model:open="paletteOpen" :go="go" />
  </div>
</template>
