# Changelog

All notable project changes should be recorded here.

## Unreleased

Development is continuing from the preserved v1.0.8 baseline. The current hardening work focuses on correctness around active-network detection, Wi-Fi interface discovery, NetworkManager escaping, duplicate BSSID handling, open-network normalization, safe disconnect semantics, scan error reporting, and Kodi list refresh behaviour.

## 1.0.8

Baseline development snapshot preserved in this repository.

Key behaviour at this point:

- controller-friendly Kodi Wi-Fi list
- live NetworkManager-backed scanning
- NetworkManager saved-profile activation
- new open and personal secured network connection paths
- active network disconnect action
- enterprise-network guardrails
- post-connect stability verification
- no direct profile modification, deletion, netplan editing, or custom autoconnect implementation

Known issues in 1.0.8 are documented in the repository README and development notes. This version is retained as a reproducible baseline rather than presented as a finished community release.
