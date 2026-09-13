# Release checklist

Keep releases simple and make sure the ZIP matches the tracked source.

Before packaging:

- addon version is correct
- addon XML parses
- Python source compiles
- connected network marker works
- scan and refresh work
- saved-network activation works
- new open-network flow works
- new WPA/WPA2/WPA3 personal flow works
- disconnect leaves the saved profile intact
- NetworkManager autoconnect still works after reboot
- no passwords, private SSIDs, UUIDs, MAC/BSSID values or raw logs are committed

The release code must not modify or delete NetworkManager profiles, change autoconnect policy, edit netplan, use privileged helper services, or invoke commands through a shell.

Package layout:

```text
plugin.program.wifi/
├── addon.xml
├── default.py
└── LICENSE.txt
```

Build a release ZIP directly from the matching release branch:

```bash
git archive --format=zip --prefix=plugin.program.wifi/ release/v1.0.9:plugin.program.wifi -o plugin.program.wifi-1.0.9.zip
```

Do not keep a ZIP in the repository if it no longer matches the release branch.
