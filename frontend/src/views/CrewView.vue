<script setup lang="ts">
import { computed, nextTick, ref, type CSSProperties } from 'vue'
import { useRouter } from 'vue-router'
import { L } from '@/design/tokens'
import { useBreakpoint } from '@/composables/useBreakpoint'
import { S } from '@/dock/status'
import { streamCrewChat, type CrewMessage } from '@/dock/api'
import { useDockStore } from '@/stores/dock'
import Pill from '@/components/kit/Pill.vue'
import Icon from '@/components/kit/Icon.vue'
import SecLabel from '@/components/kit/SecLabel.vue'
import Btn from '@/components/kit/Btn.vue'

const router = useRouter()
const { isMobile, isCompact } = useBreakpoint()
const { systems, sessions, knowledge } = useDockStore()

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
const meshStyle = computed<CSSProperties>(() => ({
  width: '264px',
  flex: '0 0 264px',
  borderLeft: `1px solid ${L.border}`,
  background: L.pageBg,
  padding: '18px 16px',
  overflowY: 'auto',
}))

// --- live conversation -----------------------------------------------------

interface NavTarget {
  section: string
  sub: string | null
}
interface ChatTurn {
  role: 'user' | 'crew'
  text: string
  streaming?: boolean
  error?: boolean
  navs: NavTarget[]
}

const conversation = ref<ChatTurn[]>([])
const draft = ref('')
const sending = ref(false)
const threadEl = ref<HTMLElement | null>(null)

function scrollSoon(): void {
  nextTick(() => {
    if (threadEl.value) threadEl.value.scrollTop = threadEl.value.scrollHeight
  })
}

function pathFor(section: string, sub: string | null): string {
  switch (section) {
    case 'sessions':
      return sub ? `/sessions/${sub}` : '/sessions'
    case 'systems':
      return sub ? `/systems/${sub}` : '/systems'
    default:
      return `/${section}`
  }
}
function navLabel(nav: NavTarget): string {
  const label = nav.section.charAt(0).toUpperCase() + nav.section.slice(1)
  return nav.sub ? `${label} · ${nav.sub}` : label
}
function openNav(nav: NavTarget): void {
  router.push(pathFor(nav.section, nav.sub))
}

async function send(text: string): Promise<void> {
  const q = text.trim()
  if (!q || sending.value) return

  conversation.value.push({ role: 'user', text: q, navs: [] })
  conversation.value.push({ role: 'crew', text: '', streaming: true, navs: [] })
  const idx = conversation.value.length - 1
  draft.value = ''
  sending.value = true
  scrollSoon()

  const history: CrewMessage[] = conversation.value.slice(0, idx).map((m) => ({
    role: m.role === 'user' ? 'user' : 'assistant',
    content: m.text,
  }))

  await streamCrewChat(history, null, {
    onText: (t) => {
      conversation.value[idx].text += t
      scrollSoon()
    },
    onNavigate: (section, sub) => {
      conversation.value[idx].navs.push({ section, sub })
    },
    onError: (msg) => {
      const c = conversation.value[idx]
      if (!c.text) {
        c.text = msg
        c.error = true
      }
    },
    onDone: () => {},
  })

  conversation.value[idx].streaming = false
  sending.value = false
  scrollSoon()
}

/* Map a mesh / scope click to a route. */
function go(to: string): void {
  router.push(to === 'session' ? '/sessions/S-2040' : `/${to}`)
}

interface Agent {
  name: string
  to: string
  state: 'work' | 'done' | 'queued' | 'idle'
  note: string
}
const AGENTS: Agent[] = [
  { name: 'Deployment History', to: 'sessions', state: 'work', note: 'scanning 6 sessions…' },
  { name: 'Troubleshooting', to: 'diagnostics', state: 'work', note: 'matching clock events…' },
  { name: 'Networking', to: 'diagnostics', state: 'done', note: '3 PTP events found' },
  { name: 'Topology', to: 'systems', state: 'done', note: '2 grandmasters flagged' },
  { name: 'Documentation', to: 'docs', state: 'queued', note: 'queued' },
  { name: 'Audio Systems', to: 'crew', state: 'idle', note: 'idle' },
]

const SUGGEST: string[] = [
  'What needs my attention right now?',
  'Why is SCOPE-Broadcast offline?',
  'Walk me through the clock failover in S-2040',
  'Which systems need a software update?',
]

const SCOPE: Array<[string, string]> = [
  ['systems', `${systems.length} systems`],
  ['sessions', `${sessions.length} sessions`],
  ['knowledge', `${knowledge.length} knowledge docs`],
  ['docs', '4 doc sections'],
]
function scopeIcon(to: string): string {
  return to === 'systems' ? 'systems' : to === 'sessions' ? 'sessions' : to === 'knowledge' ? 'knowledge' : 'docs'
}

