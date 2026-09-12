# Kodi Network Manager for Linux

Kodi Program add-on providing a controller-friendly front end to NetworkManager (`nmcli`) for Wi-Fi discovery, connection, disconnection, and refresh.

## Baseline

The repository is initially populated from the tested `plugin.program.wifi` **v1.0.8** ZIP supplied from the Orange Pi 5 Pro project.

Baseline source is kept under `plugin.program.wifi/`, and the exact v1.0.8 ZIP is archived under `baseline/`.

### Current baseline status

v1.0.8 is a development baseline, not a finished community release. Known hardening items remain, including active-SSID detection, fully safe handling of escaped NetworkManager values, open-network normalization, duplicate-BSSID handling, safe disconnect behavior, and removal of the `wlan0` fallback in favour of NetworkManager-driven interface discovery.

The design goal is deliberately narrow: remain a thin Kodi UI over the system's existing NetworkManager configuration. It must not replace or reconfigure netplan, autoconnect policy, saved profiles, or desktop networking.

## Baseline checksums

- `plugin.program.wifi/default.py`: `fe4fdcdfb8b06a7946f0944493697fb6f3eb80b114d781ff78703b5931539750`
- `plugin.program.wifi-1.0.8.zip`: `2405e18b82206959305d9de7e1cb688a30d2789f986e037b3e09bde217400a2e`
