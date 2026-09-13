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

## Upstream interfaces used

Current NetworkManager documentation still defines the commands this add-on depends on:

- `nmcli device status`
- `nmcli device wifi list --rescan yes ifname <ifname>`
- `nmcli device wifi connect <SSID> [password <password>] ifname <ifname>`
- `nmcli connection show`
- `nmcli connection show --active`
- `nmcli connection up uuid <UUID> ifname <ifname>`
- `nmcli connection down uuid <UUID>`

The add-on requests explicit fields in terse mode instead of parsing the normal human-readable table. This reduces exposure to formatting changes between NetworkManager versions.

Kodi-side usage is also conventional: a Python 3 program plugin declared with `xbmc.python.pluginsource`, `<provides>executable</provides>`, directory items, and `endOfDirectory()`.

## Update risk

Routine distro updates should be low risk because the add-on does not depend on KDE internals, netplan file formats, interface names, private NetworkManager libraries, or privileged helper services.

The likely compatibility breakpoints are major upstream changes to:

- NetworkManager `nmcli` command or field semantics
- NetworkManager authorization policy for unprivileged users
- Kodi's Python add-on ABI or plugin APIs

The explicit UTF-8 decoding is intentional. It avoids inheriting an ASCII or non-UTF-8 process locale from Kodi while preserving SSIDs from any language that NetworkManager reports as valid UTF-8.

Out of scope:

- hidden SSIDs
- creating new enterprise/802.1X profiles
- captive-portal browser login
- static IP, DNS, route, VPN and hotspot configuration
