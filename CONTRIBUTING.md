# Contributing

Keep the add-on small. It should use NetworkManager, not replace it.

## Rules

- Reuse existing NetworkManager profiles instead of rewriting them.
- Do not edit netplan, wpa_supplicant, DNS, routes, or autoconnect settings.
- Do not add `sudo`, daemons, dispatcher scripts, or helper services.
- Do not delete NetworkManager profiles.
- Use documented `nmcli` and Kodi APIs.
- Keep the UI usable with a controller.

## Privacy

Do not commit:

- real test SSIDs
- Wi-Fi passwords or PSKs
- live NetworkManager UUIDs
- private MAC/BSSID values
- tokens or credentials
- raw Kodi or NetworkManager logs

Use generic examples in docs and tests.

## Testing

Before sending a change, check the part you touched. At minimum:

- Python syntax
- `addon.xml`
- `nmcli` command construction
- SSIDs with spaces, Unicode, `:` and `\\`
- no `shell=True`
- no `sudo`
- no profile modify/delete calls
- no netplan writes
- no password logging

Disconnect/reconnect tests should be done manually on a test machine because they can interrupt the active connection.

## Builds

Keep old baseline ZIPs intact. Use a new version number for each build and update `CHANGELOG.md` when behavior changes.
