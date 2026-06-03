<script setup lang="ts">
import { computed, nextTick, ref, watch, type CSSProperties } from 'vue'
import { useRoute, useRouter, RouterLink } from 'vue-router'
import { L } from '@/design/tokens'
import { S } from '@/dock/status'
import { useBreakpoint } from '@/composables/useBreakpoint'
import Icon from '@/components/kit/Icon.vue'
import { DOC_GUIDES, DEFAULT_DOC, DOC_INDEX, DOC_ORDER, type DocGuide } from '@/docs/manifest'
import { getDocSource, docExists, docPlainText } from '@/docs/content'
import { renderDoc, extractTitle } from '@/docs/render'
import 'highlight.js/styles/github.css'

const route = useRoute()
const router = useRouter()
const { isMobile, isTablet } = useBreakpoint()

const slug = computed(() => {
  const s = route.params.slug
  return Array.isArray(s) ? s.join('/') : (s ?? '')
})
// Empty slug → default doc. Unknown slug → not-found state.
const currentId = computed(() => {
  if (!slug.value) return DEFAULT_DOC
  return docExists(slug.value) ? slug.value : ''
})
const notFound = computed(() => !currentId.value)

const html = computed(() => {
  const id = currentId.value
  if (!id) return ''
  return renderDoc(getDocSource(id) as string, id)
})
const meta = computed(() => (currentId.value ? DOC_INDEX[currentId.value] : null))

// Per-page document title. The router's afterEach skips the 'docs' route so
// this owns the title while a doc is open.
const pageTitle = computed(() => {
  if (notFound.value) return 'Page not found'
  const id = currentId.value
  return DOC_INDEX[id]?.label ?? extractTitle(getDocSource(id) as string)
})
watch(pageTitle, (t) => (document.title = `${t} — TapeForge Dock`), { immediate: true })

// prev / next within the flat order
const neighbours = computed(() => {
  const i = DOC_ORDER.indexOf(currentId.value)
  return {
    prev: i > 0 ? DOC_INDEX[DOC_ORDER[i - 1]] : null,
    next: i >= 0 && i < DOC_ORDER.length - 1 ? DOC_INDEX[DOC_ORDER[i + 1]] : null,
  }
})

// --- search ----------------------------------------------------------------
const q = ref('')
const filteredGuides = computed<DocGuide[]>(() => {
  const term = q.value.trim().toLowerCase()
  if (!term) return DOC_GUIDES
  const hit = (label: string, id: string) =>
    label.toLowerCase().includes(term) || id.toLowerCase().includes(term) || docPlainText(id).toLowerCase().includes(term)
  return DOC_GUIDES.map((g) => ({
    ...g,
    tree: g.tree
      .map((n) =>
        n.type === 'doc'
          ? hit(n.label, n.id)
            ? n
            : null
          : { ...n, items: n.items.filter((l) => hit(l.label, l.id)) },
      )
      .filter((n): n is NonNullable<typeof n> => n !== null && (n.type === 'doc' || n.items.length > 0)),
  })).filter((g) => g.tree.length > 0)
})

// --- mobile tree disclosure ------------------------------------------------
const treeOpen = ref(false)
function selected() {
  treeOpen.value = false
}

// --- in-content link interception + scroll ---------------------------------
const contentEl = ref<HTMLElement | null>(null)
function onContentClick(e: MouseEvent) {
  const a = (e.target as HTMLElement).closest('a[data-doc-link], a[href^="#"]') as HTMLAnchorElement | null
  if (!a) return
  const href = a.getAttribute('href')
  if (!href) return
  e.preventDefault()
  // Pure in-page anchors keep the current doc and only move the hash; that
  // re-triggers the scroll watch without a route component change.
  if (href.startsWith('#')) router.push({ path: route.path, hash: href })
  else router.push(href)
}

