<script setup lang="ts">
import { computed, nextTick, ref, type CSSProperties } from 'vue'
import { L } from '@/design/tokens'
import { S } from '@/dock/status'
import { useBreakpoint } from '@/composables/useBreakpoint'
import { SCENARIOS, sectionLabel, suggestionsFor, type DockRoute, type Scenario } from '@/dock/crew'
import { streamCrewChat, type CrewMessage } from '@/dock/api'
import Icon from '@/components/kit/Icon.vue'
import SecLabel from '@/components/kit/SecLabel.vue'
import Btn from '@/components/kit/Btn.vue'

const { isMobile } = useBreakpoint()

const props = defineProps<{
  route: DockRoute
  go: (section: string, sub?: string) => void
  lastNav: string | null
}>()
const emit = defineEmits<{ close: [] }>()

const ctx = computed(() => sectionLabel(props.route))
const sug = computed(() => suggestionsFor(props.route))

// --- guided walkthroughs (scripted demos) ----------------------------------
const scen = ref<string | null>(null)
const step = ref(0)
const active = computed<Scenario | null>(() => SCENARIOS.find((s) => s.id === scen.value) ?? null)
const playedSteps = computed(() => (active.value ? active.value.steps.slice(0, step.value + 1) : []))

function startScenario(s: Scenario) {
  scen.value = s.id
  step.value = 0
  props.go(...s.steps[0].to)
}
function advance() {
  const a = active.value
  if (!a) return
  const next = step.value + 1
  if (next < a.steps.length) {
    step.value = next
    props.go(...a.steps[next].to)
  } else {
    scen.value = null
    step.value = 0
  }
}
function endScenario() {
  scen.value = null
  step.value = 0
}

