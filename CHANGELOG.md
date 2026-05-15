# Changelog

All notable changes to delamain-sp-bridge are documented here.

---

## [1.0.0] — 2026-05-15

### Added
- **`delamaind.py`** — bridge daemon that reads sunnypilot msgq shared memory and streams telemetry and vehicle events to the Delamain backend over WebSocket.
- **Vehicle event detection** — hard brake, very hard brake, rapid acceleration, lane changes, lead car proximity, high speed, ACC engage/disengage, stopped in traffic, seatbelt, sunnypilot alerts, speeding, steer override, personality change, thermal warnings, and drive duration milestones.
- **Telemetry streaming** — speed, cruise speed, ACC state, lead distance, speed limit, GPS coordinates streamed at 2 Hz.
- **Road camera snapshots** — VisionIPC integration to capture and send JPEG frames on demand for Delamain's vision feature.
- **Car identity reporting** — brand and fingerprint sent to backend on connect.
- **`deploy.sh`** — one-command SSH deployment to the Comma device.
- **`disable_driver_monitoring.sh`** — helper script to suppress driver monitoring alerts during bridge use.
