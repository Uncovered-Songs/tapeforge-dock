# C++ Core Overview

The C++ code lives in three tiers: `vendor/`, `shared/cpp/`, and `apps/<name>/backend/`.

## Directory structure

```
shared/cpp/
├── utils/          tapeforge_utils — Logger, SPSCQueue, TimeUtils, DebouncedFileWriter, HostPaths, ProcessProbe, InstanceSentinel
├── config/         tapeforge_config — MachineConfigStore, MachineId resolver
├── tape/           tapeforge_tape — InstanceConfigStore, ProjectConfigStore, PerMachineStateStore, MachineBindingStore, InstanceLayout, InstanceDiscovery, TapeDirectory
├── streaming/      tapeforge_streaming — SharedAudioStream, SharedMemoryRegion, OutputMode, StreamLayout
├── audio/          tapeforge_audio — AudioDeviceManager, AudioEngineBase
├── web/            tapeforge_web — WebServer, WebSocketServer
├── plugins/        tapeforge_plugins — VstHost, SharedVstInstance, VstInstancePool
├── network/        tapeforge_network — MdnsService, NetworkIdentity, RegistrationDoc, MembershipTable, ElectionEngine, PatchbayClient
├── wizard/         tapeforge_wizard — SetupServer, AsioEnumerator, WizardLock
└── license/        tapeforge_license — LicenseChecker (stub)
```

## Library dependencies

```
tapeforge_utils        → juce_core, juce_events
tapeforge_config       → tapeforge_utils, juce_core
tapeforge_tape         → tapeforge_utils, juce_core
tapeforge_streaming    → tapeforge_utils, juce_core
tapeforge_audio        → tapeforge_utils, juce_audio_basics, juce_audio_devices, juce_core, juce_events
tapeforge_web          → tapeforge_utils, tapeforge_third_party (Crow), juce_core
tapeforge_network      → tapeforge_utils, tapeforge_tape, juce_core
tapeforge_plugins      → tapeforge_utils, juce_audio_processors
tapeforge_wizard       → tapeforge_utils, tapeforge_config, tapeforge_tape, tapeforge_network, tapeforge_third_party, juce_core, juce_audio_devices
tapeforge_license      → tapeforge_utils, juce_core
```

## App link matrix

| Library | Capstan | Bridge | Bus | Print | Patchbay |
|---|---|---|---|---|---|
| utils | ✓ | ✓ | ✓ | ✓ | ✓ |
| config | ✓ | ✓ | ✓ | ✓ | ✓ |
| tape | ✓ | ✓ | ✓ | ✓ | ✓ |
| streaming | ✓ | ✓ | ✓ | ✓ | ✗ |
| audio | ✓ | ✓ | ✓ | ✓ | ✗ |
| web | ✓ | ✓ | ✓ | ✓ | ✓ |
| network | ✓ | ✓ | ✓ | ✓ | ✓ |
| plugins | ✗ | ✓ | ✓ | ✗ | ✗ |
| wizard | ✓ | ✓ | ✓ | ✓ | ✗ |
| license | ✓ | ✓ | ✓ | ✓ | ✓ |

## Namespace strategy

| Namespace | Location |
|---|---|
| `tapeforge::` | Shared code in `shared/cpp/` |
| `tapeforge::config::` | Config layer |
| `tapeforge::tape::` | Tape/instance/project schemas |
| `tapeforge::streaming::` | Streaming layout |
| `tapeforge::web::` | Web server |
| `tapeforge::plugins::` | VST hosting |
| `tapeforge::network::` | mDNS + federation |
| `tapeforge::<app>::` | Per-app code in `apps/<app>/backend/` |
