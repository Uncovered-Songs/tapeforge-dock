/* render.ts — markdown → HTML for the in-app docs. markdown-it with GitHub-style
   heading slugs (so #fragment links resolve), syntax highlighting, and internal
   .md link rewriting to /docs/<id> routes (resolved relative to the current doc). */
import MarkdownIt from 'markdown-it'
import anchor from 'markdown-it-anchor'
import hljs from 'highlight.js/lib/common'
import powershell from 'highlight.js/lib/languages/powershell'
import cmake from 'highlight.js/lib/languages/cmake'

hljs.registerLanguage('powershell', powershell)
hljs.registerLanguage('cmake', cmake)

function escapeHtml(s: string): string {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;')
}

/** GitHub-slugger-compatible: lowercase, strip punctuation (keep word chars,
    spaces, hyphens), spaces → single hyphens (no collapsing). */
export function slugify(input: string): string {
  return input
    .trim()
    .toLowerCase()
    .replace(/[^\w\s-]/g, '')
    .replace(/\s/g, '-')
}

const md: MarkdownIt = new MarkdownIt({
  html: true,
  linkify: true,
  typographer: false,
  highlight(str, lang) {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return `<pre class="hljs"><code>${hljs.highlight(str, { language: lang, ignoreIllegals: true }).value}</code></pre>`
      } catch {
        /* fall through */
      }
    }
    return `<pre class="hljs"><code>${escapeHtml(str)}</code></pre>`
  },
})

md.use(anchor, { slugify, level: [1, 2, 3, 4] })

interface ResolvedLink {
  href: string
  external?: boolean
  internal?: boolean
  anchor?: boolean
}

/** Resolve a markdown link against the current doc id. */
export function resolveDocLink(href: string, currentId: string): ResolvedLink {
  if (/^(https?:)?\/\//i.test(href) || href.startsWith('mailto:')) {
    return { href, external: true }
  }
  if (href.startsWith('#')) return { href, anchor: true }

  const hashAt = href.indexOf('#')
  const pathPart = hashAt >= 0 ? href.slice(0, hashAt) : href
  const frag = hashAt >= 0 ? href.slice(hashAt) : ''
  if (!pathPart) return { href, anchor: true }

  const cleaned = pathPart.replace(/\.md$/, '')
  let segs: string[]
  if (cleaned.startsWith('/')) {
    segs = cleaned.replace(/^\/(docs\/)?/, '').split('/')
  } else {
    segs = currentId.split('/').slice(0, -1)
    for (const part of cleaned.split('/')) {
      if (part === '.' || part === '') continue
      else if (part === '..') segs.pop()
      else segs.push(part)
    }
  }
  return { href: `/docs/${segs.filter(Boolean).join('/')}${frag}`, internal: true }
}

const defaultLinkOpen =
  md.renderer.rules.link_open ?? ((tokens, idx, options, _env, self) => self.renderToken(tokens, idx, options))

md.renderer.rules.link_open = (tokens, idx, options, env, self) => {
  const token = tokens[idx]
  const hrefIdx = token.attrIndex('href')
  if (hrefIdx >= 0 && token.attrs) {
    const r = resolveDocLink(token.attrs[hrefIdx][1], (env as { currentId?: string }).currentId ?? '')
    token.attrs[hrefIdx][1] = r.href
    if (r.external) {
      token.attrSet('target', '_blank')
      token.attrSet('rel', 'noopener noreferrer')
    }
    if (r.internal) token.attrSet('data-doc-link', '')
  }
  return defaultLinkOpen(tokens, idx, options, env, self)
}

/** Render one doc's markdown to HTML. `currentId` resolves relative links. */
export function renderDoc(source: string, currentId: string): string {
  return md.render(source, { currentId })
}

/** First H1 of the source, used as the page title. */
export function extractTitle(source: string): string {
  const m = source.match(/^#\s+(.+?)\s*$/m)
  return m ? m[1].replace(/[`*_]/g, '') : 'Documentation'
}
