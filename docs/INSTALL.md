# Installation

## Requirements

- Kodi 21+
- Linux
- NetworkManager with `nmcli` in `PATH`
- a Wi-Fi device managed by NetworkManager
- permission for the Kodi user to scan and activate connections without `sudo`

On a normal KDE Plasma desktop using NetworkManager, these requirements are usually already met.

## Install from ZIP

1. Download `releases/plugin.program.wifi-1.0.9.zip`.
2. In Kodi, open **Add-ons**.
3. Choose **Install from zip file**.
4. Select the ZIP.
5. Open **Program add-ons → Wi-Fi**.

No system files are installed and no service is added.

## What it does

The list comes from the current NetworkManager scan.

- active network: shown with a check mark and offers `Disconnect` / `Cancel`
- saved network: activates the existing profile
- new open network: connects without a Wi-Fi password
- new WPA/WPA2/WPA3 personal network: asks for a password using Kodi's on-screen keyboard
- new 802.1X/EAP network: setup is left to the system network manager

It does not edit static IPs, DNS, routes, VPNs, hotspots, netplan, saved profile settings, or autoconnect policy.

## Troubleshooting

Useful checks:

```bash
nmcli general status
nmcli device status
nmcli device wifi list
```

Kodi logs are usually in `~/.kodi/temp/kodi.log`.

Review logs before posting them publicly; they can contain SSIDs, interface names and connection identifiers.
