#!/usr/bin/env python3
"""Wi-Fi Manager — thin NetworkManager frontend for Kodi.

Scans, connects, and disconnects Wi-Fi via nmcli.  Never modifies saved
NetworkManager profiles, credentials, autoconnect, or netplan configuration.
"""
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
    """Run a command and return (returncode, stdout, stderr)."""
    try:
        r = subprocess.run(
            cmd, capture_output=True, text=True,
            env=_nm_env(), timeout=timeout,
        )
        return r.returncode, r.stdout.strip(), r.stderr.strip()
    except subprocess.TimeoutExpired:
        return -1, "", "Timed out"
    except Exception as exc:
        return -1, "", str(exc)


def _nmcli_values(fields, *args, timeout=15):
    """nmcli -g <fields> — returns values only, no field-name prefix."""
    cmd = ["nmcli", "-g", ",".join(fields)] + list(args)
    rc, out, _ = _run(cmd, timeout=timeout)
    return out.splitlines() if rc == 0 else []


def _nmcli_raw(*args, timeout=15):
    """Run nmcli and return raw stdout lines."""
    cmd = ["nmcli"] + list(args)
    rc, out, _ = _run(cmd, timeout=timeout)
    return out.splitlines() if rc == 0 else []


# ── Interface ───────────────────────────────────────────────────────────

def _get_interface():
    """Return the first Wi-Fi interface, defaulting to wlan0."""
    for line in _nmcli_raw("-t", "-e", "yes",
                           "-f", "DEVICE,TYPE",
                           "device", "status"):
        device, typ = _parse_escaped_colons(line, 2)
        if typ == "wifi" and "p2p" not in device:
            return device
    return "wlan0"


# ── Active SSID / UUID ─────────────────────────────────────────────────

def _get_active_ssid(ifname):
    """Return the SSID currently connected on *ifname*, or None."""
    for line in _nmcli_raw("-t", "-e", "yes",
                           "-f", "ACTIVE,SSID",
                           "device", "wifi", "list",
                           "ifname", ifname):
        in_use, ssid = _parse_escaped_colons(line, 2)
        if in_use == "*" and ssid:
            return ssid
    return None


def _get_active_uuid(ifname):
    """Return the UUID of the active connection on *ifname*, or None."""
    for line in _nmcli_raw("-t", "-e", "yes",
                           "-f", "NAME,UUID,DEVICE",
                           "connection", "show", "--active"):
        _name, uuid, device = _parse_escaped_colons(line, 3)
        if device == ifname:
            return uuid
    return None


# ── Saved profile lookup ───────────────────────────────────────────────

def _find_saved_uuid(ssid):
    """Find a saved NM Wi-Fi profile UUID whose SSID matches."""
    for line in _nmcli_raw("-t", "-e", "yes",
                           "-f", "NAME,UUID,TYPE",
                           "connection", "show"):
        _name, uuid, typ = _parse_escaped_colons(line, 3)
        if typ == "802-11-wireless":
            ssid_val = _nmcli_values(["802-11-wireless.ssid"],
                                     "connection", "show", uuid)
            if ssid_val and ssid_val[0] == ssid:
                return uuid
    return None


# ── Connection verification ────────────────────────────────────────────

def _verify_connection(ssid, ifname, timeout=8):
    """Poll NetworkManager for up to *timeout* seconds.

    Returns True only if *ssid* remains the active SSID continuously
    for at least 3 seconds.
    """
    required_stable = 3.0
    stable_since = None
    deadline = time.monotonic() + timeout
    while True:
        now = time.monotonic()
        if _get_active_ssid(ifname) == ssid:
            if stable_since is None:
                stable_since = now
            elif now - stable_since >= required_stable:
                return True
        else:
            stable_since = None
        if now >= deadline:
            break
        time.sleep(0.5)
    return False


# ── Terse-mode parser ─────────────────────────────────────────────────

def _parse_escaped_colons(line, count):
    """Split an nmcli -e yes line on unescaped colons, unescape tokens."""
    fields = []
    current = []
    i = 0
    while i < len(line) and len(fields) < count:
        ch = line[i]
        if ch == "\\" and i + 1 < len(line):
            current.append(line[i + 1])
            i += 2
        elif ch == ":" and len(fields) < count - 1:
            fields.append("".join(current))
            current = []
            i += 1
        else:
            current.append(ch)
            i += 1
    fields.append("".join(current))
    return fields


# ── Network list ────────────────────────────────────────────────────────

