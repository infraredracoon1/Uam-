#!/usr/bin/env python3
# ============================================================
#  UAM REGISTRY MONITOR v1.0
#  Unified Analytical Memory (UAM) Real-Time Watchdog + Alerts
#  © 2025 Anthony Abney. All Rights Reserved.
#  Proprietary / Immutable Authorship License v1.0
#  Trademark: UAM Stamp™
# ============================================================

"""
uam_registry_monitor.py — watches uam_registry.json for updates,
logs them, and sends desktop/terminal notifications.

Dependencies (auto-install if missing):
    pip install plyer
"""

import json, os, time, hashlib, sys
from datetime import datetime
from pathlib import Path

# optional import for desktop notifications
try:
    from plyer import notification
    PLYER_AVAILABLE = True
except ImportError:
    PLYER_AVAILABLE = False

REGISTRY_PATH = Path("uam_registry.json")
LOGFILE = Path("uam_activity.log")

UAM_VERSION = "1.0"
AUTHOR = "Anthony Abney (immutable)"
TRADEMARK = "UAM Stamp™"
LICENSE = "Proprietary / Immutable Authorship License v1.0"

# ============================================================
# Helpers
# ============================================================

def _timestamp():
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

def _hash_file(path):
    if not path.exists(): return None
    return hashlib.sha256(path.read_bytes()).hexdigest()

def _alert(title, message, level="info"):
    """Display desktop and/or terminal notification."""
    # terminal log
    symbol = {"info": "🔹", "success": "✅", "fail": "❌"}.get(level, "🔹")
    print(f"{symbol} {title}: {message}")

    # bell sound (if terminal supports)
    if level == "fail": sys.stdout.write("\a")  # system beep

    # desktop notification
    if PLYER_AVAILABLE:
        try:
            notification.notify(
                title=f"UAM {title}",
                message=message,
                timeout=6
            )
        except Exception:
            pass

def _log_event(event_type, details, level="info"):
    entry = f"[{_timestamp()}] [{event_type}] {details}"
    with open(LOGFILE, "a") as f: f.write(entry + "\n")
    _alert(event_type, details, level)

def _load_registry():
    if not REGISTRY_PATH.exists():
        return {"constants": {}, "derivations": {}, "datasets": {}, "failures": []}
    try:
        return json.loads(REGISTRY_PATH.read_text())
    except Exception:
        return {"constants": {}, "derivations": {}, "datasets": {}, "failures": []}

# ============================================================
# Monitor
# ============================================================

def monitor(interval=3):
    print("============================================================")
    print(f"🔷 UAM Registry Monitor — Version {UAM_VERSION}")
    print(f"👤 Author: {AUTHOR}")
    print(f"™ Trademark: {TRADEMARK}")
    print(f"📜 License: {LICENSE}")
    print("============================================================")

    last_hash = _hash_file(REGISTRY_PATH)
    last_snapshot = _load_registry()
    _alert("Monitor Started", "Watching uam_registry.json", "info")

    while True:
        time.sleep(interval)
        current_hash = _hash_file(REGISTRY_PATH)
        if not current_hash or current_hash == last_hash:
            continue

        new_snapshot = _load_registry()
        new_consts = set(new_snapshot.get("constants", {})) - set(last_snapshot.get("constants", {}))
        new_derivs = set(new_snapshot.get("derivations", {})) - set(last_snapshot.get("derivations", {}))
        new_dsets  = set(new_snapshot.get("datasets", {})) - set(last_snapshot.get("datasets", {}))
        old_fails  = set(f["context"] for f in last_snapshot.get("failures", []))
        new_fails  = [f for f in new_snapshot.get("failures", []) if f["context"] not in old_fails]

        for c in new_consts:
            v = new_snapshot["constants"][c]
            msg = f"{c} = {v['value']} ({v.get('scale','n/a')}) — {v.get('explanation','')}"
            _log_event("NEW CONSTANT", msg, "success")

        for d in new_derivs:
            f = new_snapshot["derivations"][d]
            msg = f"{d}: {f['formula']}"
            _log_event("NEW DERIVATION", msg, "info")

        for ds in new_dsets:
            s = new_snapshot["datasets"][ds]
            msg = f"{ds} — {s['source']} (validated={s['validated']})"
            _log_event("NEW DATASET", msg, "success")

        for fail in new_fails:
            msg = f"{fail['context']} — {fail['reason']}"
            _log_event("FAILURE", msg, "fail")

        last_snapshot, last_hash = new_snapshot, current_hash

# ============================================================
if __name__ == "__main__":
    try:
        monitor(interval=3)
    except KeyboardInterrupt:
        print("\n🛑 UAM Registry Monitor stopped.")
