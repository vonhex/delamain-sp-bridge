# Security Policy

## Supported Versions

Only the latest release of delamain-sp-bridge is actively supported for security updates.

| Version | Supported          |
| ------- | ------------------ |
| v1.0.x  | :white_check_mark: |
| < v1.0  | :x:                |

## Reporting a Vulnerability

**Do not open a GitHub Issue for security vulnerabilities.**

If you discover a potential security risk, please report it privately by emailing **necropsyk@gmail.com**.

Please include:
- A description of the vulnerability
- Steps to reproduce the issue
- Potential impact if exploited

I will acknowledge your report within 48 hours and provide a timeline for a fix.

## Security Model

The bridge daemon (`delamaind.py`) runs on the Comma device and connects outbound to the Delamain backend over WebSocket. Keep the following in mind:

- The bridge reads sunnypilot shared memory **read-only** — it cannot control the vehicle or modify sunnypilot behaviour.
- The WebSocket connection uses `DELAMAIN_WS_URL` from the environment. Ensure this points to a trusted server, ideally over a VPN or private network.
- The bridge is exempt from JWT authentication on the backend and is assumed to be on a trusted LAN. Do not expose the backend port directly to the internet.