def _signal_bar(signal):
    if signal >= 80:
        return " \u2582\u2584\u2586\u2588"
    elif signal >= 60:
        return " \u2582\u2584\u2586_"
    elif signal >= 40:
        return " \u2582\u2584__"
    elif signal >= 20:
        return " \u2582___"
    return ""


def scan_networks(ifname):
    """Return deduplicated visible networks sorted by connected-first, signal."""
    raw = _nmcli_raw("-t", "-e", "yes",
                     "-f", "IN-USE,SSID,SIGNAL,SECURITY",
                     "device", "wifi", "list",
                     "--rescan", "yes",
                     "ifname", ifname,
                     timeout=20)
    if not raw:
        return []

    active_ssid = _get_active_ssid(ifname)

    networks = {}
    for line in raw:
        in_use, ssid, sig_str, security = _parse_escaped_colons(line, 4)
        if not ssid or ssid == "--":
            continue
        try:
            signal = int(sig_str)
        except ValueError:
            continue
        if not (1 <= signal <= 100):
            continue
        sec = security if security else "Open"

        is_active = (in_use == "*") or (ssid == active_ssid)
        prev = networks.get(ssid)
        if prev is None or is_active or signal > prev["signal"]:
            networks[ssid] = {
                "ssid": ssid,
                "signal": signal,
                "security": sec,
                "connected": is_active,
            }

    return sorted(networks.values(),
                  key=lambda n: (not n["connected"], -n["signal"]))


def show_networks(ifname):
    """Display the network list in Kodi."""
    xbmcplugin.setContent(ADDON_HANDLE, "files")

    li = xbmcgui.ListItem(label="[B]Refresh networks[/B]")
    xbmcplugin.addDirectoryItem(
        handle=ADDON_HANDLE,
        url="{}?action=refresh".format(sys.argv[0]),
        listitem=li, isFolder=False)

    networks = scan_networks(ifname)

    for net in networks:
        prefix = "[COLOR green]\u2713[/COLOR] " if net["connected"] else "  "
        bar = _signal_bar(net["signal"])
        label = "{}{}{} \u2014 {}% \u2014 {}".format(
            prefix, net["ssid"], bar, net["signal"], net["security"])
        li = xbmcgui.ListItem(label=label)
        li.setInfo("programs", {"title": net["ssid"]})
        url = "{}?action=select&ssid={}&security={}".format(
            sys.argv[0],
            urllib.parse.quote(net["ssid"], safe=""),
            urllib.parse.quote(net["security"], safe=""))
        xbmcplugin.addDirectoryItem(
            handle=ADDON_HANDLE, url=url, listitem=li, isFolder=False)

    if not networks:
        li = xbmcgui.ListItem(label="No networks found")
        xbmcplugin.addDirectoryItem(
            handle=ADDON_HANDLE, url="", listitem=li, isFolder=False)

    xbmcplugin.endOfDirectory(ADDON_HANDLE, True)


# ── Connection logic ────────────────────────────────────────────────────

def _is_enterprise(security):
    """Return True if the security string indicates 802.1X / EAP."""
    up = security.upper()
    return "802.1X" in up or "EAP" in up


def select_network(ssid, security, ifname):
    """Handle user selecting an SSID from the list."""
    active_ssid = _get_active_ssid(ifname)

    # ── Currently connected → Disconnect / Cancel ──────────────────────
    if active_ssid == ssid:
        choice = xbmcgui.Dialog().select(ssid, ["Disconnect", "Cancel"])
        if choice == 0:
            _disconnect(ifname)
        return

    # ── Saved profile exists → activate it (no modification) ───────────
    saved_uuid = _find_saved_uuid(ssid)
    if saved_uuid:
        _activate_saved(saved_uuid, ssid, ifname, security)
        return

    # ── 802.1X / Enterprise → refuse ──────────────────────────────────
    if _is_enterprise(security):
        xbmcgui.Dialog().ok(
            "Wi-Fi",
            "Advanced network configuration required \u2014 use KDE "
            "NetworkManager to configure [B]{}[/B].".format(ssid))
        return

    # ── No saved profile → new connection ──────────────────────────────
    _connect_new(ssid, security, ifname)


