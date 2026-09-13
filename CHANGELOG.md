# Changelog

## 1.0.9

- fixed active SSID detection (`IN-USE` / `*`)
- made saved-profile SSID lookup safe for escaped NetworkManager values
- normalised blank and `--` security fields to `Open`
- fixed duplicate-BSSID handling so the connected AP always wins
- accepted `SIGNAL=0`
- removed the `nmcli device disconnect` fallback
- separated scan failures from empty scan results
- skipped malformed `nmcli` rows instead of crashing the add-on
- verified saved-profile activation by both SSID and UUID
- switched connect/disconnect/refresh UI updates to `Container.Refresh`
- removed the `wlan0` fallback; Wi-Fi interfaces are selected from NetworkManager
- highlighted the connected network with a bold row and green ASCII marker
- made `nmcli` output decoding independent of Kodi/system locale
- added GPL-2.0-or-later metadata and license files
- confirmed scan, password entry and connection on a separate real-world Wi-Fi network through Kodi

Install ZIP: `releases/plugin.program.wifi-1.0.9.zip`

## 1.0.8

Baseline snapshot.

Included at this point:

- Kodi Wi-Fi list
- live NetworkManager scans
- saved-profile activation
- new open and WPA/WPA2/WPA3 personal network connection
- disconnect action
- enterprise-network guardrails
- post-connect verification

The exact v1.0.8 ZIP is kept in `baseline/` and on branch `baseline/v1.0.8`.
