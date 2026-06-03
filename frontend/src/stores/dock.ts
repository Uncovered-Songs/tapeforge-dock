import { defineStore } from 'pinia'
import { ref } from 'vue'
import { fetchBootstrap } from '@/dock/api'
import type {
  ConfigChange,
  CrewRec,
  CrewTurn,
  Diagnostics,
  DockEvent,
  DockSession,
  DockSystem,
  DocGroup,
  KnowledgeItem,
} from '@/dock/data'

const emptyDiagnostics: Diagnostics = {
  clockOffset: [],
  jitter: [],
  latency: [],
  packetLoss: [],
  incidents: [],
}

/** Holds the operational dataset, loaded once from the backend's /bootstrap. */
export const useDockStore = defineStore('dock', () => {
  const systems = ref<DockSystem[]>([])
  const sessions = ref<DockSession[]>([])
  const eventStream = ref<DockEvent[]>([])
  const configChanges = ref<ConfigChange[]>([])
  const crewRecs = ref<CrewRec[]>([])
  const knowledge = ref<KnowledgeItem[]>([])
  const docTree = ref<DocGroup[]>([])
  const crewThread = ref<CrewTurn[]>([])
  const diagnostics = ref<Diagnostics>({ ...emptyDiagnostics })

  const loaded = ref(false)
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function load(): Promise<void> {
    if (loading.value) return
    loading.value = true
    error.value = null
    try {
      const b = await fetchBootstrap()
      systems.value = b.systems
      sessions.value = b.sessions
      eventStream.value = b.eventStream
      configChanges.value = b.configChanges
      crewRecs.value = b.crewRecs
      knowledge.value = b.knowledge
      docTree.value = b.docTree
      crewThread.value = b.crewThread
      diagnostics.value = b.diagnostics
      loaded.value = true
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to load Dock data.'
    } finally {
      loading.value = false
    }
  }

  return {
    systems,
    sessions,
    eventStream,
    configChanges,
    crewRecs,
    knowledge,
    docTree,
    crewThread,
    diagnostics,
    loaded,
    loading,
    error,
    load,
  }
})