def _activate_saved(uuid, ssid, ifname, security=""):
    """Activate an existing saved profile.  Never modifies it."""
    cmd = ["nmcli", "--wait", "20", "connection", "up", "uuid", uuid,
           "ifname", ifname]
    rc, out, err = _run(cmd, timeout=30)
    xbmc.log(
        "plugin.program.wifi: activate saved ssid='{}' rc={}".format(
            ssid, rc),
        xbmc.LOGINFO)
    if rc != 0:
        msg = out or err
        xbmcgui.Dialog().ok(
            "Connection failed",
            "Could not connect to [B]{}[/B]:\n{}".format(
                ssid, _short_error(msg)))
        xbmc.log(
            "plugin.program.wifi: activation failed ssid='{}': {}".format(
                ssid, msg),
            xbmc.LOGERROR)
        return

    if not _verify_connection(ssid, ifname):
        xbmcgui.Dialog().ok(
            "Connection failed",
            "Could not stay connected to [B]{}[/B].".format(ssid))
        xbmc.log(
            "plugin.program.wifi: verification failed ssid='{}'".format(ssid),
            xbmc.LOGERROR)
        return

    _show_success(ssid, ifname, security)


def _connect_new(ssid, security, ifname):
    """Connect to a network with no saved profile."""
    cmd = ["nmcli", "--wait", "20", "device", "wifi", "connect", ssid,
           "ifname", ifname]
    if security and security != "Open":
        pw = xbmcgui.Dialog().input(
            "Enter Wi-Fi password for [B]{}[/B]".format(ssid),
            type=xbmcgui.INPUT_ALPHANUM,
            option=xbmcgui.ALPHANUM_HIDE_INPUT)
        if not pw:
            return
        cmd += ["password", pw]

    rc, out, err = _run(cmd, timeout=30)
    xbmc.log(
        "plugin.program.wifi: new connect ssid='{}' rc={}".format(ssid, rc),
        xbmc.LOGINFO)
    if rc != 0:
        msg = out or err
        xbmcgui.Dialog().ok(
            "Connection failed",
            "Could not connect to [B]{}[/B]:\n{}".format(
                ssid, _short_error(msg)))
        xbmc.log(
            "plugin.program.wifi: new connect failed ssid='{}': {}".format(
                ssid, msg),
            xbmc.LOGERROR)
        return

    if not _verify_connection(ssid, ifname):
        xbmcgui.Dialog().ok(
            "Connection failed",
            "Could not stay connected to [B]{}[/B].".format(ssid))
        xbmc.log(
            "plugin.program.wifi: verification failed ssid='{}'".format(ssid),
            xbmc.LOGERROR)
        return

    _show_success(ssid, ifname, security)


def _show_success(ssid, ifname, security=""):
    """Display success dialog and refresh Kodi directory."""
    hint = ""
    if not security or security == "Open":
        hint = "\n\nThis network may require a web sign-in."
    xbmcgui.Dialog().ok("Wi-Fi",
                        "Connected to [B]{}[/B]{}".format(ssid, hint))
    show_networks(ifname)


def _disconnect(ifname):
    """Disconnect without deleting profile or altering credentials."""
    uuid = _get_active_uuid(ifname)
    cmd = (["nmcli", "connection", "down", "uuid", uuid] if uuid
           else ["nmcli", "device", "disconnect", ifname])
    rc, out, err = _run(cmd, timeout=15)
    if rc == 0:
        xbmc.log("plugin.program.wifi: disconnected ifname={}".format(ifname),
                 xbmc.LOGINFO)
        show_networks(ifname)
    else:
        xbmcgui.Dialog().ok(
            "Disconnect failed",
            "Could not disconnect: {}".format(_short_error(out or err)))
        xbmc.log(
            "plugin.program.wifi: disconnect failed ifname={}: {}".format(
                ifname, out or err),
            xbmc.LOGERROR)


def _short_error(msg):
    lower = msg.lower()
    if "auth" in lower or "password" in lower or "secret" in lower:
        return "Authentication failed."
    if "not found" in lower or "available" in lower:
        return "Network unavailable."
    if "timeout" in lower:
        return "Connection timed out."
    if "already" in lower and "active" in lower:
        return "Already connected."
    if "no property" in lower or "invalid" in lower:
        return "Advanced network configuration required \u2014 use KDE NetworkManager."
    return msg[:200] if msg else "Unknown error."


# ── Main ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    ifname = _get_interface()

    params = {}
    if len(sys.argv) > 2:
        params = dict(urllib.parse.parse_qsl(sys.argv[2].lstrip("?")))

    action = params.get("action", "list")

    if action in ("list", "refresh"):
        show_networks(ifname)
    elif action == "select":
        ssid = params.get("ssid", "")
        security = params.get("security", "Open")
        select_network(ssid, security, ifname)