// --- live conversation (real AI) -------------------------------------------
interface ChatTurn {
  role: 'user' | 'crew'
  text: string
  streaming?: boolean
  error?: boolean
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

async function send(text: string): Promise<void> {
  const q = text.trim()
  if (!q || sending.value) return
  conversation.value.push({ role: 'user', text: q })
  conversation.value.push({ role: 'crew', text: '', streaming: true })
  const idx = conversation.value.length - 1
  draft.value = ''
  sending.value = true
  scrollSoon()

  const history: CrewMessage[] = conversation.value.slice(0, idx).map((m) => ({
    role: m.role === 'user' ? 'user' : 'assistant',
    content: m.text,
  }))

  // In the rail, Crew governs the app: navigate tool calls actually move it.
  await streamCrewChat(history, props.route, {
    onText: (t) => {
      conversation.value[idx].text += t
      scrollSoon()
    },
    onNavigate: (section, sub) => {
      props.go(section, sub ?? undefined)
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

// Fills the width on phones (it lives in a full-screen overlay there);
// fixed 520px beside the rail / in the tablet overlay otherwise.
const root = computed<CSSProperties>(() => ({
  width: isMobile.value ? '100%' : '520px',
  flex: isMobile.value ? '1 1 auto' : '0 0 520px',
  maxWidth: '100%',
  height: '100%',
  display: 'flex',
  flexDirection: 'column',
  minHeight: 0,
  background: L.panel,
  borderRight: `1px solid ${L.border}`,
}))
const sparkBadge: CSSProperties = {
  width: '26px',
  height: '26px',
  borderRadius: '7px',
  background: S.accentBg,
  border: `1px solid ${S.accentBorder}`,
  color: S.accentText,
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  flex: '0 0 auto',
  marginTop: '1px',
}
const crewText: CSSProperties = {
  margin: 0,
  fontFamily: L.body,
  fontSize: '13px',
  lineHeight: 1.55,
  color: L.text,
  whiteSpace: 'pre-wrap',
}
const userBubble: CSSProperties = {
  alignSelf: 'flex-end',
  maxWidth: '85%',
  background: S.accent,
  color: '#fff',
  borderRadius: '12px 12px 4px 12px',
  padding: '10px 13px 11px',
  fontFamily: L.body,
  fontSize: '13px',
  lineHeight: 1.5,
}
const suggestChip: CSSProperties = {
  fontFamily: L.body,
  fontSize: '12.5px',
  color: L.text2,
  background: L.pageBg,
  border: `1px solid ${L.border}`,
  borderRadius: '8px',
  padding: '8px 11px',
  cursor: 'pointer',
}
</script>

<template>
  <div :style="root">
    <!-- header -->
    <div :style="{ display: 'flex', alignItems: 'center', gap: '11px', padding: '15px 16px', borderBottom: `1px solid ${L.border}` }">
      <span :style="{ width: '30px', height: '30px', borderRadius: '8px', background: S.accent, color: '#fff', display: 'flex', alignItems: 'center', justifyContent: 'center', flex: '0 0 auto' }"><Icon name="spark" :size="16" fill="cur" /></span>
      <div :style="{ flex: 1, minWidth: 0 }">
        <div :style="{ fontFamily: L.body, fontSize: '14.5px', fontWeight: 700, color: L.text }">Crew</div>
        <div :style="{ fontFamily: L.mono, fontSize: '9.5px', color: L.text3 }">operational manager · governs the app</div>
      </div>
      <span title="Full workspace" :style="{ cursor: 'pointer', color: L.text3, display: 'flex' }" @click="go('crew')"><Icon name="ext" :size="15" /></span>
      <span title="Collapse" :style="{ cursor: 'pointer', color: L.text3, display: 'flex' }" @click="emit('close')"><Icon name="chevron" :size="16" :style="{ transform: 'rotate(180deg)' }" /></span>
    </div>

    <!-- context strip -->
    <div :style="{ padding: '10px 16px', background: S.accentBg, borderBottom: `1px solid ${L.border}` }">
      <div :style="{ display: 'flex', alignItems: 'center', gap: '8px' }">
        <Icon name="pin" :size="12" fill="cur" :style="{ color: S.accentText }" />
        <span :style="{ fontFamily: L.mono, fontSize: '10px', color: S.accentText }">You are on <b>{{ ctx }}</b></span>
      </div>
      <div v-if="lastNav" :style="{ display: 'flex', alignItems: 'flex-start', gap: '8px', marginTop: '7px', paddingTop: '7px', borderTop: `1px solid ${S.accentBorder}` }">
        <Icon name="arrowR" :size="12" :style="{ color: S.accentText, marginTop: '2px' }" />
        <span :style="{ fontFamily: L.body, fontSize: '11.5px', lineHeight: 1.4, color: L.text }">{{ lastNav }}</span>
      </div>
    </div>

    <!-- working mesh strip -->
    <div :style="{ display: 'flex', alignItems: 'center', gap: '8px', padding: '10px 16px', borderBottom: `1px solid ${L.border}` }">
      <span :style="{ display: 'inline-flex', alignItems: 'center', gap: '6px', fontFamily: L.mono, fontSize: '9px', fontWeight: 600, letterSpacing: '0.06em', color: S.accentText }">
        <span :style="{ width: '6px', height: '6px', borderRadius: '3px', background: S.accent, animation: 'dock-pulse 1.1s ease-in-out infinite' }" />{{ sending ? 'WORKING' : 'READY' }}
      </span>
      <span :style="{ fontFamily: L.mono, fontSize: '9.5px', color: L.text3 }">· grounded in your live environment</span>
    </div>

    <!-- thread -->
    <div ref="threadEl" :style="{ flex: 1, minHeight: 0, overflowY: 'auto', padding: '16px', display: 'flex', flexDirection: 'column', gap: '13px' }">
      <!-- guided walkthrough (scripted) -->
      <template v-if="active">
        <div :style="{ display: 'flex', alignItems: 'center', gap: '9px', padding: '8px 11px', borderRadius: '9px', background: S.accentBg, border: `1px solid ${S.accentBorder}` }">
          <Icon :name="active.icon" :size="14" :style="{ color: S.accentText }" />
          <span :style="{ fontFamily: L.body, fontSize: '12.5px', fontWeight: 700, color: L.text, flex: 1 }">{{ active.title }}</span>
          <span :style="{ fontFamily: L.mono, fontSize: '9.5px', color: S.accentText }">{{ step + 1 }}/{{ active.steps.length }}</span>
          <span title="End walkthrough" :style="{ cursor: 'pointer', color: L.text3, fontFamily: L.mono, fontSize: '15px', lineHeight: 1 }" @click="endScenario">×</span>
        </div>
        <div v-for="(st, i) in playedSteps" :key="i" :style="{ display: 'flex', gap: '10px', opacity: i === step ? 1 : 0.55 }">
          <span :style="sparkBadge"><Icon name="spark" :size="14" fill="cur" /></span>
          <div :style="{ minWidth: 0 }">
            <p :style="{ margin: 0, fontFamily: L.body, fontSize: '13px', lineHeight: 1.55, color: L.text }">{{ st.say }}</p>
            <div v-if="i === step" :style="{ display: 'inline-flex', alignItems: 'center', gap: '5px', marginTop: '6px', fontFamily: L.mono, fontSize: '9px', color: L.text3 }"><Icon name="arrowR" :size="10" />navigated the app</div>
          </div>
        </div>
      </template>

      <!-- live conversation (real AI) -->
      <template v-else-if="conversation.length">
        <template v-for="(mm, i) in conversation" :key="i">
          <div v-if="mm.role === 'user'" :style="userBubble">{{ mm.text }}</div>
          <div v-else :style="{ display: 'flex', gap: '10px' }">
            <span :style="sparkBadge"><Icon name="spark" :size="14" fill="cur" /></span>
            <p :style="{ ...crewText, color: mm.error ? S.crit : L.text }">{{ mm.text
              }}<span v-if="mm.streaming" :style="{ display: 'inline-block', width: '6px', height: '13px', marginLeft: '2px', background: S.accent, borderRadius: '1px', verticalAlign: 'text-bottom', animation: 'dock-pulse 1s ease-in-out infinite' }" /></p>
          </div>
        </template>
      </template>

      <!-- idle: greeting + suggestions -->
      <template v-else>
        <div :style="{ display: 'flex', gap: '10px' }">
          <span :style="sparkBadge"><Icon name="spark" :size="14" fill="cur" /></span>
          <p :style="crewText">I can see your systems, sessions and diagnostics. Ask me anything — or pick a starting point and I’ll take you there.</p>
        </div>
        <div :style="{ display: 'flex', flexDirection: 'column', gap: '7px' }">
          <span v-for="s in sug" :key="s.t" :style="suggestChip" @click="send(s.t)">{{ s.t }}</span>
        </div>
      </template>
    </div>

    <!-- footer -->
    <div :style="{ padding: '12px 16px', borderTop: `1px solid ${L.border}` }">
      <div v-if="active" :style="{ display: 'flex', alignItems: 'center', gap: '9px' }">
        <Btn sm @click="endScenario">End</Btn>
        <span :style="{ flex: 1 }" />
        <Btn v-if="step + 1 < active.steps.length" sm primary icon="arrowR" @click="advance">Next step</Btn>
        <Btn v-else sm primary icon="check" @click="endScenario">Done</Btn>
      </div>
      <template v-else>
        <!-- walkthroughs only before any chat -->
        <template v-if="conversation.length === 0">
          <SecLabel :style="{ marginBottom: '9px' }">Guided walkthroughs</SecLabel>
          <div :style="{ display: 'flex', flexDirection: 'column', gap: '7px', marginBottom: '12px' }">
            <div
              v-for="s in SCENARIOS"
              :key="s.id"
              :style="{ display: 'flex', alignItems: 'center', gap: '10px', padding: '9px 11px', borderRadius: '9px', border: `1px solid ${L.border}`, background: L.pageBg, cursor: 'pointer' }"
              @click="startScenario(s)"
            >
              <span :style="{ width: '24px', height: '24px', borderRadius: '7px', background: L.panel, border: `1px solid ${L.border}`, display: 'flex', alignItems: 'center', justifyContent: 'center', flex: '0 0 auto', color: S.accentText }"><Icon :name="s.icon" :size="13" /></span>
              <div :style="{ flex: 1, minWidth: 0 }">
                <div :style="{ fontFamily: L.body, fontSize: '12.5px', fontWeight: 600, color: L.text }">{{ s.title }}</div>
                <div :style="{ fontFamily: L.mono, fontSize: '9px', color: L.text3, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }">{{ s.blurb }}</div>
              </div>
              <span :style="{ display: 'inline-flex', alignItems: 'center', gap: '4px', fontFamily: L.mono, fontSize: '9px', color: S.accentText }"><Icon name="arrowR" :size="11" />{{ s.steps.length }}</span>
            </div>
          </div>
        </template>

        <!-- functional composer -->
        <div :style="{ display: 'flex', alignItems: 'center', gap: '8px', padding: '10px 12px', borderRadius: '9px', border: `1px solid ${L.border2}`, background: L.panel }">
          <Icon name="spark" :size="15" :style="{ color: L.text3 }" />
          <input
            v-model="draft"
            type="text"
            placeholder="Ask Crew or tell it where to go…"
            :disabled="sending"
            :style="{ flex: 1, minWidth: 0, border: 'none', outline: 'none', background: 'transparent', fontFamily: L.body, fontSize: '13px', color: L.text }"
            @keyup.enter="send(draft)"
          />
          <span
            :style="{ cursor: sending ? 'default' : 'pointer', color: draft.trim() && !sending ? S.accent : L.text3, display: 'flex' }"
            @click="send(draft)"
          ><Icon name="arrowR" :size="16" /></span>
        </div>
      </template>
    </div>
  </div>
</template>