function scrollToHashOrTop() {
  nextTick(() => {
    const hash = route.hash
    if (hash) {
      const el = document.getElementById(decodeURIComponent(hash.slice(1)))
      if (el) {
        el.scrollIntoView({ block: 'start' })
        return
      }
    }
    if (contentEl.value) contentEl.value.scrollTop = 0
  })
}
watch(() => [currentId.value, route.hash], scrollToHashOrTop, { immediate: true })

// --- styles ----------------------------------------------------------------
const root = computed<CSSProperties>(() => ({
  flex: 1,
  minWidth: 0,
  display: 'flex',
  flexDirection: isMobile.value ? 'column' : 'row',
  minHeight: 0,
  height: '100%',
}))
const treeWrap = computed<CSSProperties>(() => ({
  width: isMobile.value ? '100%' : isTablet.value ? '210px' : '256px',
  flex: isMobile.value ? '0 0 auto' : `0 0 ${isTablet.value ? '210px' : '256px'}`,
  borderRight: isMobile.value ? 'none' : `1px solid ${L.border}`,
  borderBottom: isMobile.value && treeOpen.value ? `1px solid ${L.border}` : 'none',
  background: L.pageBg,
  display: 'flex',
  flexDirection: 'column',
  minHeight: 0,
  maxHeight: isMobile.value ? '45%' : 'none',
  overflowY: 'auto',
}))
const contentWrap = computed<CSSProperties>(() => ({
  flex: 1,
  minWidth: 0,
  minHeight: 0,
  overflowY: 'auto',
  background: L.panel,
}))
const article: CSSProperties = { maxWidth: '820px', margin: '0 auto', padding: '0 0 64px' }

const searchBox: CSSProperties = {
  display: 'flex',
  alignItems: 'center',
  gap: '8px',
  margin: '12px 12px 6px',
  padding: '8px 10px',
  borderRadius: '8px',
  border: `1px solid ${L.border}`,
  background: L.panel,
}
function docLinkStyle(on: boolean): CSSProperties {
  return {
    display: 'block',
    padding: '6px 12px 6px 22px',
    fontFamily: L.body,
    fontSize: '13px',
    color: on ? S.accentText : L.text2,
    fontWeight: on ? 600 : 400,
    textDecoration: 'none',
    borderLeft: `2px solid ${on ? S.accent : 'transparent'}`,
    background: on ? S.accentBg : 'transparent',
  }
}
const guideLabelStyle: CSSProperties = {
  fontFamily: L.mono,
  fontSize: '10px',
  letterSpacing: '0.12em',
  textTransform: 'uppercase',
  color: S.accentText,
  padding: '14px 12px 7px',
}
const catLabelStyle: CSSProperties = {
  fontFamily: L.body,
  fontSize: '12px',
  fontWeight: 700,
  color: L.text,
  padding: '10px 12px 4px',
}
</script>

