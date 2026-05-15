# Delamain — sunnypilot Bridge

> Bridge daemon that connects [Delamain AI](https://github.com/vonhex/delamain) to your sunnypilot device (Comma 4 / Comma 3X).

`delamaind.py` runs on the Comma device, reads vehicle state from sunnypilot's shared memory (`/dev/shm/msgq_*`), and streams telemetry and events to the Delamain backend over WebSocket — without registering as a msgq reader so openpilot is completely unaffected.

---

## What it does

- Streams live vehicle telemetry at 2 Hz (speed, ACC, lead distance, GPS, steering)
- Fires voice events: hard braking, ACC engage/disengage, lane changes, speeding, lead car proximity, thermal warnings, seatbelt alerts, SP alerts
- Captures road camera frames on demand (for Delamain's vision Q&A feature)
- Sends drive milestones (20 / 45 / 90 min into trip)
- Auto-reconnects with exponential backoff

---

## Prerequisites

- Comma 4 or Comma 3X running **sunnypilot** (not stock openpilot)
- SSH access to the device
- The Delamain backend running and reachable from the Comma device
  - See [vonhex/delamain](https://github.com/vonhex/delamain) for setup

---

## Installation

### 1. Edit the WebSocket URL

Open `delamaind.py` and set `DELAMAIN_WS_URL` to your Delamain backend, or set the `DELAMAIN_WS_URL` environment variable:

```python
DELAMAIN_WS_URL = "wss://your-delamain-host/ws/sunnypilot-bridge"
```

If your backend is on your home network and the Comma connects to the same network, you can use `ws://192.168.x.x:8888/ws/sunnypilot-bridge`.

### 2. SSH into your Comma device

Find your Comma's IP in **Settings → Device → SSH**:

```bash
ssh comma@<COMMA_IP>
```

Default SSH port is 22. The default password is `comma` (or set in your Comma account).

### 3. Create the Delamain directory on device

```bash
ssh comma@<COMMA_IP> "mkdir -p /data/delamain"
```

### 4. Copy the bridge script

```bash
scp delamaind.py comma@<COMMA_IP>:/data/delamain/delamaind.py
```

### 5. Start the bridge

```bash
ssh comma@<COMMA_IP> \
  "PYTHONPATH=/data/openpilot DELAMAIN_WS_URL=wss://your-host/ws/sunnypilot-bridge \
   PYTHONUNBUFFERED=1 nohup /usr/local/venv/bin/python3 -u \
   /data/delamain/delamaind.py >> /data/delamain/delamaind.log 2>&1 &"
```

Check it started:

```bash
ssh comma@<COMMA_IP> "tail -20 /data/delamain/delamaind.log"
```

You should see:
```
[Delamain] waiting for openpilot controlsd...
[Delamain] openpilot ready
[Delamain] waiting for network...
[Delamain] network ready
[Delamain] connecting to wss://your-host/ws/sunnypilot-bridge ...
[Delamain] WebSocket connected
```

### 6. Make it persistent across reboots

SSH into the device and create a launch script:

```bash
ssh comma@<COMMA_IP> "cat > /data/delamain/launch.sh << 'EOF'
#!/bin/bash
export PYTHONPATH=/data/openpilot
export DELAMAIN_WS_URL=wss://your-host/ws/sunnypilot-bridge
export PYTHONUNBUFFERED=1
exec /usr/local/venv/bin/python3 -u /data/delamain/delamaind.py >> /data/delamain/delamaind.log 2>&1
EOF
chmod +x /data/delamain/launch.sh"
```

Then add it to sunnypilot's `launch_chffrplus.sh` or use sunnypilot's custom launch script support.

---

## Quick deploy script

Edit `COMMA` and `DELAMAIN_WS_URL` at the top of `deploy.sh`, then run from your laptop:

```bash
bash deploy.sh
```

This will `scp` the bridge, restart it, and tail the log.

---

## Disabling Driver Monitoring (optional)

sunnypilot's driver monitoring camera can interfere with comfort during long drives. Two scripts are provided:

- `disable_driver_monitoring.sh` — runs on the Comma device, patches `process_config.py`
- `deploy_disable_dm.sh` — copies and runs the above remotely from your laptop

```bash
bash deploy_disable_dm.sh
```

Then restart sunnypilot:

```bash
ssh comma@<COMMA_IP> "sudo systemctl restart comma"
```

> **Note:** This patches sunnypilot's source files. It may need to be re-applied after sunnypilot updates.

---

## Troubleshooting

**Bridge won't connect**
- Check `DELAMAIN_WS_URL` — the Comma must be able to reach the backend
- If using a public domain, ensure port 443 (wss) or 8888 (ws) is open
- Check the log: `ssh comma@<IP> "tail -50 /data/delamain/delamaind.log"`

**No telemetry in Delamain dashboard**
- Confirm the bridge log shows "WebSocket connected"
- Confirm the SP status indicator in the Delamain UI is green

**Events firing but no audio**
- Check F5-TTS is running on the backend (first event synthesizes, cache warms)
- Check the backend log for TTS errors

---

## How it works

`delamaind.py` uses a custom `MsgqReader` that opens `/dev/shm/msgq_<topic>` read-only via `mmap` and tracks the write pointer without registering as a reader. This means:

- No impact on sunnypilot's internal message counts
- Safe to start/stop/crash at any time
- Works even if a topic hasn't been published yet (waits and retries)

Topics read: `carState`, `radarState`, `gpsLocationExternal`, `selfdriveState`, `liveMapDataSP`, `deviceState`
