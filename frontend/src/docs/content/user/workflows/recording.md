# Recording Workflow

## Setup

1. **Connect your audio interface** — ensure ASIO drivers are installed
2. **Launch Capstan** — `Capstan.exe --instance "D:\MyTapeForge"`
3. **Create a tape** — via the web UI: name + duration
4. **Arm tracks** — click arm buttons on the tracks you want to record

## Recording

1. Press **REC** to arm recording, then **PLAY** to start
   - Or press **REC** alone — Capstan enters REC+PLAY mode
2. Monitor levels via the VU meters on each armed track
3. Press **STOP** to end the recording session

## After recording

- Tracks appear in the tape as `track_NN.rawf32` files
- You can rename the tape, add notes, or create a new tape
- The tape is immediately available for Bridge to process or Bus to mix

## Transport behavior

| Action | Behavior |
|---|---|
| PLAY | Accelerates from 0 to 1× speed (exponential ramp, τ = 0.16 s) |
| STOP | Decelerates to 0 |
| REW/FF | Steps through wind speeds: 5× → 10× → 20× |
| REC | Cannot REW/FF during active recording (returns 409) |
