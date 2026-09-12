# Installation

## Requirements

- Kodi 21 or newer
- Linux
- NetworkManager with `nmcli` available in `PATH`
- A Wi-Fi device managed by NetworkManager
- Permission for the Kodi user to scan and manage NetworkManager connections without `sudo`

The add-on is intended to be a thin Kodi front end to the system's existing NetworkManager configuration. It does not replace NetworkManager, netplan, desktop networking, or autoconnect policy.

## Install from ZIP

1. Download the desired `plugin.program.wifi-<version>.zip` build.
2. In Kodi, open **Add-ons**.
3. Choose **Install from zip file**.
4. Select the ZIP.
5. Open **Program add-ons → Wi-Fi**.

## Expected behaviour

The network list is generated from the current NetworkManager scan results. Networks no longer visible to NetworkManager should disappear from Kodi, and newly discovered networks should appear after refresh.

- Active network: offers **Disconnect** / **Cancel**.
- Saved network: activates the existing NetworkManager profile without modifying it.
- New open network: connects without a Wi-Fi password.
- New WPA/WPA2/WPA3 personal network: prompts with Kodi's on-screen keyboard.
- Unsaved enterprise/802.1X network: intentionally requires configuration outside the add-on.

## Scope

The add-on deliberately does not provide:

- static IP configuration
- DNS or route editing
- VPN management
- hotspot creation
- NetworkManager profile editing
- netplan editing
- custom autoconnect logic
- captive-portal authentication

## Troubleshooting

Useful read-only checks:

```bash
nmcli general status
nmcli device status
nmcli device wifi list
```

Kodi logs are normally under the Kodi profile directory, for example `~/.kodi/temp/kodi.log`.

Do not post logs publicly without reviewing them first. Runtime logs can contain SSIDs, interface names, profile names, and other local network identifiers even though the repository itself does not contain those values.
