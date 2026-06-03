import { computed, readonly, ref } from 'vue'

/* Shared reactive viewport width. A single module-level ref + one resize
   listener is shared across every component that calls useBreakpoint(), so we
   don't attach N listeners. The inline-style architecture can't be driven by
   CSS media queries (inline styles win specificity), so layout branches read
   these reactive booleans instead. */

export const MOBILE_MAX = 639
export const TABLET_MAX = 1023

const width = ref(typeof window !== 'undefined' ? window.innerWidth : 1280)

let initialized = false
function init() {
  if (initialized || typeof window === 'undefined') return
  initialized = true
  const onResize = () => {
    width.value = window.innerWidth
  }
  window.addEventListener('resize', onResize, { passive: true })
  onResize()
}

export function useBreakpoint() {
  init()
  const isMobile = computed(() => width.value <= MOBILE_MAX)
  const isTablet = computed(() => width.value > MOBILE_MAX && width.value <= TABLET_MAX)
  const isDesktop = computed(() => width.value > TABLET_MAX)
  // mobile OR tablet — i.e. anything below the desktop layout
  const isCompact = computed(() => width.value <= TABLET_MAX)
  return { width: readonly(width), isMobile, isTablet, isDesktop, isCompact }
}