const lastQuestion = computed(() => {
  for (let i = conversation.value.length - 1; i >= 0; i--) {
    if (conversation.value[i].role === 'user') return conversation.value[i].text
  }
  return 'Ask Crew anything about your environment.'
})
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
            <div :style="{ fontFamily: L.mono, fontSize: '10px', color: L.text3 }">Operational assistant · grounded in your live environment</div>
          </div>
          <div :style="{ flex: 1 }" />
          <Pill :tone="sending ? 'accent' : 'ok'">{{ sending ? 'thinking…' : 'online' }}</Pill>
        </div>

        <!-- thread -->
        <div ref="threadEl" :style="threadScrollStyle">
          <div :style="{ maxWidth: '760px', margin: '0 auto', display: 'flex', flexDirection: 'column', gap: '22px' }">
            <!-- empty / welcome state -->
            <div v-if="conversation.length === 0" :style="{ display: 'flex', gap: '12px' }">
              <span :style="{ width: '28px', height: '28px', borderRadius: '8px', background: S.accentBg, border: `1px solid ${S.accentBorder}`, color: S.accentText, display: 'flex', alignItems: 'center', justifyContent: 'center', flex: '0 0 auto', marginTop: '2px' }"><Icon name="spark" :size="15" fill="cur" /></span>
              <p :style="{ margin: 0, fontFamily: L.body, fontSize: '14px', lineHeight: 1.6, color: L.text }">
                I’m Crew — I can see your systems, sessions and diagnostics. Ask me what needs attention, trace an incident, or tell me where to take you.
              </p>
            </div>

            <template v-for="(m, i) in conversation" :key="i">
              <div
                v-if="m.role === 'user'"
                :style="{ alignSelf: 'flex-end', maxWidth: '78%', background: S.accent, color: '#fff', borderRadius: '12px 12px 4px 12px', padding: '12px 15px 13px', fontFamily: L.body, fontSize: '14px', lineHeight: 1.55 }"
              >{{ m.text }}</div>
              <div v-else :style="{ display: 'flex', gap: '12px' }">
                <span :style="{ width: '28px', height: '28px', borderRadius: '8px', background: S.accentBg, border: `1px solid ${S.accentBorder}`, color: S.accentText, display: 'flex', alignItems: 'center', justifyContent: 'center', flex: '0 0 auto', marginTop: '2px' }"><Icon name="spark" :size="15" fill="cur" /></span>
                <div :style="{ minWidth: 0 }">
                  <p :style="{ margin: 0, fontFamily: L.body, fontSize: '14px', lineHeight: 1.6, color: m.error ? S.crit : L.text, whiteSpace: 'pre-wrap' }">{{ m.text
                    }}<span v-if="m.streaming" :style="{ display: 'inline-block', width: '7px', height: '14px', marginLeft: '2px', background: S.accent, borderRadius: '1px', verticalAlign: 'text-bottom', animation: 'dock-pulse 1s ease-in-out infinite' }" /></p>
                  <div v-if="m.navs.length" :style="{ display: 'flex', flexWrap: 'wrap', gap: '8px', marginTop: '12px' }">
                    <span
                      v-for="(nav, j) in m.navs"
                      :key="j"
                      :style="{ display: 'inline-flex', alignItems: 'center', gap: '6px', fontFamily: L.body, fontSize: '12px', fontWeight: 600, color: '#fff', background: S.accent, borderRadius: '7px', padding: '6px 11px', cursor: 'pointer' }"
                      @click="openNav(nav)"
                    >
                      <Icon name="arrowR" :size="12" />{{ navLabel(nav) }}
                    </span>
                  </div>
                </div>
              </div>
            </template>

            <!-- suggestions (only before the first message) -->
            <div v-if="conversation.length === 0" :style="{ marginTop: '4px' }">
              <SecLabel :style="{ marginBottom: '10px' }">Try asking</SecLabel>
              <div :style="{ display: 'flex', flexWrap: 'wrap', gap: '9px' }">
                <span
                  v-for="q in SUGGEST"
                  :key="q"
                  :style="{ fontFamily: L.body, fontSize: '12.5px', color: L.text2, background: L.panel, border: `1px solid ${L.border}`, borderRadius: '8px', padding: '8px 12px', cursor: 'pointer' }"
                  @click="send(q)"
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
              :disabled="sending"
              :style="{ flex: 1, minWidth: 0, border: 'none', outline: 'none', background: 'transparent', fontFamily: L.body, fontSize: '14px', color: L.text }"
              @keyup.enter="send(draft)"
            />
            <Btn primary sm icon="arrowR" @click="send(draft)">Ask</Btn>
          </div>
        </div>
      </div>

      <!-- agent mesh sidebar — ambient orchestration flavor. Hidden on compact. -->
      <div v-if="!isCompact" :style="meshStyle">
        <div :style="{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px' }">
          <SecLabel>Agent mesh</SecLabel>
          <span :style="{ display: 'inline-flex', alignItems: 'center', gap: '6px', fontFamily: L.mono, fontSize: '9px', fontWeight: 600, letterSpacing: '0.06em', color: S.accentText, background: S.accentBg, border: `1px solid ${S.accentBorder}`, borderRadius: '5px', padding: '2px 7px' }">
            <span :style="{ width: '6px', height: '6px', borderRadius: '3px', background: S.accent, animation: 'dock-pulse 1.1s ease-in-out infinite' }" />{{ sending ? 'PROCESSING' : 'READY' }}
          </span>
        </div>

        <div :style="{ background: L.panel, border: `1px solid ${L.border}`, borderRadius: '10px', padding: '11px 12px', marginBottom: '14px' }">
          <div :style="{ fontFamily: L.mono, fontSize: '8.5px', letterSpacing: '0.1em', color: L.text3, marginBottom: '5px' }">LAST QUERY</div>
          <div :style="{ fontFamily: L.body, fontSize: '12px', fontWeight: 600, color: L.text, lineHeight: 1.4 }">“{{ lastQuestion }}”</div>
        </div>

        <div :style="{ display: 'flex', flexDirection: 'column', gap: '7px', marginBottom: '14px' }">
          <div
            v-for="a in AGENTS"
            :key="a.name"
            :style="{ display: 'flex', alignItems: 'center', gap: '9px', padding: '9px 11px', borderRadius: '9px', border: `1px solid ${a.state === 'work' ? S.accentBorder : L.border}`, background: a.state === 'work' ? S.accentBg : L.panel, cursor: 'pointer', opacity: a.state === 'idle' ? 0.55 : 1 }"
            @click="go(a.to)"
          >
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
