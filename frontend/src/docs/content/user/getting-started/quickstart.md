# Quickstart

This guide gets you recording and listening back in under five minutes.

## 1. Set up your instance

1. Plug in a USB drive or create a folder anywhere.
2. Launch **Capstan.exe --instance "D:\MyTapeForge"** (substitute your path).
3. The first-run wizard opens in your browser. Configure:
   - **Role**: Recorder
   - **ASIO device**: Select your audio interface
   - **Sample rate**: 48000 Hz
   - **Buffer size**: 256 samples
4. Click Apply. Capstan exits.
5. Relaunch **Capstan.exe --instance "D:\MyTapeForge"**.

## 2. Create a tape

With Capstan running, open `http://localhost:8080` in your browser (or the port Capstan reports).

Click **Create Tape**, enter a name and duration (e.g., 15 minutes), and confirm.

## 3. Arm and record

1. Arm track 1 by clicking its arm button.
2. Press **REC** then **PLAY** (or just **REC** to arm + record in one action).
3. Play your instrument. The track's VU meter shows input level.
4. Press **STOP** when done.

## 4. Listen back

1. Press **STOP** (if recording), then **REW** to go to the beginning.
2. Press **PLAY**. Your recorded track plays through the ASIO outputs.

## Next steps

- Add **Bridge** for VST processing
- Add **Bus** for mixing and monitoring
- Add **Print** for mastering and archiving

See the [Workflows](../workflows/recording.md) section for detailed guides.
