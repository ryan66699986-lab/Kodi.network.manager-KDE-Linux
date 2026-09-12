# Kodi Network Manager for Linux

A Kodi Program add-on for managing Wi-Fi through NetworkManager (`nmcli`) without leaving Kodi.

Kodi handles the UI. NetworkManager keeps control of devices, saved connections, credentials and autoconnect.

## Status

Development currently starts from `plugin.program.wifi` v1.0.8. The exact v1.0.8 ZIP is kept in `baseline/`, and `baseline/v1.0.8` preserves the same snapshot while work continues on `main`.

## Features

- controller-friendly Wi-Fi list inside Kodi
- live NetworkManager scans
- connects to new open and WPA/WPA2/WPA3 personal networks
- reuses saved NetworkManager profiles
- disconnects the active Wi-Fi connection
- supports saved enterprise profiles without editing them
- leaves new 802.1X/EAP setup to the system network manager
- verifies the selected SSID before reporting a successful connection

It does not edit netplan, rewrite saved profiles, delete connections, replace autoconnect, or require `sudo`.

## Requirements

- Kodi 21+
- Linux
- NetworkManager and `nmcli`
- Wi-Fi managed by NetworkManager
- permission for the Kodi user to scan and activate connections

## Docs

- [Installation](docs/INSTALL.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Testing](docs/TESTING.md)
- [v1.0.8 provenance](docs/PROVENANCE.md)
- [Security](SECURITY.md)
- [Contributing](CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)

## Baseline checksums

- `plugin.program.wifi/default.py`: `fe4fdcdfb8b06a7946f0944493697fb6f3eb80b114d781ff78703b5931539750`
- `baseline/plugin.program.wifi-1.0.8.zip`: `2405e18b82206959305d9de7e1cb688a30d2789f986e037b3e09bde217400a2e`

## Privacy

Do not commit real Wi-Fi passwords, private SSIDs, NetworkManager UUIDs, MAC/BSSID values, tokens, or raw logs from a live system.

## License

TBD.
