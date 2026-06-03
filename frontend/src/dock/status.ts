/* status.ts — DOCK status palette. Color communicates health/activity only.
   Ported from dock-kit.jsx (the `S` object) and the TONE/TONEBG maps. */
import { L } from '@/design/tokens'

export type Tone = 'ok' | 'warn' | 'crit' | 'info' | 'idle' | 'accent'

export const S = {
  ok: '#5C8A6B',
  okBg: '#EAF1EC',
  okBorder: '#CBDDD0',
  warn: '#C2913F',
  warnBg: '#F8F1E3',
  warnBorder: '#E6D6B4',
  crit: '#C0533B',
  critBg: '#F8EAE6',
  critBorder: '#E8C7BC',
  info: '#4A6D8C',
  infoBg: '#EAF0F5',
  infoBorder: '#C7D6E2',
  accent: L.accent,
  accentBg: L.accentBg,
  accentBorder: L.accentBorder,
  accentText: L.accentText,
  idle: '#8A93A3',
  idleBg: '#F1F3F5',
  idleBorder: '#E0E4E8',
} as const

export const TONE: Record<Tone, string> = {
  ok: S.ok,
  warn: S.warn,
  crit: S.crit,
  info: S.info,
  idle: S.idle,
  accent: S.accent,
}

/** [background, border] per tone — for filled pills/badges. */
export const TONE_BG: Record<Tone, [string, string]> = {
  ok: [S.okBg, S.okBorder],
  warn: [S.warnBg, S.warnBorder],
  crit: [S.critBg, S.critBorder],
  info: [S.infoBg, S.infoBorder],
  idle: [S.idleBg, S.idleBorder],
  accent: [S.accentBg, S.accentBorder],
}