<template>
  <div :style="root">
    <!-- nav tree -->
    <div :style="treeWrap">
      <!-- mobile disclosure header -->
      <div
        v-if="isMobile"
        :style="{ display: 'flex', alignItems: 'center', gap: '8px', padding: '12px 14px', cursor: 'pointer' }"
        @click="treeOpen = !treeOpen"
      >
        <Icon name="docs" :size="15" :style="{ color: S.accentText }" />
        <span :style="{ fontFamily: L.body, fontSize: '13px', fontWeight: 700, color: L.text, flex: 1 }">Contents</span>
        <Icon name="chevronD" :size="14" :style="{ color: L.text3, transform: treeOpen ? 'rotate(180deg)' : 'none' }" />
      </div>

      <template v-if="!isMobile || treeOpen">
        <div :style="searchBox">
          <Icon name="search" :size="14" :style="{ color: L.text3 }" />
          <input
            v-model="q"
            placeholder="Search docs…"
            :style="{ flex: 1, minWidth: 0, border: 'none', outline: 'none', background: 'transparent', fontFamily: L.body, fontSize: '13px', color: L.text }"
          />
        </div>

        <nav :style="{ paddingBottom: '16px' }">
          <template v-for="guide in filteredGuides" :key="guide.id">
            <div :style="guideLabelStyle">{{ guide.label }}</div>
            <template v-for="node in guide.tree" :key="node.type === 'doc' ? node.id : node.label">
              <RouterLink
                v-if="node.type === 'doc'"
                :to="`/docs/${node.id}`"
                :style="docLinkStyle(node.id === currentId)"
                @click="selected"
              >{{ node.label }}</RouterLink>
              <template v-else>
                <div :style="catLabelStyle">{{ node.label }}</div>
                <RouterLink
                  v-for="leaf in node.items"
                  :key="leaf.id"
                  :to="`/docs/${leaf.id}`"
                  :style="docLinkStyle(leaf.id === currentId)"
                  @click="selected"
                >{{ leaf.label }}</RouterLink>
              </template>
            </template>
          </template>
          <div v-if="filteredGuides.length === 0" :style="{ padding: '12px', fontFamily: L.mono, fontSize: '11px', color: L.text3 }">
            No matches.
          </div>
        </nav>
      </template>
    </div>

    <!-- content -->
    <div ref="contentEl" :style="contentWrap">
      <div :style="{ padding: isMobile ? '20px 16px 0' : '34px 40px 0' }">
        <div :style="article">
          <template v-if="notFound">
            <p class="tf-kicker">DOCUMENTATION</p>
            <h1 class="tf-h1">Page not found</h1>
            <p :style="{ fontFamily: L.body, fontSize: '15px', color: L.text2 }">
              No doc at “{{ slug }}”.
              <RouterLink :to="`/docs/${DEFAULT_DOC}`" :style="{ color: S.accentText }">Back to the User Guide →</RouterLink>
            </p>
          </template>

          <template v-else>
            <div v-if="meta" :style="{ display: 'flex', alignItems: 'center', gap: '7px', fontFamily: L.mono, fontSize: '10.5px', letterSpacing: '0.06em', color: L.text3, marginBottom: '10px' }">
              <span>{{ meta.guideLabel }}</span>
              <template v-if="meta.category"><Icon name="chevron" :size="11" /><span>{{ meta.category }}</span></template>
            </div>

            <!-- rendered markdown -->
            <div class="tf-prose" v-html="html" @click="onContentClick" />

            <!-- prev / next -->
            <div :style="{ display: 'flex', gap: '12px', marginTop: '40px', paddingTop: '20px', borderTop: `1px solid ${L.border}` }">
              <RouterLink
                v-if="neighbours.prev"
                :to="`/docs/${neighbours.prev.id}`"
                :style="{ flex: 1, padding: '12px 14px', border: `1px solid ${L.border}`, borderRadius: '10px', textDecoration: 'none', background: L.panel }"
              >
                <div :style="{ fontFamily: L.mono, fontSize: '9.5px', color: L.text3, letterSpacing: '0.08em' }">← PREVIOUS</div>
                <div :style="{ fontFamily: L.body, fontSize: '13.5px', fontWeight: 600, color: L.text, marginTop: '3px' }">{{ neighbours.prev.label }}</div>
              </RouterLink>
              <RouterLink
                v-if="neighbours.next"
                :to="`/docs/${neighbours.next.id}`"
                :style="{ flex: 1, padding: '12px 14px', border: `1px solid ${L.border}`, borderRadius: '10px', textDecoration: 'none', background: L.panel, textAlign: 'right' }"
              >
                <div :style="{ fontFamily: L.mono, fontSize: '9.5px', color: L.text3, letterSpacing: '0.08em' }">NEXT →</div>
                <div :style="{ fontFamily: L.body, fontSize: '13.5px', fontWeight: 600, color: L.text, marginTop: '3px' }">{{ neighbours.next.label }}</div>
              </RouterLink>
            </div>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Hex values mirror design/tokens.ts. Prose targets v-html content via :deep. */
