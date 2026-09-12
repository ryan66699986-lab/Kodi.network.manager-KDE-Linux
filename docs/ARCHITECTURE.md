# Architecture

This add-on is intentionally a thin Kodi front end to the Linux system's existing NetworkManager state.

## Design rule

Kodi does not own networking. NetworkManager does.

The add-on should only:

- ask NetworkManager which Wi-Fi networks are currently visible;
- display those networks inside Kodi;
- activate an existing saved NetworkManager profile when one already matches the selected SSID;
- connect to a new open or WPA/WPA2/WPA3 personal network through `nmcli`;
- disconnect the currently active Wi-Fi connection;
- refresh the visible list.

The add-on must not become a second network manager.

## Data flow

```text
NetworkManager live scan
        |
        v
Kodi Program add-on
        |
        +-- active SSID -> Disconnect / Cancel
        |
        +-- visible + saved profile -> activate saved UUID unchanged
        |
        +-- visible + unsaved personal network -> connect with nmcli
        |
        +-- visible + unsaved enterprise network -> refuse advanced setup
```

## Source of truth

The current NetworkManager scan is the only source of truth for network visibility. The add-on should not persist its own list of nearby SSIDs.

If NetworkManager no longer sees a network, Kodi should not show it. If NetworkManager sees a new network, Kodi should show it on the next scan/refresh.

Saved profiles are consulted only after the user selects a currently visible SSID.

## Existing profile policy

Existing saved profiles are treated as NetworkManager-owned configuration.

The add-on may activate them by UUID but must not rewrite:

- SSID;
- secrets;
- key-management;
- 802.1X settings;
- certificates;
- autoconnect;
- autoconnect priority;
- IP configuration;
- DNS;
- routes;
- profile permissions.

## New connections

For a new open network, NetworkManager is asked to connect without a password.

For a new WPA/WPA2/WPA3 personal network, Kodi obtains the password through its masked input dialog and passes it to `nmcli` as an argument list without `shell=True`.

Unsaved enterprise/802.1X/EAP configuration is deliberately out of scope. Existing enterprise profiles may be activated unchanged.

## Interface selection

The long-term behavior should be NetworkManager-driven rather than hard-coded to `wlan0`:

1. prefer a currently connected Wi-Fi device;
2. otherwise use an available managed Wi-Fi device;
3. ignore Wi-Fi P2P devices;
4. if no Wi-Fi device exists, report that clearly rather than inventing an interface name.

## Kodi integration

The add-on is a Python Program add-on and uses Kodi UI primitives for:

- network listing;
- password input;
- disconnect/cancel selection;
- result/error dialogs;
- list refresh.

No terminal window, desktop network editor, daemon, or helper service is required.

## Environment isolation

The original development system launches Kodi with a private multimedia environment. `nmcli` subprocesses therefore strip `LD_LIBRARY_PATH` and `LD_PRELOAD` so NetworkManager tooling does not inherit Kodi-specific multimedia libraries.

This behavior is defensive and should remain harmless on normal Kodi installations where those variables are unset.
