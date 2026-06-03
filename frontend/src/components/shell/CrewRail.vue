<script setup lang="ts">
import type { CSSProperties } from 'vue'
import { S } from '@/dock/status'
import type { DockRoute } from '@/dock/crew'
import Icon from '@/components/kit/Icon.vue'
import CrewPanel from './CrewPanel.vue'

const props = defineProps<{
  route: DockRoute
  go: (section: string, sub?: string) => void
  expanded: boolean
  cover: boolean
  lastNav: string | null
}>()
const emit = defineEmits<{ 'toggle-expanded': []; 'toggle-cover': []; expand: [] }>()

const railStyle: CSSProperties = {
  width: '56px',
  flex: '0 0 56px',
  background: S.accent,
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  padding: '14px 0 12px',
}
function crewToggleStyle(): CSSProperties {
  return {
    width: '36px',
    height: '36px',
    borderRadius: '10px',
    background: props.expanded ? '#fff' : 'rgba(255,255,255,0.16)',
    color: props.expanded ? S.accentText : '#fff',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    cursor: 'pointer',
    transition: 'all .15s',
  }
}
const agentDot = (bg: string, anim = false): CSSProperties => ({
  width: '9px',
  height: '9px',
  borderRadius: '5px',
  background: bg,
  ...(anim ? { animation: 'dock-pulse 1s ease-in-out infinite' } : {}),
})
</script>

<template>
  <div :style="{ display: 'flex', height: '100%', flex: '0 0 auto' }">
    <!-- slim accent rail -->
    <div :style="railStyle">
      <span title="Crew" :style="crewToggleStyle()" @click="emit('toggle-expanded')"><Icon name="spark" :size="18" fill="cur" /></span>
      <div :style="{ width: '26px', height: '1px', background: 'rgba(255,255,255,0.2)', margin: '14px 0' }" />

      <!-- working agents -->
      <div :style="{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '10px' }">
        <span title="Networking · working" :style="agentDot('#fff', true)" />
        <span title="Topology · done" :style="{ ...agentDot('#fff'), opacity: 0.9 }" />
        <span title="Documentation · queued" :style="agentDot('rgba(255,255,255,0.4)')" />
      </div>

      <div :style="{ flex: 1 }" />

      <!-- insight badge -->
      <span
        title="1 new insight — recurring clock drift"
        :style="{ width: '30px', height: '30px', borderRadius: '9px', background: '#fff', color: S.accentText, fontFamily: 'JetBrains Mono, monospace', fontSize: '12px', fontWeight: 700, display: 'flex', alignItems: 'center', justifyContent: 'center', cursor: 'pointer', position: 'relative', marginBottom: '14px' }"
        @click="emit('expand')"
      >
        1<span :style="{ position: 'absolute', top: '-2px', right: '-2px', width: '9px', height: '9px', borderRadius: '5px', background: S.warn, border: `1.5px solid ${S.accent}` }" />
      </span>

      <span :style="{ writingMode: 'vertical-rl', transform: 'rotate(180deg)', fontFamily: 'JetBrains Mono, monospace', fontSize: '9.5px', letterSpacing: '0.2em', color: 'rgba(255,255,255,0.9)' }">CREW</span>

      <!-- coverage toggle -->
      <div :style="{ marginTop: '14px', display: 'flex', flexDirection: 'column', gap: '5px' }">
        <span
          :title="cover ? 'Crew spans full height (covers top bar)' : 'Crew sits below the top bar'"
          :style="{ width: '28px', height: '22px', borderRadius: '6px', background: 'rgba(255,255,255,0.16)', display: 'flex', alignItems: 'center', justifyContent: 'center', cursor: 'pointer' }"
          @click="emit('toggle-cover')"
        >
          <svg width="16" height="14" viewBox="0 0 16 14" fill="none" stroke="#fff" stroke-width="1.3">
            <rect x="1" y="1" width="14" height="12" rx="1.5" />
            <line x1="1" :y1="cover ? '1' : '4.5'" x2="15" :y2="cover ? '1' : '4.5'" stroke="#fff" :stroke-width="cover ? '0' : '1.3'" />
            <rect x="1" y="1" width="5" height="12" fill="#fff" opacity="0.5" />
          </svg>
        </span>
      </div>
    </div>

    <!-- expanded panel -->
    <CrewPanel v-if="expanded" :route="route" :go="go" :last-nav="lastNav" @close="emit('toggle-expanded')" />
  </div>
</template>
