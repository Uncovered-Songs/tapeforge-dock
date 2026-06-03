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
