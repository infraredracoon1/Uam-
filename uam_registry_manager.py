#!/usr/bin/env python3
# ============================================================
#  UAM REGISTRY MANAGER v1.0
#  Unified Analytical Memory (UAM) — Global Run Ledger
#  © 2025 Anthony Abney.  All Rights Reserved.
#  Proprietary / Immutable Authorship License v1.0
#  Trademark: UAM Stamp™
# ============================================================

"""
uam_registry_manager.py
-----------------------
Maintains a persistent JSON registry (`uam_registry.json`)
logging every Unified Analytical Memory (UAM) engine execution,
dataset ingestion, and constant update.
"""

import json, os, datetime, platform, getpass
from typing import Dict, Any

REGISTRY_FILE = "uam_registry.json"

# --------------------------------------------------------------------
def _load_registry() -> Dict[str, Any]:
    if os.path.exists(REGISTRY_FILE):
        try:
            with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "registry": "Unified Analytical Memory (UAM) Global Ledger",
        "version": "1.0",
        "entries": [],
        "metadata": {
            "author": "Anthony Abney (immutable)",
            "license": "Proprietary / Immutable Authorship License v1.0",
            "trademark": "UAM Stamp™",
            "created": datetime.datetime.utcnow().isoformat() + "Z",
        },
    }

# --------------------------------------------------------------------
def _save_registry(registry: Dict[str, Any]):
    with open(REGISTRY_FILE, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)

# --------------------------------------------------------------------
def log_entry(engine: str, status: str = "completed",
              constants: Dict[str, Any] = None,
              datasets: Dict[str, Any] = None,
              notes: str = ""):
    """
    Append a new entry to the registry.
    """
    reg = _load_registry()
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "engine": engine,
        "status": status,
        "host": platform.node(),
        "user": getpass.getuser(),
        "constants": constants or {},
        "datasets": datasets or {},
        "notes": notes,
    }
    reg["entries"].append(entry)
    _save_registry(reg)
    print(f"[UAM-REGISTRY] Logged run of {engine} ({status})")

# --------------------------------------------------------------------
def summarize():
    """
    Display a brief summary of the registry.
    """
    reg = _load_registry()
    print("============================================================")
    print("📘 Unified Analytical Memory — Run Ledger Summary")
    print(f"🔢 Total Entries: {len(reg['entries'])}")
    if reg["entries"]:
        latest = reg["entries"][-1]
        print(f"🕒  Last Run: {latest['timestamp']}  Engine: {latest['engine']}")
        print(f"💻  Host: {latest['host']}  User: {latest['user']}")
    print("============================================================")
    return reg
