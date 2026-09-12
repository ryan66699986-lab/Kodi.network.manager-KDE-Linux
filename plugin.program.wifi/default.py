#!/usr/bin/env python3
"""Wi-Fi manager for Kodi using NetworkManager/nmcli."""
import os
import subprocess
import sys
import time
import urllib.parse

import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin

ADDON = xbmcaddon.Addon()
ADDON_HANDLE = int(sys.argv[1])
_NM_ENV = None


def _nm_env():
    global _NM_ENV
    if _NM_ENV is None:
        _NM_ENV = os.environ.copy()
        _NM_ENV.pop("LD_LIBRARY_PATH", None)
        _NM_ENV.pop("LD_PRELOAD", None)
    return _NM_ENV


def _run(cmd, timeout=15):
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            env=_nm_env(),
            timeout=timeout,
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return -1, "", "Timed out"
    except Exception as exc:
        return -1, "", str(exc)


def _parse_escaped_colons(line, expected):
    """Parse nmcli terse output produced with '-e yes'."""
    fields = []
    current = []
    escaped = False

    for ch in line:
        if escaped:
            current.append(ch)
            escaped = False
        elif ch == "\\":
            escaped = True
        elif ch == ":" and len(fields) < expected - 1:
            fields.append("".join(current))
            current = []
        else:
            current.append(ch)

    if escaped:
        current.append("\\")
    fields.append("".join(current))
    return fields


def _parse_row(line, expected, context):
    fields = _parse_escaped_colons(line, expected)
    if len(fields) != expected:
        xbmc.log(
            "plugin.program.wifi: skipped malformed {} row".format(context),
            xbmc.LOGWARNING,
        )
        return None
    return fields


def _nmcli_lines(*args, timeout=15):
    cmd = ["nmcli"] + list(args)
    rc, out, err = _run(cmd, timeout=timeout)
    return rc, out.splitlines() if out else [], err


def _get_interface():
    """Prefer the connected Wi-Fi interface; otherwise use an available Wi-Fi interface."""
    rc, lines, err = _nmcli_lines(
        "-t", "-e", "yes", "-f", "DEVICE,TYPE,STATE", "device", "status"
    )
    if rc != 0:
        xbmc.log(
            "plugin.program.wifi: device discovery failed rc={} err={}".format(rc, err[:200]),
            xbmc.LOGERROR,
        )
        return None

    candidates = []
    for line in lines:
        row = _parse_row(line, 3, "device")
        if not row:
            continue
        device, dev_type, state = row
        if dev_type != "wifi" or "p2p" in device.lower():
            continue
        if state == "connected":
            return device
        if state not in ("unavailable", "unmanaged"):
            candidates.append(device)

    return candidates[0] if candidates else None


def _get_active_ssid(ifname):
    rc, lines, _ = _nmcli_lines(
        "-t", "-e", "yes", "-f", "IN-USE,SSID",
        "device", "wifi", "list", "ifname", ifname,
    )
    if rc != 0:
        return None
    for line in lines:
        row = _parse_row(line, 2, "active-ssid")
        if not row:
            continue
        in_use, ssid = row
        if in_use == "*" and ssid:
            return ssid
    return None


def _get_active_uuid(ifname):
    rc, lines, _ = _nmcli_lines(
        "-t", "-e", "yes", "-f", "NAME,UUID,DEVICE",
        "connection", "show", "--active",
    )
    if rc != 0:
        return None
    for line in lines:
        row = _parse_row(line, 3, "active-connection")
        if not row:
            continue
        _name, uuid, device = row
        if device == ifname and uuid:
            return uuid
    return None


def _profile_ssid(uuid):
    """Return the unescaped SSID value stored in a NetworkManager profile."""
    rc, out, _ = _run([
        "nmcli", "-e", "no", "-g", "802-11-wireless.ssid",
        "connection", "show", "uuid", uuid,
    ])
    if rc != 0 or not out:
        return None
    return out.splitlines()[0]


def _find_saved_uuid(ssid):
    rc, lines, _ = _nmcli_lines(
        "-t", "-e", "yes", "-f", "NAME,UUID,TYPE", "connection", "show"
    )
    if rc != 0:
        return None

    for line in lines:
        row = _parse_row(line, 3, "saved-profile")
        if not row:
            continue
        _name, uuid, conn_type = row
        if conn_type == "802-11-wireless" and _profile_ssid(uuid) == ssid:
            return uuid
    return None


def _verify_connection(ssid, ifname, expected_uuid=None, timeout=8):
    """Require the requested connection to remain active for three seconds."""
    stable_since = None
    deadline = time.monotonic() + timeout

    while True:
        now = time.monotonic()
        ssid_ok = _get_active_ssid(ifname) == ssid
        uuid_ok = expected_uuid is None or _get_active_uuid(ifname) == expected_uuid

        if ssid_ok and uuid_ok:
            if stable_since is None:
                stable_since = now
            elif now - stable_since >= 3.0:
                return True
        else:
            stable_since = None

        if now >= deadline:
            return False
        time.sleep(0.5)


