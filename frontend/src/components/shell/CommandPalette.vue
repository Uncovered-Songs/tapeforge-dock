<script setup lang="ts">
import { computed, nextTick, onMounted, onBeforeUnmount, ref, watch, type CSSProperties } from 'vue'
import { L } from '@/design/tokens'
import { S } from '@/dock/status'
import { paletteItems, type NavTarget } from '@/dock/crew'
import Icon from '@/components/kit/Icon.vue'

const props = defineProps<{
  open: boolean
  go: (section: string, sub?: string) => void
}>()
const emit = defineEmits<{ 'update:open': [boolean] }>()

const q = ref('')
const inputRef = ref<HTMLInputElement | null>(null)
const ITEMS = paletteItems()

function onKey(e: KeyboardEvent) {
  if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
    e.preventDefault()
    emit('update:open', !props.open)
  }
  if (e.key === 'Escape') emit('update:open', false)
}
onMounted(() => window.addEventListener('keydown', onKey))
onBeforeUnmount(() => window.removeEventListener('keydown', onKey))

watch(
  () => props.open,
  (open) => {
    if (open) nextTick(() => inputRef.value?.focus())
    else q.value = ''
  },
)

const ql = computed(() => q.value.trim().toLowerCase())
const matches = computed(() =>
  ql.value
    ? ITEMS.filter((n) => n.label.toLowerCase().includes(ql.value) || (n.hint ?? '').toLowerCase().includes(ql.value))
    : ITEMS.slice(0, 7),
)
const looksLikeQuestion = computed(
  () => ql.value.length > 0 && (ql.value.split(' ').length > 2 || /\?|why|how|what|when|which|explain|show|take/.test(ql.value)),
)

function run(to: NavTarget) {
  emit('update:open', false)
  props.go(...to)
}
function askCrew() {
  emit('update:open', false)
  props.go('crew')
}

const overlay: CSSProperties = {
  position: 'fixed',
  inset: '0',
  zIndex: 80,
  background: 'rgba(20,24,28,0.32)',
  backdropFilter: 'blur(2px)',
  display: 'flex',
  alignItems: 'flex-start',
  justifyContent: 'center',
  paddingTop: '12vh',
}
const dialog: CSSProperties = {
  width: '600px',
  maxWidth: '92vw',
  background: L.panel,
  borderRadius: '14px',
  border: `1px solid ${L.border2}`,
  boxShadow: '0 24px 70px rgba(16,24,40,0.30)',
  overflow: 'hidden',
}
</script>

<template>
  <div v-if="open" :style="overlay" @click="emit('update:open', false)">
    <div :style="dialog" @click.stop>
      <div :style="{ display: 'flex', alignItems: 'center', gap: '11px', padding: '15px 18px', borderBottom: `1px solid ${L.border}` }">
        <Icon :name="looksLikeQuestion ? 'spark' : 'search'" :size="17" :fill="looksLikeQuestion ? 'cur' : 'none'" :style="{ color: looksLikeQuestion ? S.accent : L.text3 }" />
        <input
          ref="inputRef"
          v-model="q"
          placeholder="Jump to a system or session — or ask Crew to take you somewhere…"
          :style="{ flex: 1, border: 'none', outline: 'none', background: 'transparent', fontFamily: L.body, fontSize: '15px', color: L.text }"
        />
        <span :style="{ fontFamily: L.mono, fontSize: '9.5px', color: L.text3, border: `1px solid ${L.border}`, borderRadius: '4px', padding: '2px 6px' }">ESC</span>
      </div>

      <div
        v-if="looksLikeQuestion"
        :style="{ display: 'flex', alignItems: 'center', gap: '11px', padding: '13px 18px', borderBottom: `1px solid ${L.border}`, background: S.accentBg, cursor: 'pointer' }"
        @click="askCrew"
      >
        <span :style="{ width: '28px', height: '28px', borderRadius: '8px', background: S.accent, color: '#fff', display: 'flex', alignItems: 'center', justifyContent: 'center' }"><Icon name="spark" :size="15" fill="cur" /></span>
        <div :style="{ flex: 1 }">
          <div :style="{ fontFamily: L.body, fontSize: '13.5px', fontWeight: 600, color: L.text }">Ask Crew: “{{ q }}”</div>
          <div :style="{ fontFamily: L.mono, fontSize: '9.5px', color: S.accentText }">Crew will answer and navigate the app for you</div>
        </div>
        <Icon name="arrowR" :size="15" :style="{ color: S.accentText }" />
      </div>

      <div :style="{ maxHeight: '320px', overflowY: 'auto', padding: '8px 8px 10px' }">
        <div :style="{ fontFamily: L.mono, fontSize: '9px', letterSpacing: '0.12em', color: L.text3, padding: '8px 12px 6px' }">{{ ql ? 'JUMP TO' : 'QUICK NAV' }}</div>
        <div
          v-for="(m, i) in matches"
          :key="i"
          :style="{ display: 'flex', alignItems: 'center', gap: '11px', padding: '9px 12px', borderRadius: '8px', cursor: 'pointer' }"
          @click="run(m.to)"
          @mouseenter="(e) => ((e.currentTarget as HTMLElement).style.background = L.pageBg)"
          @mouseleave="(e) => ((e.currentTarget as HTMLElement).style.background = 'transparent')"
        >
          <Icon :name="m.icon" :size="15" :style="{ color: L.text3 }" />
          <span :style="{ fontFamily: L.body, fontSize: '13.5px', color: L.text, flex: 1 }">{{ m.label }}</span>
          <span v-if="m.hint" :style="{ fontFamily: L.mono, fontSize: '10px', color: L.text3 }">{{ m.hint }}</span>
          <Icon name="arrowR" :size="13" :style="{ color: L.text3 }" />
        </div>
      </div>

      <div :style="{ display: 'flex', alignItems: 'center', gap: '16px', padding: '9px 16px', borderTop: `1px solid ${L.border}`, background: '#FCFCFD', fontFamily: L.mono, fontSize: '9.5px', color: L.text3 }">
        <span>↓↑ navigate</span><span>↵ open</span><span :style="{ flex: 1 }" /><span :style="{ display: 'flex', alignItems: 'center', gap: '5px' }"><Icon name="spark" :size="11" />Crew routes &amp; navigates for you</span>
      </div>
    </div>
  </div>
</template>
