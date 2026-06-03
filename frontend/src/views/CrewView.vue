<script setup lang="ts">
import { computed, ref, type CSSProperties } from 'vue'
import { useRouter } from 'vue-router'
import { L } from '@/design/tokens'
import { useBreakpoint } from '@/composables/useBreakpoint'
import { S } from '@/dock/status'
import { type CrewTurn } from '@/dock/data'
import { useDockStore } from '@/stores/dock'
import Pill from '@/components/kit/Pill.vue'
import Icon from '@/components/kit/Icon.vue'
import SecLabel from '@/components/kit/SecLabel.vue'
import Btn from '@/components/kit/Btn.vue'

const router = useRouter()
const { isMobile, isCompact } = useBreakpoint()
const { crewThread, systems, sessions, knowledge } = useDockStore()

/* Horizontal padding shrinks on narrow viewports to avoid overflow. */
const padX = computed(() => (isMobile.value ? '14px' : '26px'))

const headerStyle = computed<CSSProperties>(() => ({
  display: 'flex',
  alignItems: 'center',
  gap: '11px',
  padding: `16px ${padX.value}`,
  borderBottom: `1px solid ${L.border}`,
}))
const threadScrollStyle = computed<CSSProperties>(() => ({
  flex: 1,
  minHeight: 0,
  overflowY: 'auto',
  padding: `24px ${padX.value}`,
}))
const composerStyle = computed<CSSProperties>(() => ({
  padding: isMobile.value ? '12px 14px 16px' : '14px 26px 20px',
  borderTop: `1px solid ${L.border}`,
}))
/* Agent-mesh sidebar: hidden on compact (tablet + mobile), narrower otherwise stays as-is on desktop. */
const meshStyle = computed<CSSProperties>(() => ({
  width: '264px',
  flex: '0 0 264px',
  borderLeft: `1px solid ${L.border}`,
  background: L.pageBg,
  padding: '18px 16px',
  overflowY: 'auto',
}))

/* Map a crew nav target (from cites / mesh / sources) to a router path. */
function go(to: string): void {
  switch (to) {
    case 'session':
      router.push('/sessions/S-2040')
      break
    case 'sessions':
      router.push('/sessions')
      break
    case 'systems':
      router.push('/systems')
      break
    case 'knowledge':
      router.push('/knowledge')
      break
    case 'docs':
      router.push('/docs')
      break
    case 'diagnostics':
      router.push('/diagnostics')
      break
    case 'crew':
      router.push('/crew')
      break
    default:
      router.push('/overview')
  }
}

interface Agent {
  name: string
  to: string
  state: 'work' | 'done' | 'queued' | 'idle'
  note: string
  pct?: number
}

const AGENTS: Agent[] = [
  { name: 'Deployment History', to: 'sessions', state: 'work', note: 'scanning 6 sessions…', pct: 64 },
  { name: 'Troubleshooting', to: 'diagnostics', state: 'work', note: 'matching clock events…', pct: 41 },
  { name: 'Networking', to: 'diagnostics', state: 'done', note: '3 PTP events found' },
  { name: 'Topology', to: 'systems', state: 'done', note: '2 grandmasters flagged' },
  { name: 'Documentation', to: 'docs', state: 'queued', note: 'queued' },
  { name: 'Audio Systems', to: 'crew', state: 'idle', note: 'idle' },
]

const SUGGEST: string[] = [
  'Compare today’s config with last week’s',
  'Show all sessions with AES67 clock problems',
  'Explain the Riverside routing topology',
  'Which systems need a software update?',
]

/* Sources gathered so far — [navTarget, label, count]. */
const SOURCES: Array<[string, string, string]> = [
  ['sessions', 'S-2041, S-2038 +1', '3'],
  ['knowledge', 'clock topology playbook', '1'],
]

/* What Crew knows — [navTarget, label]. */
const SCOPE: Array<[string, string]> = [
  ['systems', `${systems.length} systems`],
  ['sessions', `${sessions.length} sessions`],
  ['knowledge', `${knowledge.length} knowledge docs`],
  ['docs', '4 doc sections'],
]
function scopeIcon(to: string): string {
  return to === 'systems' ? 'systems' : to === 'sessions' ? 'sessions' : to === 'knowledge' ? 'knowledge' : 'docs'
}

const thread: CrewTurn[] = crewThread

/* Non-functional composer state (first UI pass). */
const draft = ref('')
</script>

