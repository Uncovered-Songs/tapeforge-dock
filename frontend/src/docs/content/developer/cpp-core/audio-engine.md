# Audio Engine & Algorithms

This is the heart of TapeForge: how live audio actually moves through the system,
and the algorithms that keep it **sample-aligned**, **low-latency**, and **alive**
under load. Read this top to bottom — each section builds on the previous one.

> **One sentence:** PATCH owns the soundcard, and once per audio buffer it runs
> the whole graph (Capstan → Bridge → Bus → Print) in lockstep, moving every
> channel's audio through shared-memory rings that it keeps time-aligned by
> always reading the *most recent* block.

---

## 1. The big idea: one clock, one graph

A digital audio interface (the Audient, here) calls back at a fixed cadence:
"here are `N` input samples, give me `N` output samples." At 44.1 kHz with a
128-sample buffer that callback fires every **~2.9 ms**, and everything for those
128 samples must be done before it returns or you get a dropout (a click/gap).

TapeForge is **five separate processes** (PATCH + the four products). The danger
with multiple processes touching one audio stream is that they drift out of time
with each other. TapeForge avoids this with a single rule:

- **PATCH is the only process that opens the soundcard (ASIO).**
- Every audio buffer, PATCH **drives** each product in turn, waiting for each to
  finish before moving on. The products don't have their own audio clock; they
  run *because PATCH told them to*, exactly once per buffer.

So there is **one clock** (PATCH's ASIO callback) and **one pass** through the
graph per buffer. This is what makes cross-process audio stay in sample-lockstep.

Where the config for that one clock lives (device, sample rate, buffer size):
the per-machine **MachineBinding** JSON, read by `apps/patchbay/backend/src/main.cpp`
at startup. The products inherit sample rate + buffer size from PATCH; they never
open the device themselves.

---

## 2. Who owns audio

| Process | Role in audio |
|---|---|
| **PATCH** (patchbay) | Opens ASIO. Runs the audio callback. Orchestrates the whole graph each buffer. Owns the per-channel routing streams. |
| **Capstan** | Tape deck. Produces tape playback; records incoming audio to disk. |
| **Bridge** | Insert processor. Runs the FX/plugin chain on channels that have their insert engaged. |
| **Bus** | Mixer. Sums all channels to the main/monitor outputs. |
| **Print** | Mastering. Final stereo stage before the speakers. |

The product audio code is reached only through PATCH's per-buffer "go" signal.
Outside that, products just run their UI/HTTP servers.

Key files:
- `apps/patchbay/backend/src/PatchAudioEngine.cpp` — the ASIO callback owner.
- `apps/patchbay/backend/src/GraphScheduler.cpp` — `executeGraph()` is the whole
  per-buffer algorithm (sections 3–8 below all live here).

---

## 3. One cycle of `executeGraph()` — the forward chain

This is the central algorithm. Every audio buffer, PATCH runs these steps **in
order**, for all channels, within the single callback:

```
                 ┌──────────────────────────────────────────────┐
   ASIO in  ───► │ 1. drive(Capstan)   → tape playback ready     │
                 │ 2. per channel front-end:                     │
                 │      pick source  A=live-in  /  B=tape-return  │
                 │      tap it DRY → record send (pre-insert)     │
                 │      insert ON?  → send to Bridge              │
                 │              OFF → keep as the channel feed    │
                 │ 3. drive(Bridge)    → processes engaged sends  │
                 │ 4. read each engaged channel's processed return│
                 │ 4b. write every channel's feed → channel-in    │
                 │      (through the alignment delay, section 7)  │
                 │ 5. drive(Bus)       → sums to main/monitor     │
                 │ 6. drive(Print)     → masters the main bus     │
                 │ 7. read product outputs → ASIO out             │ ───► ASIO out
                 └──────────────────────────────────────────────┘
```

Because every leg resolves **in the same cycle**, an engaged insert adds **no
extra buffer** of latency — the send goes to Bridge and the processed return
comes back before Bus reads the channel, all within one 2.9 ms callback. This is
the "inline insert" model (it replaced an older design that looped back a buffer
later).

**A / B per channel:**
- **A** = the live interface input (a physical ASIO input mapped to this channel).
- **B** = the tape return (what Capstan is playing back on this track).
The operator picks A or B per channel in the Bus UI; PATCH enacts the choice.

**The dry record tap** is taken *before* the insert, always following A/B. So
what you record is the clean source, regardless of what the insert does to the
monitor — see section 11.

---

## 4. Cross-process lockstep: GraphSync

How does PATCH "drive" a product and *wait* for it, across process boundaries,
fast enough to fit in a 2.9 ms budget? With a tiny cross-process handshake called
**GraphSync** (`shared/cpp/audio/src/GraphSync.h`):

```
PATCH                                Product (e.g. Bridge)
  signalInputsReady()  ───────────►   (wakes, runs processGraph: read inputs,
                                        process, write outputs)
  waitOutputsReady()   ◄───────────   signalOutputsReady()
  (proceeds to next stage)
```

PATCH signals "your inputs are ready," the product processes one buffer, signals
"outputs ready," PATCH continues. It's a barrier: PATCH doesn't move to Bus until
Bridge has produced this cycle's audio.

**What if a product is slow or stalls?** PATCH can't wait forever (that would
blow the 2.9 ms budget and dropout). So:

