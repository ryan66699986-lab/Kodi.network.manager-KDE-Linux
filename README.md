# Kodi Network Manager for Linux

A Kodi Program add-on for managing Wi-Fi through NetworkManager (`nmcli`) without leaving Kodi.

Kodi handles the UI. NetworkManager keeps control of devices, saved connections, credentials and autoconnect.

## Status

Current development version: **1.0.9**.

The original v1.0.8 ZIP is kept in `baseline/`, and branch `baseline/v1.0.8` preserves that snapshot.

The v1.0.9 install ZIP is in `releases/`.

## Features

- controller-friendly Wi-Fi list inside Kodi
- live NetworkManager scans
- connects to new open and WPA/WPA2/WPA3 personal networks
- reuses saved NetworkManager profiles
- disconnects the active Wi-Fi connection
- supports saved enterprise profiles without editing them
- leaves new 802.1X/EAP setup to the system network manager
- verifies the selected SSID before reporting a successful connection
- selects the Wi-Fi interface from NetworkManager instead of assuming `wlan0`

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

## Checksums

v1.0.9:

- `plugin.program.wifi/default.py`: `45e69cb1b9ec0f27fd538d6baa1d232c85e76c138791b616c8500781e73b2ef0`
- `plugin.program.wifi/addon.xml`: `7e05b58ce2c7f4f7821afb29b45832305317c1be51d7a4c5a293749a85fd9d1b`
- `releases/plugin.program.wifi-1.0.9.zip`: `d6807de81ffc3d5de545162710ad07472d4587a724676a5c17604ddae385a285`

v1.0.8 baseline:

- `plugin.program.wifi/default.py`: `fe4fdcdfb8b06a7946f0944493697fb6f3eb80b114d781ff78703b5931539750`
- `baseline/plugin.program.wifi-1.0.8.zip`: `2405e18b82206959305d9de7e1cb688a30d2789f986e037b3e09bde217400a2e`

## Privacy

Do not commit real Wi-Fi passwords, private SSIDs, NetworkManager UUIDs, MAC/BSSID values, tokens, or raw logs from a live system.

## License

TBD.
