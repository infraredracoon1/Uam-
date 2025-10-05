#!/usr/bin/env python3
# ============================================================
#  UAM VIEWER v1.0
#  Unified Analytical Memory Registry Inspector
#  © 2025 Anthony Abney.  All Rights Reserved.
#  Proprietary / Immutable Authorship License v1.0
#  Trademark: UAM Stamp™
# ============================================================

"""
uam_viewer.py — command-line / notebook interface for inspecting the
UAM Global Registry and engine logs.

Usage (terminal):
    python uam_viewer.py --list
    python uam_viewer.py --show constant:C_S
    python uam_viewer.py --search "spectral gap"
    python uam_viewer.py --export registry.json
"""

import json, sys, os, textwrap
from pathlib import Path
from datetime import datetime

REGISTRY_FILE = Path("uam_registry.json")
VERSION = "1.0"
AUTHOR = "Anthony Abney (immutable)"
TRADEMARK = "UAM Stamp™"
LICENSE = "Proprietary / Immutable Authorship License v1.0"

# ------------------------------------------------------------
def load_registry():
    if not REGISTRY_FILE.exists():
        print("[UAM] ⚠️  Registry not found — run uam_sweep first.")
        return {"constants": {}, "derivations": {}, "datasets": {}}
    try:
        with open(REGISTRY_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"[UAM] ❌  Failed to load registry: {e}")
        return {}

def pretty(obj):
    return json.dumps(obj, indent=2, sort_keys=True)

# ------------------------------------------------------------
def list_all(reg):
    print("============================================================")
    print("📚  UAM Global Registry Overview")
    print("============================================================")
    print(f"Constants logged: {len(reg.get('constants',{}))}")
    print(f"Derivations logged: {len(reg.get('derivations',{}))}")
    print(f"Datasets logged: {len(reg.get('datasets',{}))}")
    print("------------------------------------------------------------")
    for section in ["constants","derivations","datasets"]:
        print(f"[{section.upper()}]")
        for key in reg.get(section,{}).keys():
            print(f"  • {key}")
        print("------------------------------------------------------------")

def show_entry(reg, token):
    """Example: constant:C_S or derivation:BKM"""
    if ":" not in token:
        print("[UAM] ❌  Please specify category:name (e.g. constant:C_S)")
        return
    section, key = token.split(":",1)
    section = section.lower()+"s"
    data = reg.get(section,{}).get(key)
    if not data:
        print(f"[UAM] ❌  No entry for {key} in {section}")
        return
    print(f"============================================================\n🔹  {section[:-1].capitalize()}: {key}\n============================================================")
    print(pretty(data))

def search_entries(reg, phrase):
    phrase = phrase.lower()
    hits = []
    for section, items in reg.items():
        if not isinstance(items, dict): continue
        for key, val in items.items():
            txt = json.dumps(val).lower()
            if phrase in key.lower() or phrase in txt:
                hits.append((section,key))
    if not hits:
        print(f"[UAM] ❌  No matches for '{phrase}'.")
        return
    print(f"============================================================\n🔍  Matches for '{phrase}'\n============================================================")
    for sec,key in hits:
        print(f"[{sec.upper()}] {key}")

def export_registry(reg, path):
    try:
        with open(path,"w") as f:
            json.dump(reg,f,indent=2)
        print(f"[UAM] ✅  Exported registry to {path}")
    except Exception as e:
        print(f"[UAM] ❌  Export failed: {e}")

# ------------------------------------------------------------
def main():
    print("============================================================")
    print(f"🔷 UAM Registry Viewer — Version {VERSION}")
    print(f"👤 Author: {AUTHOR}")
    print(f"™ Trademark: {TRADEMARK}")
    print(f"📜 License: {LICENSE}")
    print("============================================================")

    reg = load_registry()
    args = sys.argv[1:]
    if not args or "--list" in args:
        list_all(reg)
        return

    if "--show" in args:
        idx = args.index("--show")
        if idx+1 < len(args): show_entry(reg,args[idx+1])
        else: print("[UAM] ❌  Missing argument after --show")
        return

    if "--search" in args:
        idx = args.index("--search")
        if idx+1 < len(args): search_entries(reg,args[idx+1])
        else: print("[UAM] ❌  Missing argument after --search")
        return

    if "--export" in args:
        idx = args.index("--export")
        if idx+1 < len(args): export_registry(reg,args[idx+1])
        else: print("[UAM] ❌  Missing argument after --export")
        return

    print("[UAM] ℹ️  Use --list, --show, --search, or --export")

# ------------------------------------------------------------
if __name__ == "__main__":
    main()
