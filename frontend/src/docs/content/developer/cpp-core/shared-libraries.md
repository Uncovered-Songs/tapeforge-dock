# Shared Libraries

## tapeforge_utils

Core utilities used by every library and app.

- **Logger** — structured logging with severity levels
- **SPSCQueue** — single-producer single-consumer lock-free queue
- **TimeUtils** — ISO 8601 formatting, duration helpers
- **DebouncedFileWriter** — debounced file writes (250–500 ms) with flush-on-shutdown
- **HostPaths** — per-OS host config + log directory resolution (`%LOCALAPPDATA%` / `~/Library/Application Support` / `~/.local/share`)
- **ProcessProbe** — per-OS PID-alive check (`{win,posix}.cpp` split)
- **InstanceSentinel** — single-instance-per-host claim via `InterProcessLock`

## tapeforge_config

Machine configuration and identification.

- **MachineConfigStore** — legacy v3 machine.json reader
- **MachineId** — per-OS machine identity resolver (`{win,mac,linux}.cpp` split)

## tapeforge_tape

Tape, instance, project, and per-machine state schemas + stores.

- **InstanceConfigStore** — reads/writes `<instance>/.tapeforge/instance.json`
- **ProjectConfigStore** — reads/writes `<project>/project.json`
- **PerMachineStateStore** — reads/writes per-(project, machine) state
- **MachineBindingStore** — reads/writes per-(instance, machine, scenario) bindings
- **InstanceLayout** — canonical path constants
- **InstanceDiscovery** — mounted-volume enumeration for dongle discovery
- **TapeDirectory** — tape directory I/O (metadata, track files)
- **TapeMetadata** — tape metadata schema

## tapeforge_streaming

Inter-process audio transport.

- **SharedAudioStream** — lock-free ring-buffer producer/consumer
- **SharedMemoryRegion** — per-OS IPC primitive (`{win,posix}.cpp` split)
- **OutputMode** — `DirectASIO | ExternalStream | Hybrid` enum
- **StreamLayout** — wire format constants (`kDefaultStreamName`, `TFST` magic)

## tapeforge_audio

Audio device management.

- **AudioDeviceManager** — wraps JUCE's `AudioDeviceManager`
- **AudioEngineBase** — `juce::AudioIODeviceCallback` base class for apps

## tapeforge_web

HTTP/WebSocket server.

- **WebServer** — wraps Crow's `SimpleApp`, takes a per-app routes registrar
- **WebSocketServer** — WebSocket endpoint management

## tapeforge_plugins

VST3 plugin hosting.

- **VstHost** — plugin scanning and instantiation
- **SharedVstInstance** — shared plugin instance across tracks
- **VstInstancePool** — pool management
- **VstPluginRef** — generic plugin reference `{id, vst3Path, sharedInstanceGroup}`

## tapeforge_network

mDNS discovery and federation primitives.

- **MdnsService** — per-OS mDNS (`{win,mac,linux}.cpp` split)
- **NetworkIdentity** + **NetworkIdentityStore** — network membership
- **RegistrationDoc** + **ProductEntry** — product registration schemas
- **MembershipTable** — peer tracking with expiry
- **ElectionEngine** — lowest-UUID-wins leader election
- **NetworkStateDoc** + **NetworkStateCacheStore** — network state
- **PatchbayClient** — per-product patchbay registration helper

## tapeforge_wizard

First-run wizard server.

- **SetupServer** — Crow-based HTTP setup wizard
- **AsioEnumerator** — ASIO device enumeration without opening
- **WizardLock** — sentinel for concurrent wizard launches

## tapeforge_license

License verification (stub).

- **LicenseChecker::verify()** — currently returns `LicenseStatus::Ok`
- Full enforcement (Ed25519 verification, dongle binding, polling) deferred