.tf-kicker {
  margin: 0;
  font-family: 'JetBrains Mono', ui-monospace, monospace;
  font-size: 11px;
  letter-spacing: 0.16em;
  color: #2e6358;
}
.tf-h1 {
  margin: 10px 0 0;
  font-family: 'Satoshi', -apple-system, sans-serif;
  font-weight: 700;
  font-size: 30px;
  letter-spacing: -0.02em;
  color: #2f343c;
}
.tf-prose :deep(h1) {
  font-family: 'Satoshi', -apple-system, sans-serif;
  font-weight: 700;
  font-size: 30px;
  letter-spacing: -0.025em;
  color: #2f343c;
  margin: 0 0 6px;
  line-height: 1.15;
}
.tf-prose :deep(h2) {
  font-family: 'Satoshi', -apple-system, sans-serif;
  font-weight: 700;
  font-size: 21px;
  letter-spacing: -0.015em;
  color: #2f343c;
  margin: 36px 0 0;
  padding-top: 8px;
  border-top: 1px solid #eef0f3;
}
.tf-prose :deep(h3) {
  font-family: 'Satoshi', -apple-system, sans-serif;
  font-weight: 700;
  font-size: 16.5px;
  color: #2f343c;
  margin: 26px 0 0;
}
.tf-prose :deep(h4) {
  font-family: 'Satoshi', -apple-system, sans-serif;
  font-weight: 600;
  font-size: 14px;
  color: #2f343c;
  margin: 20px 0 0;
}
.tf-prose :deep(p),
.tf-prose :deep(li) {
  font-family: 'Satoshi', -apple-system, sans-serif;
  font-size: 15px;
  line-height: 1.7;
  color: #4a5565;
}
.tf-prose :deep(p) {
  margin: 13px 0 0;
}
.tf-prose :deep(ul),
.tf-prose :deep(ol) {
  margin: 12px 0 0;
  padding-left: 22px;
}
.tf-prose :deep(li) {
  margin: 5px 0 0;
}
.tf-prose :deep(a) {
  color: #3c7a6f;
  text-decoration: none;
  border-bottom: 1px solid #c4dad3;
}
.tf-prose :deep(a:hover) {
  border-bottom-color: #3c7a6f;
}
.tf-prose :deep(strong) {
  color: #2f343c;
  font-weight: 600;
}
.tf-prose :deep(code) {
  font-family: 'JetBrains Mono', ui-monospace, monospace;
  font-size: 12.5px;
  background: #f1f3f5;
  color: #2f343c;
  padding: 1.5px 5px;
  border-radius: 5px;
}
.tf-prose :deep(pre.hljs) {
  margin: 16px 0 0;
  padding: 14px 16px;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  overflow-x: auto;
  background: #fbfbfc;
}
.tf-prose :deep(pre.hljs code) {
  background: none;
  padding: 0;
  font-size: 12.5px;
  line-height: 1.6;
  color: #2f343c;
}
.tf-prose :deep(blockquote) {
  margin: 16px 0 0;
  padding: 4px 16px;
  border-left: 3px solid #c4dad3;
  background: #ecf4f1;
  border-radius: 0 8px 8px 0;
}
.tf-prose :deep(blockquote p) {
  margin: 8px 0;
  color: #2e6358;
}
.tf-prose :deep(table) {
  margin: 16px 0 0;
  border-collapse: collapse;
  width: 100%;
  font-family: 'Satoshi', -apple-system, sans-serif;
  font-size: 13.5px;
}
.tf-prose :deep(th),
.tf-prose :deep(td) {
  border: 1px solid #e5e7eb;
  padding: 8px 11px;
  text-align: left;
  color: #4a5565;
}
.tf-prose :deep(th) {
  background: #f9fafb;
  color: #2f343c;
  font-weight: 700;
}
.tf-prose :deep(hr) {
  border: none;
  border-top: 1px solid #e5e7eb;
  margin: 28px 0 0;
}
.tf-prose :deep(img) {
  max-width: 100%;
  border-radius: 8px;
}
</style>
