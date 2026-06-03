/* manifest.ts — the documentation navigation tree, ported from the former
   Docusaurus sidebars.ts. Each `id` maps to src/docs/content/<id>.md and the
   in-app route /docs/<id>. Labels are concise nav titles (the page's own H1 is
   the on-page title). */

export interface DocLeaf {
  type: 'doc'
  id: string
  label: string
}
export interface DocCategory {
  type: 'category'
  label: string
  items: DocLeaf[]
}
export type DocNode = DocLeaf | DocCategory

export interface DocGuide {
  id: string
  label: string
  tree: DocNode[]
}

function doc(id: string, label: string): DocLeaf {
  return { type: 'doc', id, label }
}
function cat(label: string, items: DocLeaf[]): DocCategory {
  return { type: 'category', label, items }
}

export const DOC_GUIDES: DocGuide[] = [
  {
    id: 'user',
    label: 'User Guide',
    tree: [
      doc('user/overview', 'Overview'),
      cat('Getting Started', [
        doc('user/getting-started/installation', 'Installation'),
        doc('user/getting-started/first-run', 'First Run'),
        doc('user/getting-started/quickstart', 'Quickstart'),
      ]),
      cat('The Four Apps', [
        doc('user/apps/capstan', 'Capstan'),
        doc('user/apps/bridge', 'Bridge'),
        doc('user/apps/bus', 'Bus'),
        doc('user/apps/print', 'Print'),
      ]),
      cat('User Interface', [
        doc('user/interface/visual-language', 'Visual Language'),
        doc('user/interface/atmospheres', 'Atmospheres'),
        doc('user/interface/instruments', 'Instruments'),
      ]),
      cat('Workflows', [
        doc('user/workflows/recording', 'Recording'),
        doc('user/workflows/processing', 'Processing'),
        doc('user/workflows/mixing', 'Mixing'),
        doc('user/workflows/printing', 'Printing'),
      ]),
      cat('Configuration', [
        doc('user/configuration/portable-instance', 'Portable Instance'),
        doc('user/configuration/machine-binding', 'Machine Binding'),
        doc('user/configuration/network', 'Network'),
      ]),
      doc('user/troubleshooting', 'Troubleshooting'),
    ],
  },
  {
    id: 'developer',
    label: 'Developer Guide',
    tree: [
      doc('developer/overview', 'Overview'),
      cat('Architecture', [doc('developer/architecture', 'Architecture')]),
      cat('C++ Core', [
        doc('developer/cpp-core/overview', 'Overview'),
        doc('developer/cpp-core/shared-libraries', 'Shared Libraries'),
        doc('developer/cpp-core/app-structure', 'App Structure'),
        doc('developer/cpp-core/ipc-streaming', 'IPC & Streaming'),
        doc('developer/cpp-core/audio-engine', 'Audio Engine'),
      ]),
      cat('Frontend', [
        doc('developer/frontend/overview', 'Overview'),
        doc('developer/frontend/design-system', 'Design System'),
        doc('developer/frontend/instrument-runtime', 'Instrument Runtime'),
        doc('developer/frontend/composables', 'Composables'),
      ]),
      doc('developer/build-system', 'Build System'),
      doc('developer/protocol', 'Protocol'),
      doc('developer/openspec', 'OpenSpec'),
      doc('developer/migration', 'Migration'),
      doc('plan', 'Documentation Plan'),
    ],
  },
]

/** The first page shown at /docs. */
export const DEFAULT_DOC = 'user/overview'

/** Flattened [id → guide+breadcrumb] for lookups. */
export interface DocMeta {
  id: string
  label: string
  guideId: string
  guideLabel: string
  category: string | null
}

export const DOC_INDEX: Record<string, DocMeta> = {}
for (const guide of DOC_GUIDES) {
  for (const node of guide.tree) {
    if (node.type === 'doc') {
      DOC_INDEX[node.id] = { id: node.id, label: node.label, guideId: guide.id, guideLabel: guide.label, category: null }
    } else {
      for (const leaf of node.items) {
        DOC_INDEX[leaf.id] = { id: leaf.id, label: leaf.label, guideId: guide.id, guideLabel: guide.label, category: node.label }
      }
    }
  }
}

/** Flat ordered list of doc ids (for prev/next + search). */
export const DOC_ORDER: string[] = DOC_GUIDES.flatMap((g) =>
  g.tree.flatMap((n) => (n.type === 'doc' ? [n.id] : n.items.map((l) => l.id))),
)
