# Kodi Network Manager for Linux

A Kodi Program add-on for managing Wi-Fi through NetworkManager (`nmcli`) without leaving Kodi.

Kodi handles the UI. NetworkManager keeps control of devices, saved connections, credentials and autoconnect.

## Status

Current release: **1.0.9**.

- [download v1.0.9](releases/plugin.program.wifi-1.0.9.zip)
- source: `plugin.program.wifi/`
- original v1.0.8 baseline: `baseline/` and branch `baseline/v1.0.8`

The 1.0.9 flow has been tested on the original development system and on a separate real-world Wi-Fi network through Kodi.

## Features

- controller-friendly Wi-Fi list inside Kodi
- live NetworkManager scans
- connected network shown in bold with a green `v` marker
- connects to new open and WPA/WPA2/WPA3 personal networks
- reuses saved NetworkManager profiles
- disconnects the active Wi-Fi connection
- supports saved enterprise profiles without editing them
- leaves new 802.1X/EAP setup to the system network manager
- verifies the selected SSID before reporting success
- selects the Wi-Fi interface from NetworkManager instead of assuming `wlan0`
- decodes `nmcli` output explicitly as UTF-8 instead of relying on Kodi's inherited locale

It does not edit netplan, rewrite saved profiles, delete connections, replace autoconnect, or require `sudo`.

## Compatibility

Expected to work on normal Linux desktop installs where:

- Kodi 21+ uses Python 3 add-ons
- NetworkManager manages Wi-Fi
- `nmcli` is installed and in `PATH`
- the Kodi user is allowed to scan and activate connections

Development and testing has been on KDE Plasma. The add-on has no Orange Pi, ARM or KDE-specific networking code.

Not handled by this add-on:

- hidden SSIDs
- creating new 802.1X/EAP profiles
- captive-portal web login
- static IP, DNS, route, VPN or hotspot configuration

## Install

Download `releases/plugin.program.wifi-1.0.9.zip`, then in Kodi use **Add-ons → Install from zip file**.

See [Installation](docs/INSTALL.md) for details.

## Docs

- [Installation](docs/INSTALL.md)
- [Compatibility](docs/COMPATIBILITY.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Testing](docs/TESTING.md)
- [Release checklist](docs/RELEASE.md)
- [v1.0.8 provenance](docs/PROVENANCE.md)
- [Security](SECURITY.md)
- [Contributing](CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)

## Privacy

Do not commit real Wi-Fi passwords, private SSIDs, NetworkManager UUIDs, MAC/BSSID values, tokens, or raw logs from a live system.

## License

GPL-2.0-or-later. See [LICENSE](LICENSE).