<template>
  <div :style="{ flex: 1, minWidth: 0, display: 'flex', flexDirection: 'column', minHeight: 0, height: '100%' }">
    <div :style="{ display: 'flex', flex: 1, width: '100%', minHeight: 0 }">
      <!-- conversation -->
      <div :style="{ flex: 1, minWidth: 0, display: 'flex', flexDirection: 'column', minHeight: 0 }">
        <div :style="headerStyle">
          <span :style="{ width: '32px', height: '32px', borderRadius: '9px', background: S.accent, color: '#fff', display: 'flex', alignItems: 'center', justifyContent: 'center' }"><Icon name="spark" :size="17" fill="cur" /></span>
          <div>
            <div :style="{ fontFamily: L.body, fontSize: '15px', fontWeight: 700, color: L.text }">Crew</div>
            <div :style="{ fontFamily: L.mono, fontSize: '10px', color: L.text3 }">Operational assistant · orchestrating 6 agents</div>
          </div>
          <div :style="{ flex: 1 }" />
          <Pill tone="ok">online</Pill>
        </div>

        <!-- thread -->
        <div :style="threadScrollStyle">
          <div :style="{ maxWidth: '760px', margin: '0 auto', display: 'flex', flexDirection: 'column', gap: '22px' }">
            <template v-for="(m, i) in thread" :key="i">
              <div
                v-if="m.role === 'user'"
                :style="{ alignSelf: 'flex-end', maxWidth: '78%', background: S.accent, color: '#fff', borderRadius: '12px 12px 4px 12px', padding: '12px 15px 13px', fontFamily: L.body, fontSize: '14px', lineHeight: 1.55 }"
              >{{ m.text }}</div>
              <div v-else :style="{ display: 'flex', gap: '12px' }">
                <span :style="{ width: '28px', height: '28px', borderRadius: '8px', background: S.accentBg, border: `1px solid ${S.accentBorder}`, color: S.accentText, display: 'flex', alignItems: 'center', justifyContent: 'center', flex: '0 0 auto', marginTop: '2px' }"><Icon name="spark" :size="15" fill="cur" /></span>
                <div :style="{ minWidth: 0 }">
                  <div v-if="m.agents" :style="{ display: 'flex', gap: '6px', marginBottom: '8px' }">
                    <span
                      v-for="a in m.agents"
                      :key="a"
                      :style="{ fontFamily: L.mono, fontSize: '9px', fontWeight: 600, letterSpacing: '0.04em', color: L.text3, background: L.pageBg, border: `1px solid ${L.border}`, borderRadius: '5px', padding: '2px 7px' }"
                    >{{ a }} agent</span>
                  </div>
                  <p :style="{ margin: 0, fontFamily: L.body, fontSize: '14px', lineHeight: 1.6, color: L.text }">{{ m.text }}</p>
                  <div v-if="m.cites" :style="{ display: 'flex', flexWrap: 'wrap', gap: '8px', marginTop: '12px' }">
                    <span
                      v-for="(c, j) in m.cites"
                      :key="j"
                      :style="{ display: 'inline-flex', alignItems: 'center', gap: '6px', fontFamily: L.mono, fontSize: '10.5px', color: S.accentText, background: L.panel, border: `1px solid ${L.border2}`, borderRadius: '7px', padding: '5px 9px', cursor: 'pointer' }"
                      @click="go(c.to)"
                    >
                      <Icon name="link" :size="12" />{{ c.t }}
                    </span>
                  </div>
                </div>
              </div>
            </template>

            <!-- suggestions -->
            <div :style="{ marginTop: '4px' }">
              <SecLabel :style="{ marginBottom: '10px' }">Suggested</SecLabel>
              <div :style="{ display: 'flex', flexWrap: 'wrap', gap: '9px' }">
                <span
                  v-for="q in SUGGEST"
                  :key="q"
                  :style="{ fontFamily: L.body, fontSize: '12.5px', color: L.text2, background: L.panel, border: `1px solid ${L.border}`, borderRadius: '8px', padding: '8px 12px', cursor: 'pointer' }"
                >{{ q }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- composer -->
        <div :style="composerStyle">
          <div :style="{ maxWidth: '760px', margin: '0 auto', display: 'flex', alignItems: 'center', gap: '10px', padding: '11px 14px', borderRadius: '11px', border: `1px solid ${L.border2}`, background: L.panel, boxShadow: '0 1px 2px rgba(16,24,40,0.04)' }">
            <Icon name="spark" :size="16" :style="{ color: L.text3 }" />
            <input
              v-model="draft"
              type="text"
              placeholder="Ask about systems, sessions, topology, networking…"
              :style="{ flex: 1, minWidth: 0, border: 'none', outline: 'none', background: 'transparent', fontFamily: L.body, fontSize: '14px', color: L.text }"
            />
            <span v-if="!isMobile" :style="{ fontFamily: L.mono, fontSize: '9.5px', color: L.text3, border: `1px solid ${L.border}`, borderRadius: '5px', padding: '3px 7px' }">cites sources</span>
            <Btn primary sm icon="arrowR">Ask</Btn>
          </div>
        </div>
      </div>

      <!-- agent mesh sidebar — live orchestration ("working") state. Hidden on compact (tablet + mobile): no room beside the thread. -->
      <div v-if="!isCompact" :style="meshStyle">
        <div :style="{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px' }">
          <SecLabel>Agent mesh</SecLabel>
          <span :style="{ display: 'inline-flex', alignItems: 'center', gap: '6px', fontFamily: L.mono, fontSize: '9px', fontWeight: 600, letterSpacing: '0.06em', color: S.accentText, background: S.accentBg, border: `1px solid ${S.accentBorder}`, borderRadius: '5px', padding: '2px 7px' }">
            <span :style="{ width: '6px', height: '6px', borderRadius: '3px', background: S.accent, animation: 'dock-pulse 1.1s ease-in-out infinite' }" />PROCESSING
          </span>
        </div>

        <!-- current task -->
        <div :style="{ background: L.panel, border: `1px solid ${L.border}`, borderRadius: '10px', padding: '11px 12px', marginBottom: '14px' }">
          <div :style="{ fontFamily: L.mono, fontSize: '8.5px', letterSpacing: '0.1em', color: L.text3, marginBottom: '5px' }">ORCHESTRATING</div>
          <div :style="{ fontFamily: L.body, fontSize: '12px', fontWeight: 600, color: L.text, lineHeight: 1.4 }">“Has this happened before at Riverside Arena?”</div>
          <div :style="{ position: 'relative', height: '3px', background: L.border, borderRadius: '2px', marginTop: '10px', overflow: 'hidden' }">
            <div :style="{ position: 'absolute', left: 0, top: 0, bottom: 0, width: '58%', background: S.accent, borderRadius: '2px' }" />
          </div>
          <div :style="{ display: 'flex', justifyContent: 'space-between', marginTop: '6px', fontFamily: L.mono, fontSize: '9px', color: L.text3 }">
            <span>2 of 4 agents done</span><span>1.4s</span>
          </div>
        </div>

        <!-- agents with live state -->
        <div :style="{ display: 'flex', flexDirection: 'column', gap: '7px', marginBottom: '14px' }">
          <div
            v-for="a in AGENTS"
            :key="a.name"
            :style="{ display: 'flex', alignItems: 'center', gap: '9px', padding: '9px 11px', borderRadius: '9px', border: `1px solid ${a.state === 'work' ? S.accentBorder : L.border}`, background: a.state === 'work' ? S.accentBg : L.panel, cursor: 'pointer', opacity: a.state === 'idle' ? 0.55 : 1 }"
            @click="go(a.to)"
          >
            <!-- status glyph -->
            <svg v-if="a.state === 'work'" width="13" height="13" viewBox="0 0 13 13" :style="{ flex: '0 0 auto', animation: 'dock-spin 0.9s linear infinite' }">
              <circle cx="6.5" cy="6.5" r="5" fill="none" :stroke="S.accentBorder" stroke-width="2" />
              <path d="M6.5 1.5a5 5 0 0 1 5 5" fill="none" :stroke="S.accent" stroke-width="2" stroke-linecap="round" />
            </svg>
            <span v-else-if="a.state === 'done'" :style="{ width: '13px', height: '13px', borderRadius: '7px', background: S.ok, display: 'flex', alignItems: 'center', justifyContent: 'center', flex: '0 0 auto' }">
              <Icon name="check" :size="8" :stroke="2.2" :style="{ color: '#fff' }" />
            </span>
            <span v-else :style="{ width: '7px', height: '7px', borderRadius: '4px', background: L.border2, flex: '0 0 auto', margin: '0 3px' }" />
            <div :style="{ flex: 1, minWidth: 0 }">
              <div :style="{ fontFamily: L.body, fontSize: '12px', fontWeight: 600, color: L.text }">{{ a.name }}</div>
              <div :style="{ fontFamily: L.mono, fontSize: '9px', color: a.state === 'work' ? S.accentText : a.state === 'done' ? S.ok : L.text3, marginTop: '1px' }">{{ a.note }}</div>
            </div>
          </div>
        </div>

        <!-- sources gathered so far -->
        <div :style="{ background: L.panel, border: `1px solid ${L.border}`, borderRadius: '10px', padding: '11px 12px', marginBottom: '14px' }">
          <div :style="{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '9px' }">
            <SecLabel>Sources gathered</SecLabel>
            <span :style="{ fontFamily: L.mono, fontSize: '11px', fontWeight: 600, color: S.accentText }">4</span>
          </div>
          <div
            v-for="r in SOURCES"
            :key="r[0]"
            :style="{ display: 'flex', alignItems: 'center', gap: '8px', padding: '5px 0', cursor: 'pointer' }"
            @click="go(r[0])"
          >
            <Icon :name="r[0] === 'sessions' ? 'sessions' : 'knowledge'" :size="13" :style="{ color: L.text3, flex: '0 0 auto' }" />
            <span :style="{ flex: 1, minWidth: 0, fontFamily: L.mono, fontSize: '10px', color: L.text2, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }">{{ r[1] }}</span>
            <span :style="{ fontFamily: L.mono, fontSize: '10px', color: L.text3 }">{{ r[2] }}</span>
          </div>
        </div>

        <!-- scope -->
        <SecLabel :style="{ marginBottom: '10px' }">Crew knows</SecLabel>
        <div :style="{ display: 'flex', flexDirection: 'column', gap: '9px' }">
          <div
            v-for="r in SCOPE"
            :key="r[0]"
            :style="{ display: 'flex', alignItems: 'center', gap: '9px', fontFamily: L.mono, fontSize: '10.5px', color: L.text2, cursor: 'pointer' }"
            @click="go(r[0])"
          >
            <Icon :name="scopeIcon(r[0])" :size="13" :style="{ color: L.text3 }" />{{ r[1] }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