- `waitOutputsReady()` has a short timeout (`kSyncTimeoutMs`, 2 ms).
- If a product times out `kMaxConsecutiveTimeouts` (10) times in a row, PATCH
  **backs off** driving it for a while (`kSyncBackoffCycles`) and retries later —
  it does **not** evict the product from the graph.
- A backed-off / absent processor makes its channels fall through **dry** (the
  un-processed source), never silence, never a wedge.

This is why a momentarily-overloaded Bridge causes a brief glitch, not a crash —
and each backoff is counted (section 10, "stage stalls").

---

## 5. Shared-memory streaming: the rings

Audio crosses process boundaries through **lock-free ring buffers** in named OS
shared memory (Windows file mappings / POSIX `shm`). One ring = one mono audio
"pipe." The binary layout is `'TFST'` v2 (`shared/cpp/streaming/src/StreamLayout.h`):

```
┌────────────────────────────────────────────┐
│ StreamHeader   (magic, sr, channels,        │
│                 ringFrames, writePosition…)  │
├────────────────────────────────────────────┤
│ ConsumerSlot[8]  (per-reader: connected,    │
│                   readPosition, heartbeat)   │
├────────────────────────────────────────────┤
│ float32 ring  [channels][ringFrames]         │
└────────────────────────────────────────────┘
```

- **Producer** (`SharedAudioStream`): writes a block and advances
  `writePosition`. One writer.
- **Consumer** (`GraphStreamReader` in PATCH-driven mode): reads from its own
  `readPosition`, claims a `ConsumerSlot`, updates a heartbeat.

**Standing depth** = `writePosition − readPosition` — how many written-but-unread
frames sit in the ring for that reader. This single number is the key to
alignment (section 7). It's exposed per leg on `GET /patchbay/graph` for
diagnosis.