def _normalize_security(value):
    value = (value or "").strip()
    return "Open" if value in ("", "--") else value


def _signal_bar(signal):
    if signal >= 80:
        return " ▂▄▆█"
    if signal >= 60:
        return " ▂▄▆_"
    if signal >= 40:
        return " ▂▄__"
    if signal >= 20:
        return " ▂___"
    return ""


def scan_networks(ifname):
    """Return (networks, error). error is None when the scan command succeeded."""
    rc, lines, err = _nmcli_lines(
        "-t", "-e", "yes",
        "-f", "IN-USE,SSID,SIGNAL,SECURITY",
        "device", "wifi", "list",
        "--rescan", "yes",
        "ifname", ifname,
        timeout=20,
    )
    if rc != 0:
        message = err or "NetworkManager scan failed"
        xbmc.log(
            "plugin.program.wifi: scan failed rc={} err={}".format(rc, message[:200]),
            xbmc.LOGERROR,
        )
        return [], message

    networks = {}
    for line in lines:
        row = _parse_row(line, 4, "scan")
        if not row:
            continue
        in_use, ssid, sig_str, security = row
        if not ssid or ssid == "--":
            continue

        try:
            signal = int(sig_str)
        except ValueError:
            xbmc.log("plugin.program.wifi: skipped scan row with invalid signal", xbmc.LOGWARNING)
            continue
        if not 0 <= signal <= 100:
            continue

        entry = {
            "ssid": ssid,
            "signal": signal,
            "security": _normalize_security(security),
            "connected": in_use == "*",
        }

        previous = networks.get(ssid)
        if previous is None:
            networks[ssid] = entry
        elif previous["connected"]:
            continue
        elif entry["connected"] or entry["signal"] > previous["signal"]:
            networks[ssid] = entry

    result = sorted(
        networks.values(),
        key=lambda item: (not item["connected"], -item["signal"], item["ssid"].casefold()),
    )
    return result, None


def show_networks(ifname):
    xbmcplugin.setContent(ADDON_HANDLE, "files")

    refresh_item = xbmcgui.ListItem(label="[B]Refresh networks[/B]")
    xbmcplugin.addDirectoryItem(
        ADDON_HANDLE,
        "{}?action=refresh".format(sys.argv[0]),
        refresh_item,
        isFolder=False,
    )

    networks, scan_error = scan_networks(ifname)
    if scan_error:
        item = xbmcgui.ListItem(label="Wi-Fi scan failed")
        xbmcplugin.addDirectoryItem(ADDON_HANDLE, "", item, isFolder=False)
        xbmcgui.Dialog().ok("Wi-Fi", "Wi-Fi scan failed: {}".format(_short_error(scan_error)))
    else:
        for network in networks:
            if network["connected"]:
                prefix = "[B][COLOR green]✓[/COLOR] "
                suffix = "[/B]"
            else:
                prefix = "  "
                suffix = ""

            label = "{}{}{} — {}% — {}{}".format(
                prefix,
                network["ssid"],
                _signal_bar(network["signal"]),
                network["signal"],
                network["security"],
                suffix,
            )
            item = xbmcgui.ListItem(label=label)
            item.setInfo("programs", {"title": network["ssid"]})
            url = "{}?action=select&ssid={}&security={}".format(
                sys.argv[0],
                urllib.parse.quote(network["ssid"], safe=""),
                urllib.parse.quote(network["security"], safe=""),
            )
            xbmcplugin.addDirectoryItem(ADDON_HANDLE, url, item, isFolder=False)

        if not networks:
            item = xbmcgui.ListItem(label="No networks found")
            xbmcplugin.addDirectoryItem(ADDON_HANDLE, "", item, isFolder=False)

    xbmcplugin.endOfDirectory(ADDON_HANDLE, True)


def _is_enterprise(security):
    upper = security.upper()
    return "802.1X" in upper or "EAP" in upper


def select_network(ssid, security, ifname):
    active_ssid = _get_active_ssid(ifname)
    if active_ssid == ssid:
        choice = xbmcgui.Dialog().select(ssid, ["Disconnect", "Cancel"])
        if choice == 0:
            _disconnect(ifname)
        return

    saved_uuid = _find_saved_uuid(ssid)
    if saved_uuid:
        _activate_saved(saved_uuid, ssid, ifname, security)
        return

    if _is_enterprise(security):
        xbmcgui.Dialog().ok(
            "Wi-Fi",
            "Advanced network configuration required — use the system network manager to configure [B]{}[/B].".format(ssid),
        )
        return

    _connect_new(ssid, security, ifname)


