# Compatibility

The add-on is distro-neutral. It talks to NetworkManager through `nmcli` and uses Kodi's Python add-on API.

Expected environment:

- Kodi 21 or newer
- Linux
- NetworkManager managing the Wi-Fi device
- `nmcli` available in `PATH`
- normal user permission to scan and activate NetworkManager connections

The original test system is KDE Plasma on an Orange Pi 5 Pro. There is no board-specific, ARM-specific or KDE-specific networking code.

Normal desktop installs using NetworkManager, including KDE-based distributions such as CachyOS, should work without add-on-specific system changes.

Out of scope:

- hidden SSIDs
- creating new enterprise/802.1X profiles
- captive-portal browser login
- static IP, DNS, route, VPN and hotspot configuration
