<script setup lang="ts">
import { computed, type CSSProperties } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import { L } from '@/design/tokens'
import { S } from '@/dock/status'
import { sessions, systems, knowledge } from '@/dock/data'
import Wordmark from '@/components/kit/Wordmark.vue'
import Icon from '@/components/kit/Icon.vue'
import DockDot from '@/components/kit/DockDot.vue'

interface NavItem {
  id: string
  label: string
  icon: string
  accent?: boolean
}

const NAV: NavItem[] = [
  { id: 'overview', label: 'Overview', icon: 'overview' },
  { id: 'sessions', label: 'Sessions', icon: 'sessions' },
  { id: 'systems', label: 'Systems', icon: 'systems' },
  { id: 'crew', label: 'Crew', icon: 'crew', accent: true },
  { id: 'knowledge', label: 'Knowledge', icon: 'knowledge' },
  { id: 'docs', label: 'Documentation', icon: 'docs' },
  { id: 'diagnostics', label: 'Diagnostics', icon: 'diagnostics' },
]

const counts: Record<string, number | undefined> = {
  sessions: sessions.length,
  systems: systems.length,
  knowledge: knowledge.length,
}

const route = useRoute()
const active = (id: string) => route.path === `/${id}` || route.path.startsWith(`/${id}/`)

const wrap: CSSProperties = {
  width: '232px',
  flex: '0 0 232px',
  background: L.pageBg,
  borderRight: `1px solid ${L.border}`,
  display: 'flex',
  flexDirection: 'column',
  height: '100%',
}
const brand: CSSProperties = {
  height: '64px',
  flex: '0 0 64px',
  display: 'flex',
  alignItems: 'center',
  gap: '9px',
  padding: '0 18px',
  borderBottom: `1px solid ${L.border}`,
}
const dockTag: CSSProperties = {
  fontFamily: L.mono,
  fontSize: '10px',
  fontWeight: 600,
  letterSpacing: '0.12em',
  color: S.accentText,
  background: S.accentBg,
  border: `1px solid ${S.accentBorder}`,
  borderRadius: '5px',
  padding: '2px 6px',
}
const orgWrap: CSSProperties = { padding: '12px 12px 8px' }
const orgCard: CSSProperties = {
  display: 'flex',
  alignItems: 'center',
  gap: '10px',
  padding: '8px 10px',
  borderRadius: '9px',
  border: `1px solid ${L.border}`,
  background: L.panel,
  cursor: 'pointer',
}
const navWrap: CSSProperties = { flex: 1, minHeight: 0, overflowY: 'auto', padding: '4px 12px' }
const footer: CSSProperties = {
  padding: '12px 18px',
  borderTop: `1px solid ${L.border}`,
  display: 'flex',
  alignItems: 'center',
  gap: '8px',
}

function itemStyle(on: boolean): CSSProperties {
  return {
    display: 'flex',
    alignItems: 'center',
    gap: '11px',
    padding: '8px 10px',
    borderRadius: '8px',
    cursor: 'pointer',
    marginBottom: '2px',
    textDecoration: 'none',
    background: on ? L.panel : 'transparent',
    border: `1px solid ${on ? L.border : 'transparent'}`,
    boxShadow: on ? '0 1px 2px rgba(16,24,40,0.04)' : 'none',
    color: on ? L.text : L.text2,
  }
}
const aiTag: CSSProperties = {
  fontFamily: L.mono,
  fontSize: '8px',
  fontWeight: 600,
  letterSpacing: '0.08em',
  color: S.accentText,
  background: S.accentBg,
  border: `1px solid ${S.accentBorder}`,
  borderRadius: '4px',
  padding: '1px 5px',
}
const navList = computed(() => NAV.map((n) => ({ ...n, on: active(n.id) })))
</script>

<template>
  <div :style="wrap">
    <div :style="brand">
      <Wordmark :height="26" :color="L.text" />
      <span :style="dockTag">DOCK</span>
    </div>

    <div :style="orgWrap">
      <div :style="orgCard">
        <span
          :style="{ width: '26px', height: '26px', borderRadius: '7px', background: L.text, color: '#fff', fontFamily: L.body, fontSize: '13px', fontWeight: 700, display: 'flex', alignItems: 'center', justifyContent: 'center' }"
          >N</span
        >
        <div :style="{ flex: 1, minWidth: 0 }">
          <div :style="{ fontFamily: L.body, fontSize: '12.5px', fontWeight: 700, color: L.text, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }">
            Northgate Audio
          </div>
          <div :style="{ fontFamily: L.mono, fontSize: '9px', color: L.text3 }">ORG · 4 locations</div>
        </div>
        <span :style="{ color: L.text3 }"><Icon name="chevronD" :size="13" /></span>
      </div>
    </div>

    <nav :style="navWrap">
      <RouterLink v-for="n in navList" :key="n.id" :to="`/${n.id}`" :style="itemStyle(n.on)">
        <span :style="{ color: n.on ? S.accent : L.text3, display: 'flex' }"><Icon :name="n.icon" :size="16" /></span>
        <span :style="{ fontFamily: L.body, fontSize: '13px', fontWeight: n.on ? 700 : 500, flex: 1 }">{{ n.label }}</span>
        <span v-if="n.accent" :style="aiTag">AI</span>
        <span v-else-if="counts[n.id] != null" :style="{ fontFamily: L.mono, fontSize: '9.5px', color: L.text3 }">{{ counts[n.id] }}</span>
      </RouterLink>
    </nav>

    <div :style="footer">
      <DockDot tone="ok" pulse />
      <span :style="{ fontFamily: L.mono, fontSize: '10px', color: L.text2 }">All systems nominal</span>
    </div>
  </div>
</template>