def _activate_saved(uuid, ssid, ifname, security=""):
    rc, out, err = _run([
        "nmcli", "--wait", "20", "connection", "up", "uuid", uuid, "ifname", ifname
    ], timeout=30)
    xbmc.log(
        "plugin.program.wifi: activate saved ssid='{}' rc={}".format(ssid, rc),
        xbmc.LOGINFO,
    )
    if rc != 0:
        message = out or err
        _connection_error(ssid, message, "activation")
        return

    if not _verify_connection(ssid, ifname, expected_uuid=uuid):
        xbmcgui.Dialog().ok("Connection failed", "Could not stay connected to [B]{}[/B].".format(ssid))
        xbmc.log(
            "plugin.program.wifi: saved connection verification failed ssid='{}'".format(ssid),
            xbmc.LOGERROR,
        )
        return

    _show_success(ssid, security)


def _connect_new(ssid, security, ifname):
    cmd = ["nmcli", "--wait", "20", "device", "wifi", "connect", ssid, "ifname", ifname]
    if security != "Open":
        password = xbmcgui.Dialog().input(
            "Enter Wi-Fi password for [B]{}[/B]".format(ssid),
            type=xbmcgui.INPUT_ALPHANUM,
            option=xbmcgui.ALPHANUM_HIDE_INPUT,
        )
        if not password:
            return
        cmd += ["password", password]

    rc, out, err = _run(cmd, timeout=30)
    password = None
    xbmc.log(
        "plugin.program.wifi: new connect ssid='{}' rc={}".format(ssid, rc),
        xbmc.LOGINFO,
    )
    if rc != 0:
        _connection_error(ssid, out or err, "new connection")
        return

    if not _verify_connection(ssid, ifname):
        xbmcgui.Dialog().ok("Connection failed", "Could not stay connected to [B]{}[/B].".format(ssid))
        xbmc.log(
            "plugin.program.wifi: new connection verification failed ssid='{}'".format(ssid),
            xbmc.LOGERROR,
        )
        return

    _show_success(ssid, security)


def _connection_error(ssid, message, action):
    xbmcgui.Dialog().ok(
        "Connection failed",
        "Could not connect to [B]{}[/B]:\n{}".format(ssid, _short_error(message)),
    )
    xbmc.log(
        "plugin.program.wifi: {} failed ssid='{}': {}".format(action, ssid, (message or "")[:200]),
        xbmc.LOGERROR,
    )


def _show_success(ssid, security=""):
    hint = "\n\nThis network may require a web sign-in." if security == "Open" else ""
    xbmcgui.Dialog().ok("Wi-Fi", "Connected to [B]{}[/B]{}".format(ssid, hint))
    xbmc.executebuiltin("Container.Refresh")


def _disconnect(ifname):
    uuid = _get_active_uuid(ifname)
    if not uuid:
        xbmcgui.Dialog().ok("Disconnect failed", "Could not identify the active Wi-Fi connection.")
        xbmc.log(
            "plugin.program.wifi: disconnect aborted; no active UUID for {}".format(ifname),
            xbmc.LOGERROR,
        )
        return

    rc, out, err = _run(["nmcli", "connection", "down", "uuid", uuid], timeout=15)
    if rc != 0:
        xbmcgui.Dialog().ok("Disconnect failed", "Could not disconnect: {}".format(_short_error(out or err)))
        xbmc.log(
            "plugin.program.wifi: disconnect failed ifname={}: {}".format(ifname, (out or err)[:200]),
            xbmc.LOGERROR,
        )
        return

    xbmc.log("plugin.program.wifi: disconnected ifname={}".format(ifname), xbmc.LOGINFO)
    xbmc.executebuiltin("Container.Refresh")


def _short_error(message):
    message = message or ""
    lower = message.lower()
    if "auth" in lower or "password" in lower or "secret" in lower:
        return "Authentication failed."
    if "not found" in lower or "available" in lower:
        return "Network unavailable."
    if "timeout" in lower or "timed out" in lower:
        return "Connection timed out."
    if "already" in lower and "active" in lower:
        return "Already connected."
    if "no property" in lower or "invalid" in lower:
        return "Advanced network configuration required."
    return message[:200] if message else "Unknown error."


def _refresh():
    xbmc.executebuiltin("Container.Refresh")


def main():
    ifname = _get_interface()
    if not ifname:
        xbmcgui.Dialog().ok("Wi-Fi", "No Wi-Fi device found.")
        xbmcplugin.endOfDirectory(ADDON_HANDLE, False)
        return

    params = {}
    if len(sys.argv) > 2:
        params = dict(urllib.parse.parse_qsl(sys.argv[2].lstrip("?")))

    action = params.get("action", "list")
    if action == "list":
        show_networks(ifname)
    elif action == "refresh":
        _refresh()
    elif action == "select":
        select_network(
            params.get("ssid", ""),
            _normalize_security(params.get("security", "Open")),
            ifname,
        )


if __name__ == "__main__":
    main()
