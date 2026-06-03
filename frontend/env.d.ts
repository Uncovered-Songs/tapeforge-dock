/// <reference types="vite/client" />

interface ImportMetaEnv {
  /** Base URL of the TapeForge Dock backend API (e.g. http://localhost:8001/api/v1). */
  readonly VITE_DOCK_API_BASE_URL?: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
