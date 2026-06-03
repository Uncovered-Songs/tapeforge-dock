<script setup lang="ts">
import { computed, ref, type CSSProperties } from 'vue'
import { L } from '@/design/tokens'
import { S } from '@/dock/status'
import { SCENARIOS, sectionLabel, suggestionsFor, seededReply, type DockRoute, type Scenario } from '@/dock/crew'
import Icon from '@/components/kit/Icon.vue'
import SecLabel from '@/components/kit/SecLabel.vue'
import Btn from '@/components/kit/Btn.vue'

const props = defineProps<{
  route: DockRoute
  go: (section: string, sub?: string) => void
  lastNav: string | null
}>()
const emit = defineEmits<{ close: [] }>()

const ctx = computed(() => sectionLabel(props.route))
const sug = computed(() => suggestionsFor(props.route))
const reply = computed(() => seededReply(props.route))

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

const root: CSSProperties = {
  width: '520px',
  flex: '0 0 520px',
  height: '100%',
  display: 'flex',
  flexDirection: 'column',
  minHeight: 0,
  background: L.panel,
  borderRight: `1px solid ${L.border}`,
}
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
        <span :style="{ width: '6px', height: '6px', borderRadius: '3px', background: S.accent, animation: 'dock-pulse 1.1s ease-in-out infinite' }" />6 AGENTS
      </span>
      <span :style="{ fontFamily: L.mono, fontSize: '9.5px', color: L.text3 }">· Networking ✓ · Topology ✓ · Troubleshooting working…</span>
    </div>

    <!-- thread -->
    <div :style="{ flex: 1, minHeight: 0, overflowY: 'auto', padding: '16px', display: 'flex', flexDirection: 'column', gap: '13px' }">
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

      <template v-else>
        <div :style="{ alignSelf: 'flex-end', maxWidth: '85%', background: S.accent, color: '#fff', borderRadius: '12px 12px 4px 12px', padding: '10px 13px 11px', fontFamily: L.body, fontSize: '13px', lineHeight: 1.5 }">{{ sug[0].t }}</div>
        <div :style="{ display: 'flex', gap: '10px' }">
          <span :style="sparkBadge"><Icon name="spark" :size="14" fill="cur" /></span>
          <div :style="{ minWidth: 0 }">
            <p :style="{ margin: 0, fontFamily: L.body, fontSize: '13px', lineHeight: 1.55, color: L.text }">{{ reply }}</p>
            <div :style="{ display: 'flex', flexWrap: 'wrap', gap: '7px', marginTop: '10px' }">
              <span :style="{ display: 'inline-flex', alignItems: 'center', gap: '6px', fontFamily: L.body, fontSize: '12px', fontWeight: 600, color: '#fff', background: S.accent, borderRadius: '7px', padding: '6px 11px', cursor: 'pointer' }" @click="go(...sug[0].to)"><Icon name="arrowR" :size="12" />Take me there</span>
              <span :style="{ display: 'inline-flex', alignItems: 'center', gap: '6px', fontFamily: L.mono, fontSize: '10px', color: S.accentText, background: L.panel, border: `1px solid ${L.border2}`, borderRadius: '7px', padding: '6px 9px', cursor: 'pointer' }" @click="go('crew')"><Icon name="link" :size="11" />sources</span>
            </div>
          </div>
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
        <div :style="{ display: 'flex', alignItems: 'center', gap: '8px', padding: '10px 12px', borderRadius: '9px', border: `1px solid ${L.border2}`, background: L.panel }">
          <Icon name="spark" :size="15" :style="{ color: L.text3 }" />
          <span :style="{ flex: 1, fontFamily: L.body, fontSize: '13px', color: L.text3 }">Ask Crew or tell it where to go…</span>
          <span :style="{ fontFamily: L.mono, fontSize: '9px', color: L.text3, border: `1px solid ${L.border}`, borderRadius: '4px', padding: '2px 5px' }">⌘K</span>
        </div>
      </template>
    </div>
  </div>
</template>
