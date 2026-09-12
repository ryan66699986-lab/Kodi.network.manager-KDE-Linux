# Architecture

The add-on is a Kodi UI for NetworkManager.

It should only:

- show Wi-Fi networks currently visible to NetworkManager
- activate an existing saved profile for a selected SSID
- connect to a new open or WPA/WPA2/WPA3 personal network
- disconnect the active Wi-Fi connection
- refresh the list

It should not maintain its own network database or edit system networking.

## Flow

```text
NetworkManager scan
        |
        v
Kodi add-on
        |
        +-- active SSID -> Disconnect / Cancel
        +-- visible + saved profile -> activate saved UUID
        +-- visible + new personal network -> connect with nmcli
        +-- visible + new enterprise network -> leave setup to the system
```

## Saved profiles

Saved profiles belong to NetworkManager. The add-on may activate them by UUID, but should not rewrite their SSID, secrets, key management, certificates, autoconnect, IP settings, DNS, routes, or permissions.

## New connections

Open networks connect without a password.

WPA/WPA2/WPA3 personal networks use Kodi's masked password dialog, then call `nmcli` with an argument list. No `shell=True`.

New 802.1X/EAP setup is out of scope. Already-saved enterprise profiles can be activated unchanged.

## Wi-Fi device selection

Do not assume the interface is called `wlan0`.

Preferred behavior:

1. use the currently connected Wi-Fi device if there is one
2. otherwise use a managed Wi-Fi device
3. ignore Wi-Fi P2P devices
4. if none exist, show an error

## Kodi UI

Kodi handles the network list, password entry, dialogs and refresh. No terminal or desktop network editor is required.

## Environment

`nmcli` subprocesses strip `LD_LIBRARY_PATH` and `LD_PRELOAD` so they do not inherit Kodi-specific multimedia libraries. On normal Kodi installs these variables are usually unset, so this has no effect.
