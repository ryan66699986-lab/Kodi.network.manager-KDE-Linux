# Testing

Test against a working NetworkManager setup. Do not use automated tests that rewrite or delete the machine's network configuration.

## Original test platform

- Kodi 21.3 Omega
- Linux / KDE Plasma
- NetworkManager 1.54.3
- Orange Pi 5 Pro / RK3588S
- Wi-Fi interface `wlan0`

This is only the original test machine, not a platform requirement.

The 1.0.9 connection flow has also been exercised on a separate real-world Wi-Fi network: scan, password entry, connection and post-connect verification all completed through Kodi.

## Read-only checks

```bash
nmcli --version
nmcli device status
nmcli connection show
nmcli connection show --active
nmcli -t -e yes -f IN-USE,SSID,SIGNAL,SECURITY device wifi list --rescan yes
```

Kodi should show the same visible, non-hidden SSIDs after deduplication.

## Functional checks

### Scan and refresh

- visible networks appear in Kodi
- duplicate BSSIDs for one SSID collapse correctly
- Refresh gets a fresh NetworkManager scan
- networks that disappear from NetworkManager disappear from Kodi
- newly visible networks appear without already having a saved profile

### Active network

- current SSID is marked connected
- selecting it offers only `Disconnect` and `Cancel`
- disconnect does not delete the profile or disable Wi-Fi

### Saved network

- selecting a visible saved network activates its existing profile by UUID
- no password prompt if NetworkManager already has the credentials
- the profile is not modified

### New network

- open network: no password prompt
- WPA/WPA2/WPA3 personal: masked Kodi password prompt
- success is checked against NetworkManager state, not just the `nmcli` return code

### Enterprise

- a saved 802.1X/EAP profile may be activated
- a new enterprise network is not partially configured by the add-on

### Controller

Verify the whole flow with a controller: open the add-on, refresh, select a network, use the on-screen keyboard, dismiss dialogs, disconnect and return to Kodi.

## Parser cases

Test:

- spaces in SSID
- `:` in SSID
- `\\` in SSID
- Unicode SSID
- blank or `--` security for open networks
- `WPA2 WPA3`
- `WPA2 802.1X`
- signal `0`
- duplicate BSSIDs where the connected AP is weaker than another AP with the same SSID

## Safety checks

Release code should not contain:

```text
nmcli connection modify
nmcli connection delete
sudo
shell=True
```

and should not write to:

```text
/etc/netplan/
/etc/NetworkManager/system-connections/
```

Passwords and PSKs must never be logged.
