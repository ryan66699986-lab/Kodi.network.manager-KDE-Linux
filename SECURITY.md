# Security and privacy

This project is intended to be a thin UI over NetworkManager. Network credentials and connection policy should remain owned by NetworkManager, not by the Kodi add-on.

## Secrets

The add-on must never:

- log Wi-Fi passwords or PSKs;
- write credentials into repository files;
- create plaintext temporary password files;
- hard-code user credentials;
- expose secrets through Kodi status/error messages.

For a new secured network, Kodi obtains the password through a masked input dialog. The current implementation passes that value to `nmcli` as an argv element rather than through a shell command. This avoids shell interpolation, but the secret may still exist transiently in the process command line while `nmcli` runs. Eliminating that exposure would require a more complex NetworkManager secret-agent or D-Bus design and is not currently implemented.

## Existing profiles

The add-on should activate existing NetworkManager profiles unchanged. It must not rewrite saved credentials, key-management, 802.1X configuration, certificates, autoconnect policy, IP settings, DNS, routes, or permissions.

## Privilege model

The add-on should operate using the logged-in user's existing NetworkManager permissions.

It must not depend on:

- `sudo`;
- setuid helpers;
- privileged background daemons;
- direct writes to NetworkManager or netplan configuration files.

## Logs

Logs may include SSID, interface, UUID, action, return code, and sanitized error text when needed for diagnostics.

Never include passwords, PSKs, secrets, session tokens, or unrelated personal data in logs, issues, screenshots, test fixtures, or commits.

## Reporting security problems

Do not post credentials or private connection profiles in a public issue. When reporting a bug, redact passwords, PSKs, tokens, private certificates, MAC addresses if sensitive, and any personally identifying network names if desired.
