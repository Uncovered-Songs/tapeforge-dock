# Composables

`@tapeforge/composables` provides shared Vue 3 runtime concerns used by all four apps.

## useStatus

```ts
useStatus<T>(statusPath: string, options?: { pollInterval?: number }): {
  status: Ref<T | null>,
  error: Ref<Error | null>,
  loading: Ref<boolean>,
}
```

Long-polling composable for `/status` endpoints. Default 1 Hz poll rate. Used by every app's shell for the live status display.

## useWebSocket

```ts
useWebSocket(url: string, options?: { autoReconnect?: boolean, reconnectDelay?: number }) : {
  send: (data: unknown) => void,
  subscribe: <T>(event: string, handler: (payload: T) => void) => void,
  connected: Ref<boolean>,
}
```

Auto-reconnect WebSocket client with typed event subscription. *(Wired for patchbay events; product WS routes forthcoming)*

## useTransport

```ts
useTransport(baseUrl: string): {
  play: () => Promise<void>,
  stop: () => Promise<void>,
  record: () => Promise<void>,
  forward: () => Promise<void>,
  rewind: () => Promise<void>,
}
```

Transport command dispatch for Capstan and Print.

## useMix

```ts
useMix(baseUrl: string): {
  setFader: (strip: number, value: number) => Promise<void>,
  setPan: (strip: number, value: number) => Promise<void>,
  setMute: (strip: number, value: boolean) => Promise<void>,
  setSolo: (strip: number, value: boolean) => Promise<void>,
  setMasterFader: (side: 'L' | 'R', value: number) => Promise<void>,
  setMasterLinked: (value: boolean) => Promise<void>,
}
```

Bus mixer dispatcher. All setters share the `{"value": T}` body shape.

## useRack

```ts
useRack(baseUrl: string): {
  addRow: (moduleId: string) => Promise<number>,
  setRowType: (index: number, moduleId: string) => Promise<void>,
  removeRow: (index: number) => Promise<void>,
  setRowParameter: (index: number, paramId: string, value: number) => Promise<void>,
}
```

Bridge rack mutation dispatcher.

## useTape

```ts
useTape(baseUrl: string): {
  createTape: (name: string, durationMinutes: number) => Promise<Tape>,
  listTapes: () => Promise<Tape[]>,
  selectTape: (tapeId: string) => Promise<void>,
}
```

Tape operations + listing for Capstan.

## useTapeClock

```ts
useTapeClock(sampleRate?: number): {
  position: Ref<number>,
  rateMultiplier: Ref<number>,
  play: () => void,
  stop: () => void,
  forward: () => void,
  rewind: () => void,
}
```

Rate-smoothed tape mechanics clock. Uses exponential rate ramp (τ = 0.16 s) matching the C++ audio engine. Each animation frame:
- `currentRate += α × (targetRate - currentRate)`
- `position += currentRate × sampleRate × dt`

Exposes `rateMultiplier` for downstream consumers (reel rotation, tape SFX).

## useDragPan

```ts
useDragPan(elementRef: Ref<HTMLElement | null>, options: {
  horizontal?: boolean,
  vertical?: boolean,
  noPanSelector?: string,
}): {
  isPanning: Ref<boolean>,
  onPointerDown: (e: PointerEvent) => void,
}
```

Click-drag pan for product surfaces. The viewport implements its pan inline (keeps `@tapeforge/ui` zero-dep on composables).
