import { beforeAll, describe, expect, it } from 'vitest'
import { ALL_DOC_IDS, getDocSource, docExists } from '../content'
import { renderDoc } from '../render'
import { DOC_INDEX, DOC_ORDER, DEFAULT_DOC } from '../manifest'

interface Rendered {
  html: string
  ids: Set<string>
  links: string[] // hrefs of internal data-doc-link anchors
  allHrefs: string[] // hrefs of every anchor (to catch bogus linkification)
}

const rendered: Record<string, Rendered> = {}

beforeAll(() => {
  for (const id of ALL_DOC_IDS) {
    const html = renderDoc(getDocSource(id) as string, id)
    const doc = new DOMParser().parseFromString(html, 'text/html')
    rendered[id] = {
      html,
      ids: new Set([...doc.querySelectorAll('[id]')].map((e) => e.id)),
      links: [...doc.querySelectorAll('a[data-doc-link]')].map((a) => a.getAttribute('href') ?? ''),
      allHrefs: [...doc.querySelectorAll('a[href]')].map((a) => a.getAttribute('href') ?? ''),
    }
  }
})

// Failures are collected into arrays so a single assertion names every
// offender — the lint config caps expect() at one argument, so we can't pass a
// per-iteration message.
describe('docs migration integrity', () => {
  it('renders every doc to non-trivial HTML with an H1 anchor', () => {
    expect(ALL_DOC_IDS.length).toBe(35)
    const trivial = ALL_DOC_IDS.filter((id) => rendered[id].html.length <= 40)
    expect(trivial).toEqual([])
    const noH1 = ALL_DOC_IDS.filter((id) => !/<h1[^>]*\bid=/.test(rendered[id].html))
    expect(noH1).toEqual([])
  })

  it('every internal .md link resolves to an existing doc', () => {
    const broken: string[] = []
    for (const id of ALL_DOC_IDS) {
      for (const href of rendered[id].links) {
        const targetId = href.replace(/^\/docs\//, '').split('#')[0]
        if (!docExists(targetId)) broken.push(`${id} → ${href}`)
      }
    }
    expect(broken).toEqual([])
  })

  it('every #fragment in an internal link resolves to a heading anchor', () => {
    const broken: string[] = []
    for (const id of ALL_DOC_IDS) {
      for (const href of rendered[id].links) {
        const [path, frag] = href.replace(/^\/docs\//, '').split('#')
        if (!frag) continue
        const target = rendered[path]
        if (target && !target.ids.has(decodeURIComponent(frag))) broken.push(`${id} → ${href}`)
      }
    }
    expect(broken).toEqual([])
  })

  it('no bare *.md filename was linkified into a bogus external link', () => {
    // markdown-it's linkify turns prose like `architecture.md` into an
    // <a href="http://architecture.md">. Bare doc filenames must be backticked.
    const bogus: string[] = []
    for (const id of ALL_DOC_IDS) {
      for (const href of rendered[id].allHrefs) {
        if (/^https?:\/\/[^/]+\.md(\/|#|$)/i.test(href)) bogus.push(`${id} → ${href}`)
      }
    }
    expect(bogus).toEqual([])
  })

  it('no Docusaurus-only syntax slipped through unrendered', () => {
    const offenders: string[] = []
    for (const id of ALL_DOC_IDS) {
      const src = getDocSource(id) as string
      if (/^:::/m.test(src)) offenders.push(`${id}: admonition`)
      if (/^import\s+\w+\s+from/m.test(src)) offenders.push(`${id}: MDX import`)
      if (/<Tabs|<TabItem|<details>/.test(src)) offenders.push(`${id}: MDX component`)
    }
    expect(offenders).toEqual([])
  })

  it('manifest and content are consistent', () => {
    // every manifest doc has a source file
    const missing = DOC_ORDER.filter((id) => !docExists(id))
    expect(missing).toEqual([])
    expect(docExists(DEFAULT_DOC)).toBe(true)
    // every content file is reachable from the nav (no orphans)
    const orphans = ALL_DOC_IDS.filter((id) => !DOC_INDEX[id])
    expect(orphans).toEqual([])
  })
})
