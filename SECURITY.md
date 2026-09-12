# Security and privacy

The add-on uses NetworkManager for connection handling. It should not own or rewrite saved network configuration.

## Secrets

Never log or commit:

- Wi-Fi passwords or PSKs
- tokens or credentials
- private certificates
- raw connection profiles

New Wi-Fi passwords come from Kodi's masked input dialog and are passed directly to `nmcli` without a shell. They are not written to disk or logged by the add-on. The password can still exist briefly in the `nmcli` process arguments while the command runs.

## Saved profiles

Existing NetworkManager profiles are activated as-is. The add-on must not rewrite credentials, key management, 802.1X settings, certificates, autoconnect, IP settings, DNS, routes, or permissions.

## Privileges

The add-on uses the current user's NetworkManager permissions. It should not require `sudo`, setuid helpers, privileged daemons, or direct writes to NetworkManager/netplan configuration files.

## Logs

Diagnostic logs may contain SSIDs, interface names, profile UUIDs, return codes, and NetworkManager errors. Review logs before posting them publicly.

Passwords, PSKs, tokens and other secrets must never be logged.
