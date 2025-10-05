#!/usr/bin/env python3
# ============================================================
#  UAM REGISTRY MANAGER v1.0
#  Unified Analytical Memory (UAM) — Global Run Ledger
#  © 2025 Anthony Abney. All Rights Reserved.
#  Proprietary / Immutable Authorship License v1.0
#  Trademark: UAM Stamp™
# ============================================================

"""
uam_registry_manager.py
-----------------------
Maintains a persistent JSON registry (`uam_registry.json`)
that records every Unified Analytical Memory (UAM) engine
execution, dataset ingestion, and constant update — now with
cryptographic chain-hash linking for full chronological
integrity (blockchain-style).
"""

import json, os, datetime, platform, getpass, hashlib
from typing import Dict, Any

REGISTRY_FILE = "uam_registry.json"
REGISTRY_VERSION = "1.0"
AUTHOR = "Anthony Abney (immutable)"
LICENSE = "Proprietary / Immutable Authorship License v1.0"
TRADEMARK = "UAM Stamp™"

# --------------------------------------------------------------------
def _load_registry() -> Dict[str, Any]:
    """Load registry or initialize new one if missing."""
    if os.path.exists(REGISTRY_FILE):
        try:
            with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    genesis_hash = hashlib.sha256(b"UAM Genesis Block").hexdigest()
    return {
        "registry": "Unified Analytical Memory (UAM) Global Ledger",
        "version": REGISTRY_VERSION,
        "entries": [],
        "metadata": {
            "author": AUTHOR,
            "license": LICENSE,
            "trademark": TRADEMARK,
            "created": datetime.datetime.utcnow().isoformat() + "Z",
            "genesis_hash": genesis_hash,
        },
    }

# --------------------------------------------------------------------
def _save_registry(registry: Dict[str, Any]):
    with open(REGISTRY_FILE, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)

# --------------------------------------------------------------------
def _compute_signature(entry: Dict[str, Any]) -> str:
    """Compute SHA256 signature of an entry (excluding signature field)."""
    data = {k: v for k, v in entry.items() if k != "signature"}
    serialized = json.dumps(data, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

# --------------------------------------------------------------------
def _get_previous_hash(registry: Dict[str, Any]) -> str:
    """Return the hash of the most recent entry or genesis if none."""
    if registry["entries"]:
        return registry["entries"][-1]["signature"]
    return registry["metadata"]["genesis_hash"]

# --------------------------------------------------------------------
def log_entry(engine: str,
              status: str = "completed",
              constants: Dict[str, Any] = None,
              datasets: Dict[str, Any] = None,
              notes: str = ""):
    """
    Log a new UAM engine event with chain-hash linking.
    """
    reg = _load_registry()
    prev_hash = _get_previous_hash(reg)
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "engine": engine,
        "status": status,
        "host": platform.node(),
        "user": getpass.getuser(),
        "constants": constants or {},
        "datasets": datasets or {},
        "notes": notes,
        "previous_hash": prev_hash,
    }
    entry["signature"] = _compute_signature(entry)
    reg["entries"].append(entry)
    _save_registry(reg)
    print(f"[UAM-REGISTRY] ✅ Logged {engine} ({status}) | SHA256={entry['signature'][:12]}… | Linked to {prev_hash[:10]}…")

# --------------------------------------------------------------------
def verify_registry() -> bool:
    """
    Verify that every entry’s signature and chain-hash linkage are intact.
    """
    reg = _load_registry()
    ok = True
    prev = reg["metadata"]["genesis_hash"]
    for e in reg.get("entries", []):
        expected_sig = _compute_signature({k: v for k, v in e.items() if k != "signature"})
        if e.get("signature") != expected_sig:
            print(f"⚠️  Signature mismatch for {e.get('engine')} @ {e.get('timestamp')}")
            ok = False
        if e.get("previous_hash") != prev:
            print(f"⚠️  Chain break detected before {e.get('engine')} @ {e.get('timestamp')}")
            ok = False
        prev = e.get("signature")
    if ok:
        print("[UAM-REGISTRY] ✅ All entries verified — full chain integrity intact.")
    else:
        print("[UAM-REGISTRY] ❌ Chain integrity compromised.")
    return ok

# --------------------------------------------------------------------
def summarize():
    """
    Display a summary of registry history.
    """
    reg = _load_registry()
    print("============================================================")
    print("📘 Unified Analytical Memory — Cryptographic Ledger Summary")
    print(f"🔢 Total Entries: {len(reg['entries'])}")
    if reg["entries"]:
        latest = reg["entries"][-1]
        print(f"🕒  Last Run: {latest['timestamp']}  Engine: {latest['engine']}")
        print(f"💻  Host: {latest['host']}  User: {latest['user']}")
        print(f"🔗  PrevHash: {latest['previous_hash'][:12]}…")
        print(f"🔐  Signature: {latest['signature'][:12]}…")
    print("============================================================")
    return reg
