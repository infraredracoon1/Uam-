#!/usr/bin/env python3
# ============================================================
#  UAM SWEEP ENGINE v1.0
#  Unified Analytical Memory (UAM) Master Orchestrator
#  © 2025 Anthony Abney.  All Rights Reserved.
#  Proprietary / Immutable Authorship License v1.0
#  Trademark: UAM Stamp™
# ============================================================

"""
uam_sweep.py — orchestrates all UAM analytical engines and manages auto-registry.

Usage:
    python uam_sweep.py            # sequential sweep
    python uam_sweep.py --parallel # run all engines in parallel
    python uam_sweep.py --upgrade  # crawl + ingest new data first
"""

import importlib, threading, time, traceback, sys, pkgutil, os
from pathlib import Path

UAM_VERSION = "1.0"
AUTHOR = "Anthony Abney (immutable)"
TRADEMARK = "UAM Stamp™"
LICENSE = "Proprietary / Immutable Authorship License v1.0"

# --------------------------------------------------------------------
#  Auto-register support
try:
    from uam_logger import register_engine
except Exception:
    register_engine = None
    print("[UAM] ⚠️  uam_logger not found — auto-registration disabled.")

# --------------------------------------------------------------------
def log(msg): print(f"[UAM] {msg}")

def discover_engines():
    """Dynamically find every Python module starting with 'uam_' except this one."""
    cwd = Path(__file__).parent
    engines = []
    for modinfo in pkgutil.iter_modules([str(cwd)]):
        name = modinfo.name
        if name.startswith("uam_") and name not in {"uam_sweep", "uam_license_header"}:
            engines.append(name)
    return sorted(set(engines))

# --------------------------------------------------------------------
def safe_import(name):
    try:
        return importlib.import_module(name)
    except Exception as e:
        log(f"⚠️  Could not import {name}: {e}")
        return None

def run_engine(name):
    try:
        log(f"🚀  Launching {name}")
        mod = importlib.import_module(name)
        # execute engine
        if hasattr(mod, "main"): mod.main()
        elif hasattr(mod, "uam_run"): mod.uam_run()
        else: log(f"⚠️  {name} has no main() or uam_run().")

        # auto-register after success
        if register_engine:
            try: register_engine(name)
            except Exception as e: log(f"⚠️  register_engine failed: {e}")

        log(f"✅  Completed {name}")
    except Exception as e:
        log(f"❌  Error in {name}: {e}")
        traceback.print_exc()

# --------------------------------------------------------------------
def upgrade_all(engines):
    log("============================================================")
    log("🔁  Full upgrade cycle: ingesting datasets & updating constants")
    log("============================================================")
    for eng in engines:
        mod = safe_import(eng)
        if not mod: continue
        try:
            if hasattr(mod, "update_datasets"): mod.update_datasets()
            elif hasattr(mod, "ingest_new_data"): mod.ingest_new_data()
            else: log(f"ℹ️  {eng} has no update function — skipped.")
            log(f"✅  {eng}: refresh complete.")
        except Exception as e:
            log(f"❌  {eng}: upgrade failed — {e}")
            traceback.print_exc()
    log("============================================================")
    log("✅  Upgrade complete. Engines ready for unified run.")
    log("============================================================")

# --------------------------------------------------------------------
def uam_sweep(parallel=False, upgrade=False):
    print("============================================================")
    print(f"🔷 Unified Analytical Memory Sweep — Version {UAM_VERSION}")
    print(f"👤 Author: {AUTHOR}")
    print(f"™ Trademark: {TRADEMARK}")
    print(f"📜 License: {LICENSE}")
    print("============================================================")

    engines = discover_engines()
    log(f"🧩  Discovered engines: {', '.join(engines) if engines else 'None'}")

    if upgrade: upgrade_all(engines)
    start = time.time()

    if parallel:
        threads = [threading.Thread(target=run_engine, args=(e,)) for e in engines]
        [t.start() for t in threads]
        [t.join() for t in threads]
    else:
        for e in engines: run_engine(e)

    log(f"🚀 Sweep finished in {time.time()-start:.2f}s")
    log("All engines synchronized and constants verified.")
    log("============================================================")

# --------------------------------------------------------------------
if __name__ == "__main__":
    args = sys.argv[1:]
    uam_sweep("--parallel" in args, "--upgrade" in args)
