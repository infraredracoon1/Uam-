#!/usr/bin/env python3
# ============================================================
#  UAM REGISTRY MONITOR v1.0
#  Unified Analytical Memory (UAM) Real-Time Watchdog
#  © 2025 Anthony Abney. All Rights Reserved.
#  Proprietary / Immutable Authorship License v1.0
#  Trademark: UAM Stamp™
# ============================================================

"""
uam_registry_monitor.py — watches uam_registry.json for updates
and logs new constants, derivations, datasets, and failures.

Runs as a lightweight local daemon. Works seamlessly with:
    - uam_logger.py
    - uam_research_engine.py
    - uam_tensor_core.py
    - uam_sweep.py
"""

import json, os, time, hashlib
from datetime import datetime
from pathlib import Path

REGISTRY_PATH = Path("uam_registry.json")
LOGFILE = Path("uam_activity.log")

UAM_VERSION = "1.0"
AUTHOR = "Anthony Abney (immutable)"
TRADEMARK = "UAM Stamp™"
LICENSE = "Proprietary / Immutable Authorship License v1.0"

# ============================================================
# Helper Functions
# ============================================================

def _timestamp():
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

def _hash_file(path):
    if not path.exists():
        return None
    data = path.read_bytes()
    return hashlib.sha256(data).hexdigest()

def _log_event(event_type, details):
    """Append activity to console + file."""
    entry = f"[{_timestamp()}] [{event_type}] {details}"
    print(entry)
    with open(LOGFILE, "a") as f:
        f.write(entry + "\n")

def _load_registry():
    if not REGISTRY_PATH.exists():
        return {"constants": {}, "derivations": {}, "datasets": {}, "failures": []}
    try:
        with open(REGISTRY_PATH, "r") as f:
            return json.load(f)
    except Exception:
        return {"constants": {}, "derivations": {}, "datasets": {}, "failures": []}

# ============================================================
# Core Monitor Loop
# ============================================================

def monitor(interval=5):
    """Continuously watch registry file for changes."""
    print("============================================================")
    print(f"🔷 UAM Registry Monitor — Version {UAM_VERSION}")
    print(f"👤 Author: {AUTHOR}")
    print(f"™ Trademark: {TRADEMARK}")
    print(f"📜 License: {LICENSE}")
    print("============================================================")

    last_hash = _hash_file(REGISTRY_PATH)
    last_snapshot = _load_registry()

    while True:
        time.sleep(interval)
        current_hash = _hash_file(REGISTRY_PATH)
        if not current_hash or current_hash == last_hash:
            continue

        # File changed → detect differences
        new_snapshot = _load_registry()

        new_consts = set(new_snapshot.get("constants", {})) - set(last_snapshot.get("constants", {}))
        new_derivs = set(new_snapshot.get("derivations", {})) - set(last_snapshot.get("derivations", {}))
        new_dsets  = set(new_snapshot.get("datasets", {})) - set(last_snapshot.get("datasets", {}))
        old_fails  = set(f["context"] for f in last_snapshot.get("failures", []))
        new_fails  = [f for f in new_snapshot.get("failures", []) if f["context"] not in old_fails]

        for c in new_consts:
            v = new_snapshot["constants"][c]
            _log_event("NEW CONSTANT", f"{c} = {v['value']} ({v.get('scale', 'n/a')}) — {v.get('explanation', '')}")

        for d in new_derivs:
            f = new_snapshot["derivations"][d]
            _log_event("NEW DERIVATION", f"{d}: {f['formula']}")

        for ds in new_dsets:
            s = new_snapshot["datasets"][ds]
            _log_event("NEW DATASET", f"{ds} — {s['source']} (validated={s['validated']})")

        for fail in new_fails:
            _log_event("FAILURE", f"{fail['context']} — {fail['reason']}")

        last_snapshot = new_snapshot
        last_hash = current_hash

# ============================================================
# Standalone Execution
# ============================================================

if __name__ == "__main__":
    try:
        monitor(interval=3)  # check every 3 seconds
    except KeyboardInterrupt:
        print("\n🛑 UAM Registry Monitor stopped.")