> **Gotcha (logged, not yet fixed):** `GraphStreamReader` stamps its heartbeat
> with `GetTickCount64`, but the producer's reclaim monitor uses `steady_clock`.
> Different clock domains → the producer thinks live consumers are stale and
> clears their slot. Audio is unaffected (readers don't check the flag), but the
> producer-side "connected consumers" / write-leg depth gauges read wrong.

The PATCH-owned per-channel streams (one set per Bus channel):

| Stream | Written by | Read by | Carries |
|---|---|---|---|
| `tf_chin_<n>` | PATCH | Bus | the final channel feed → mixer |
| `tf_psend_<n>` | PATCH | Bridge | the insert send (pre-process) |
| `tf_prec_<n>` | PATCH | Capstan | the dry record tap |
| `capstan track-out-<n>` | Capstan | PATCH | tape playback (the "B" source) |
| `bridge proc-out-<n>` | Bridge | PATCH | the processed insert return |

---

## 6. The inline insert (forward chain)

For one channel, with its insert **engaged**, one cycle looks like:

```
 source (A live / B tape)
     │  (PATCH copies it to scratch)
     ├──────────────► tf_prec_n  ─────► Capstan (records the DRY signal)
     │
     └─► tf_psend_n ─► Bridge (FX chain) ─► bridge proc-out_n ─► PATCH
                                                                   │
                                              tf_chin_n ◄──────────┘
                                                   │
                                                   ▼
                                                  Bus (mixes it)
```

With the insert **bypassed**, the source skips Bridge and goes straight to
`tf_chin_n`. Either way the channel feed reaches Bus **the same cycle**.

If Bridge missed its slot this cycle (backoff/stall), PATCH writes the **dry**
source to `tf_chin_n` instead of the processed return — the channel stays audible.

The insert processor is **graph-defined**, not hardwired: by default it's Bridge,
but the operator can repoint a channel's send/return to a different processor in
the graph editor, or disconnect it (normalled straight through).

---

## 7. Alignment — the core algorithm (read-latest)

This is the subtle part, and the bug that drove the most recent work.

**The requirement:** every channel must reach the Bus mix on the *same sample*,
regardless of its routing (A vs B, insert on/off, which processor). If one channel
is even one block (128 samples ≈ 2.9 ms) out of step, identical content on two
channels combs/flanges — you hear it as a "reverb between copies."

**Why drift happens.** A ring reader keeps a *standing depth*
(`writePosition − readPosition`). If the reader reads strictly sequentially, that
depth is whatever it was when reading started — and any momentary hiccup that
bumps it (the producer briefly gets ahead by a block) is then **preserved
forever**, because in lockstep the reader consumes exactly one block per cycle. So
one channel can end up permanently a block behind the others → the comb.

**The fix: read-latest (`GraphStreamReader::readLatestBlock`).** Instead of
reading sequentially, each cycle PATCH snaps the read cursor to the **most recent**
block before reading:

```
readPosition = writePosition − framesWanted;   // drop any backlog, read newest
```

Consequences:
- In steady lockstep (producer advances exactly one block per cycle), this snap
  lands exactly where the previous read ended → **perfectly contiguous, no click.**
- Every channel reads the newest block at the same point in the cycle → they all
  share the **same minimal standing depth** regardless of when they attached →
  **no inter-channel drift, no comb.**
- After a real hiccup (the producer skipped/doubled a block), read-latest
  **re-aligns** by dropping/repeating one block — a single ~1-sample "resync"
  click instead of a permanent offset. (A click you barely hear vs a reverb you
  definitely do.) Each such event is counted (section 10, "resyncs").
- It also fixes the **A→B flip**: a tape reader that sat unread while the channel
  was on "A" had a huge backlog; read-latest discards it and lands on the current
  tape position instead of a ring-length behind.

PATCH uses `readLatestBlock` for both the tape (B) and insert-return (proc) reads
in `executeGraph`.

**Trade-off the operator chose:** *misalignment is worse than latency.* Read-latest
keeps everything aligned at the cost of an occasional tiny resync click on a
hiccup — which is acceptable, and which the glitch counter makes visible.

---

## 8. Plugin Delay Compensation (PDC)

Some plugins delay their output internally (lookahead limiters, linear-phase EQ,
oversampling). If an inserted plugin reports `N` samples of latency, the processed
channel would arrive `N` samples after the bypassed/dry channels → misalignment.

The mechanism (built, but **dormant for the current SSL strip**, which reports
zero latency):

1. **Bridge** sums its chain's reported latency
   (`Module::latencySamples()` → `ProcessingRow` → `ProcessingChain::totalLatencySamples()`,
   reading each plugin's `getLatencySamples()`) and reports it to PATCH —
   `POST /patchbay/insert-latency`, on every rack change and ~1 Hz (because a
   VST often only publishes its latency *after* it has processed a few blocks).
2. **PATCH** delay-aligns: it runs every channel's feed through a per-channel
   delay line in `executeGraph` step 4b. Engaged channels tap at 0 (already
   plugin-delayed); bypassed/live channels tap at `L` (the reported latency). So
   every channel ends up equally delayed → aligned. At `L = 0` it's a pure
   passthrough (no added latency).

> **Important nuance:** the recent "reverb between copies" was **not** PDC — it
> was the ring standing-gap drift from section 7, fixed by read-latest. PDC
> handles a *different* source of misalignment (genuine plugin delay) and is in
> place for when a latency-reporting plugin is used. If a plugin *hides* its
> latency, the robust path is to *measure* the round-trip with an impulse inside
> PATCH (a documented follow-up).

---

## 9. The latency model

What you're actually monitoring through, end to end, is roughly:

```
ASIO input latency  +  processing block  +  (insert PDC)  +  ASIO output latency
        +  PATCH's internal ring depth (small, the alignment target)
```

PATCH exposes a readout on `GET /patchbay/hardware → latency` and in the patchbay
status bar (`LAT`). It currently reports the **config estimate** (ASIO in + out +
block + PDC); it does **not yet** include the internal ring depth — making it
sample-accurate is a follow-up (it needs the impulse measurement). On the Audient
at 128/44.1k that estimate is **193 in + 241 out + 128 block ≈ 562 samples ≈
12.7 ms** — note that's the *driver's* latency at 128 samples, the dominant term.

---

## 10. Health & telemetry — "how far from the limit"

Because the whole graph must finish inside the buffer period, the meaningful
"CPU" metric isn't OS load — it's **audio-graph load**: the fraction of the buffer
period that one `executeGraph` pass (PATCH + every product it waits on) consumes.
PATCH times the callback and reports it on `GET /patchbay/hardware → telemetry`,
shown in the patchbay status bar as `DSP %` (current + recent peak). Approaching
100% means no headroom → dropouts.

Three **session glitch counters** quantify hiccups (reset via
`POST /patchbay/telemetry/reset` or by clicking the readout):

| Counter | What it counts | Cause |
|---|---|---|
| **overruns** | callback exceeded the buffer period | the whole graph is over budget (real dropout) |
| **stage stalls** | a product missed its slot and got backed off | one product (usually Bridge) is overloaded |
| **resyncs** | a read-latest leg dropped/repeated a block | a momentary block-desync re-aligned (the ~1-sample cracks) |

These let the operator *see* what's happening: rising `resyncs` = the small
cracks; `DSP peak` near 100% = at the CPU limit; `stage stalls` = a specific
product choking.

---

## 11. Recording: latency-compensated capture

When you record while monitoring, your input arrives "late" relative to the tape
timeline: tape plays → speakers → you react and play → input comes back, a full
round-trip later. If recorded at the current playhead, the take would land late.

Capstan compensates: it writes the incoming (dry) audio at an **earlier** tape
position, shifted back by the round-trip latency
(`AudioEngine.cpp` — `recordPosition = headPosition − latencyComp`). It uses an
impulse-**calibrated** round-trip figure when available (which folds in the real
path latency), else the driver's reported sum. The recorded signal is the **dry
pre-insert tap** (`tf_prec_n`), so what lands on tape is clean regardless of the
monitor insert. *(Folding the live insert PDC into this shift automatically is a
documented follow-up — "record-shift compensation.")*

---

## 12. The graph is rebuilt safely (double buffering)

Routing changes (a product registers, the operator rewires a port) rebuild the
graph. The audio thread reads the graph **lock-free**, so the rebuild must never
mutate the graph the callback is currently reading. The scheme:

- Two graph buffers + a retired slot; rebuild fills the inactive buffer, then
  **atomically swaps** the active pointer. The just-retired graph is kept alive
  one extra generation so any in-flight callback finishes safely.
- **Coalescing:** rebuilds are funneled through a single-flight `requestRebuild()`
  so a burst of edits collapses into one rebuild instead of many. This matters:
  firing many rebuilds back-to-back (e.g. delete + relink several ports rapidly)
  used to move the active graph's data out from under the audio callback →
  use-after-free crash (`0xc0000409`). Coalescing the manual-edit path fixed that.

> **Latent hardening (logged):** even one rebuild has a narrow window where it
> moves the just-unpublished graph's vectors while a callback might still be
> reading them. Coalescing makes it rare; the real fix is to triple-buffer the
> graph (build into a buffer that's been idle two generations) — a documented
> follow-up.

---

## 13. How it stays alive (failure philosophy)

Every risky path degrades gracefully instead of dropping out or crashing:

- **Processor stalled/absent** → engaged channels fall through **dry**, never
  silence.
- **A product slow to start** → backed off and retried, never evicted.
- **Ring desync** → **re-aligned** (one resync click), never a permanent comb.
- **Reader can't attach yet** → reads silence and retries (lazy attach), the
  producing stream may not exist at the instant the reader opens.

The guiding principle: **alignment and continuity first.** A momentary click is
acceptable; a permanent timing offset or a dropout is not.

---

## Where to read the code

| Topic | File |
|---|---|
| ASIO callback owner | `apps/patchbay/backend/src/PatchAudioEngine.cpp` |
| The whole per-buffer algorithm | `apps/patchbay/backend/src/GraphScheduler.cpp` (`executeGraph`) |
| Cross-process lockstep | `shared/cpp/audio/src/GraphSync.h` |
| Ring producer / consumer | `shared/cpp/streaming/src/SharedAudioStream.*`, `GraphStreamReader.*` |
| Wire format | `shared/cpp/streaming/src/StreamLayout.h` |
| Bridge FX chain + PDC | `apps/bridge/backend/src/processing/`, `audio/AudioEngine.cpp` |
| Capstan record compensation | `apps/capstan/backend/src/audio/AudioEngine.cpp` |
| The investigation that produced read-latest/PDC/telemetry | `openspec/changes/tapeforge-patch-latency-alignment/` |
