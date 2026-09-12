# Contributing

This project aims to remain a small Kodi front end to NetworkManager rather than becoming a replacement network stack.

## Design rules

Changes should preserve these boundaries:

- NetworkManager remains the source of truth.
- Existing saved profiles should be activated, not rewritten.
- Do not edit netplan, wpa_supplicant, DNS, routes, or autoconnect policy.
- Do not add `sudo`, background daemons, dispatcher scripts, or custom services.
- Do not delete NetworkManager profiles.
- Prefer documented `nmcli` behaviour and Kodi APIs over custom networking logic.
- New functionality should remain controller-friendly inside Kodi.

## Security and privacy

Never commit:

- real SSIDs from testing
- Wi-Fi passwords or PSKs
- NetworkManager connection UUIDs copied from a live system
- MAC addresses/BSSIDs from a private environment
- session tokens, API keys, or credentials
- unreviewed Kodi or NetworkManager logs

Use generic examples such as `HomeWiFi`, `Guest`, `wlp2s0`, and placeholder UUIDs in documentation and tests.

Runtime diagnostics should not log passwords or other secrets. SSIDs and profile identifiers may still be sensitive in user logs, so diagnostic output should be kept minimal and sanitized where practical.

## Testing expectations

Before proposing a behavioural change, test the narrowest relevant path and avoid modifying the system network configuration during automated checks.

At minimum verify:

- Python syntax
- `addon.xml` validity
- NetworkManager command construction
- parsing of spaces, Unicode, escaped colons, and backslashes
- no `shell=True`
- no `sudo`
- no profile modify/delete calls
- no netplan changes
- no password logging

Real disconnect/reconnect testing should be performed manually on a test machine because it can interrupt connectivity.

## Releases

Development builds should not overwrite preserved baseline ZIPs. Keep versioned ZIPs reproducible and record notable changes in `CHANGELOG.md`.
