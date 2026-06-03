# Troubleshooting

## Common issues

### App won't start

**Instance not found**: Ensure the path points to a valid instance (contains `.tapeforge/instance.json`). Use `--instance <path>` to specify explicitly.

**Single-instance lock held**: Another instance is running. Check for a zombie process or use Task Manager to terminate it.

**No machine binding**: First-run wizard should open. If it doesn't, delete `<instance>/.tapeforge/machine-bindings/<machineId>/` and restart.

### Audio issues

**No ASIO device found**: Ensure your interface is connected and drivers are installed. Check the first-run wizard configuration.

**No audio in Bus**: Verify the input source is correct. Bus shows the source app name in its status bar.

**High latency / xRuns**: Increase buffer size in the machine binding. 256 is the default; try 512 or 1024.

**Multi-client ASIO fails**: Not all ASIO drivers support multi-client. Try running only the app that directly drives the interface.

### Network issues

**Patchbay not reachable**: Ensure `patchbay.exe` is running. Check port 9100 is not blocked.

**Can't join a network**: Verify the network UUID is correct. Instances must be on the same LAN subnet.

**Peers not showing**: mDNS relies on multicast. Ensure your network allows mDNS traffic. Check firewall settings.

### First-run wizard

**Wizard doesn't open**: Check `http://localhost:8080` (or the port for your app). If nothing serves, ensure no other app holds that port.

### Migration

**v0 → v1 migration**: See `docs/porting-from-v0.md` for the migration script contract. Use `Capstan.exe --migrate-from-localappdata` for v3 → A.1 portable instance migration.
