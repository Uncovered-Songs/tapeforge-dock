# TapeForge User Guide

TapeForge is a four-app multitrack audio suite designed as one technical instrument with four single-purpose modules:

| App | Purpose |
|---|---|
| **Capstan** | Multitrack recorder. Captures audio from an ASIO interface onto a tape. |
| **Bridge** | Virtual outboard rack. Receives tracks from Capstan, hosts VST plugins, sends to Bus. |
| **Bus** | Summing mixer. Sums tracks to a post-master stereo bus, drives ASIO monitor out, publishes the stereo bus for Print. |
| **Print** | Mastering / archive deck. Consumes Bus's stereo bus and writes finalized mixtapes. |

A typical signal chain:

```
[ Capstan ]  →  [ Bridge ]  →  [ Bus ]  →  [ Print ]
   record         process       balance      commit
```

All four apps share the same technical / industrial visual language — they look and feel like three modules of the same instrument, not three themed apps.

## Documentation structure

- **Getting Started** — installation, first run, quickstart
- **The Four Apps** — per-app capability reference
- **User Interface** — visual language, atmospheres, instrument reference
- **Workflows** — recording, processing, mixing, printing
- **Configuration** — portable instance, machine bindings, networking
- **Troubleshooting** — common issues and solutions
