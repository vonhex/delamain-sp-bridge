# Contributing to delamain-sp-bridge

Thanks for taking the time to contribute. Here's everything you need to know.

## Before you start

- **Bug fix or small improvement?** Open a PR directly — no need to ask first.
- **New feature or significant change?** Open an issue first to discuss it. Avoids wasted effort if the direction doesn't fit the project.
- **Question or help needed?** Use [GitHub Discussions](https://github.com/vonhex/delamain-sp-bridge/discussions) rather than opening an issue.

## Development setup

The bridge runs directly on the Comma device. See the [README](../README.md) for deployment instructions.

```bash
git clone https://github.com/vonhex/delamain-sp-bridge.git
cd delamain-sp-bridge

# Deploy to your Comma device
COMMA_IP=<your-comma-ip> ./deploy.sh
```

## How to contribute

1. Fork the repository and create a branch from `main`
2. Make your changes — keep them focused on one thing per PR
3. Test on a real Comma device where possible
4. Open a pull request against `main` using the PR template

## What makes a good PR

- **Focused** — one logical change per PR; easier to review and revert if needed
- **No scope creep** — don't refactor surrounding code unless it's directly related
- **No unnecessary comments** — code should be self-explanatory; only comment the *why* when it's non-obvious
- **Tested on hardware** — changes to event detection or telemetry should be verified on a real device

## Code style

- **Python:** Follow existing patterns. Type hints where they add clarity. Match the surrounding code style.

## Reporting bugs

Use the **Bug Report** issue template. Include your sunnypilot version, Comma device model, and any relevant logs from `logcat` or the bridge output.

## Feature requests

Use the **Feature Request** issue template. Explain the use case — what driving event or telemetry data you need and why.

## License note

By contributing, you agree that your contributions will be licensed under the same [noncommercial license](../LICENSE) as the rest of the project.
