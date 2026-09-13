# Builds

Release ZIPs must be built from the matching release branch so the package cannot drift from tracked source.

For v1.0.9:

```bash
git archive --format=zip --prefix=plugin.program.wifi/ release/v1.0.9:plugin.program.wifi -o plugin.program.wifi-1.0.9.zip
```
