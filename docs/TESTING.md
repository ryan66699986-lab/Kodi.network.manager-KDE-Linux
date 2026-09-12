# Testing

The add-on should be tested as a front end to an already-working NetworkManager installation. Testing must not casually rewrite or delete working network profiles.

## Baseline system

Development began on:

- Kodi 21.3 Omega
- Linux / KDE Plasma
- NetworkManager 1.54.3
- Orange Pi 5 Pro / RK3588S
- Wi-Fi device `wlan0`

This is the initial validation platform, not an intended platform restriction.

## Read-only checks

Before interactive testing:

```bash
nmcli --version
nmcli device status
nmcli connection show
nmcli connection show --active
nmcli -t -e yes -f IN-USE,SSID,SIGNAL,SECURITY device wifi list --rescan yes
```

The Kodi list should represent the same currently visible non-hidden SSIDs after deduplication.

## Required functional tests

### Live discovery

- Open the add-on.
- Confirm networks currently visible to NetworkManager appear in Kodi.
- Confirm duplicate BSSIDs for the same SSID are collapsed sensibly.
- Use Refresh and confirm the list is rebuilt from a fresh NetworkManager scan.
- Confirm networks that disappear from NetworkManager also disappear from Kodi.
- Confirm a newly visible network appears without any saved-profile prerequisite.

### Active network

- The current SSID must be marked connected.
- Selecting it should offer only `Disconnect` and `Cancel`.
- Disconnect must deactivate the connection without deleting the profile or disabling Wi-Fi.

### Saved personal network

- Select a visible SSID with an existing saved NetworkManager profile.
- The add-on should activate that profile by UUID without asking for the password again.
- It must not modify the saved profile.

### New personal network

Test on a network not previously saved on the machine:

- open network: no Wi-Fi password prompt;
- WPA/WPA2/WPA3 personal: masked Kodi password prompt;
- success must be verified from NetworkManager state rather than only the `nmcli` process return code.

### Enterprise network

- Unsaved 802.1X/EAP networks must not be partially configured by this add-on.
- A useful advanced-configuration message should be shown.
- An already-saved enterprise profile may be activated unchanged.

### Controller-only operation

Verify with the intended controller:

- open Program add-on;
- navigate network list;
- refresh;
- select network;
- enter password using Kodi's on-screen keyboard;
- dismiss dialogs;
- disconnect;
- return to Kodi without keyboard/mouse.

## Regression cases

These inputs should not break parsing:

- SSID containing spaces;
- SSID containing `:`;
- SSID containing `\\`;
- Unicode SSID;
- security string `--` or blank for open networks;
- `WPA2 WPA3`;
- `WPA2 802.1X`;
- signal value `0`;
- multiple BSSIDs with one connected and another stronger.

## Safety invariants

Every release should verify there is no code that performs:

```text
nmcli connection modify
nmcli connection delete
sudo
shell=True
```

and no direct writes to:

```text
/etc/netplan/
/etc/NetworkManager/system-connections/
```

The add-on must not implement its own autoconnect policy.

## Logging

Useful diagnostics may include:

- selected SSID;
- interface;
- saved/new connection path;
- profile UUID where relevant;
- sanitized NetworkManager return code/error;
- resulting active SSID.

Passwords, PSKs, and other secrets must never be logged.
