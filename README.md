# Kodi Network Manager for Linux

Kodi Program add-on providing a controller-friendly front end to NetworkManager (`nmcli`) for Wi-Fi discovery, connection, disconnection, and refresh.

The project is intentionally narrow: Kodi presents the UI, while NetworkManager remains the source of truth for devices, saved profiles, credentials, and normal autoconnect behaviour.

## Status

The repository is currently based on the preserved `plugin.program.wifi` **v1.0.8** development baseline. v1.0.8 is not presented as a finished community release; hardening work is continuing on newer versions.

The exact v1.0.8 ZIP is archived under `baseline/`, and branch `baseline/v1.0.8` preserves that baseline independently from ongoing work on `main`.

## Features

- controller-friendly Wi-Fi management from inside Kodi
- live NetworkManager-backed Wi-Fi scans
- current nearby SSIDs only; no separate persistent network database
- activation of existing saved NetworkManager profiles
- connection to new open and WPA/WPA2/WPA3 personal networks
- Disconnect / Cancel handling for the active network
- support for saved enterprise profiles without rewriting them
- refusal to invent configuration for new 802.1X/EAP networks
- post-connect verification before reporting success
- no `sudo`, custom daemon, profile deletion, netplan editing, or custom autoconnect implementation

## Requirements

- Kodi 21 or newer
- Linux
- NetworkManager with `nmcli`
- Wi-Fi managed by NetworkManager
- user-level permission to scan and activate Wi-Fi connections

See [docs/INSTALL.md](docs/INSTALL.md) for installation and operating scope.

## Development documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Testing](docs/TESTING.md)
- [Installation](docs/INSTALL.md)
- [Security and privacy](SECURITY.md)
- [Contributing](CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)

## Baseline checksums

- `plugin.program.wifi/default.py`: `fe4fdcdfb8b06a7946f0944493697fb6f3eb80b114d781ff78703b5931539750`
- `baseline/plugin.program.wifi-1.0.8.zip`: `2405e18b82206959305d9de7e1cb688a30d2789f986e037b3e09bde217400a2e`

## Privacy

The repository must not contain real test-environment SSIDs, Wi-Fi passwords, NetworkManager connection UUIDs, MAC/BSSID values, access tokens, or unreviewed runtime logs. Runtime Kodi/NetworkManager logs may themselves contain local network identifiers and should be reviewed before being posted publicly.

## License

No project license has been selected yet. A license should be chosen before presenting the project as a general public release for redistribution/contribution.
