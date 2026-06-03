/* content.ts — loads the raw markdown for every doc at build time.
   src/docs/content/<id>.md  ⇒  id (e.g. "user/overview"). */

const raw = import.meta.glob('./content/**/*.md', {
  query: '?raw',
  import: 'default',
  eager: true,
}) as Record<string, string>

const byId: Record<string, string> = {}
for (const [path, source] of Object.entries(raw)) {
  const id = path.replace(/^\.\/content\//, '').replace(/\.md$/, '')
  byId[id] = source
}

export function getDocSource(id: string): string | undefined {
  return byId[id]
}

export function docExists(id: string): boolean {
  return Object.prototype.hasOwnProperty.call(byId, id)
}

export const ALL_DOC_IDS: string[] = Object.keys(byId).sort()

/** Plain-text body (markdown stripped of fences/syntax) for client-side search. */
export function docPlainText(id: string): string {
  const src = byId[id] ?? ''
  return src
    .replace(/```[\s\S]*?```/g, ' ')
    .replace(/[#>*_`|>-]/g, ' ')
    .replace(/\[([^\]]*)\]\([^)]*\)/g, '$1')
    .replace(/\s+/g, ' ')
    .trim()
}
