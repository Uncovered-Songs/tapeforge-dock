// Thin client for the TapeForge Dock backend API. Base URL is configurable via
// VITE_DOCK_API_BASE_URL; defaults to the local FastAPI dev server (:8001).
import type { DockBootstrap } from './data'

const API_BASE_URL = (
  import.meta.env.VITE_DOCK_API_BASE_URL ?? 'http://localhost:8001/api/v1'
).replace(/\/$/, '')

/** Raised when the API responds with a non-2xx status or is unreachable. */
export class ApiError extends Error {
  constructor(
    message: string,
    readonly status: number,
  ) {
    super(message)
    this.name = 'ApiError'
  }
}

/** Load the entire Dock dataset in one call. */
export async function fetchBootstrap(): Promise<DockBootstrap> {
  let res: Response
  try {
    res = await fetch(`${API_BASE_URL}/bootstrap`)
  } catch {
    throw new ApiError('Could not reach the Dock API. Is the backend running?', 0)
  }
  if (!res.ok) {
    throw new ApiError(`Failed to load Dock data (HTTP ${res.status}).`, res.status)
  }
  return (await res.json()) as DockBootstrap
}

// --- Crew (streaming AI assistant) -----------------------------------------

export interface CrewMessage {
  role: 'user' | 'assistant'
  content: string
}

export interface CrewHandlers {
  onText: (text: string) => void
  onNavigate: (section: string, sub: string | null) => void
  onError: (message: string) => void
  onDone: () => void
}

/** Stream a Crew reply over Server-Sent Events. */
export async function streamCrewChat(
  messages: CrewMessage[],
  route: { section: string | null; sub: string | null } | null,
  handlers: CrewHandlers,
  signal?: AbortSignal,
): Promise<void> {
  let res: Response
  try {
    res = await fetch(`${API_BASE_URL}/crew/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ messages, route }),
      signal,
    })
  } catch {
    handlers.onError('Could not reach Crew. Is the backend running?')
    return
  }
  if (res.status === 503) {
    handlers.onError('Crew isn’t configured on the server yet (no API key).')
    return
  }
  if (!res.ok || !res.body) {
    handlers.onError(`Crew is unavailable (HTTP ${res.status}).`)
    return
  }

  const reader = res.body.getReader()
  const decoder = new TextDecoder()
  let buffer = ''
  while (true) {
    const { value, done } = await reader.read()
    if (done) break
    buffer += decoder.decode(value, { stream: true })
    const chunks = buffer.split('\n\n')
    buffer = chunks.pop() ?? ''
    for (const chunk of chunks) {
      const dataLine = chunk.split('\n').find((l) => l.startsWith('data:'))
      if (!dataLine) continue
      const json = dataLine.slice(5).trim()
      if (!json) continue
      let evt: { type: string; text?: string; section?: string; sub?: string | null; message?: string }
      try {
        evt = JSON.parse(json)
      } catch {
        continue
      }
      if (evt.type === 'text' && evt.text) handlers.onText(evt.text)
      else if (evt.type === 'navigate' && evt.section) handlers.onNavigate(evt.section, evt.sub ?? null)
      else if (evt.type === 'error') handlers.onError(evt.message ?? 'Crew error.')
      else if (evt.type === 'done') handlers.onDone()
    }
  }
}
