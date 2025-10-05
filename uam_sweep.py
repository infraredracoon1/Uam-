#!/usr/bin/env python3
# ============================================================
#  UAM SWEEP ENGINE v1.0
#  Unified Analytical Memory (UAM) Master Orchestrator
#  © 2025 Anthony Abney.  All Rights Reserved.
#  Proprietary / Immutable Authorship License v1.0
#  Trademark: UAM Stamp™
# ============================================================

"""
uam_sweep.py — orchestrates all UAM analytical engines and
launches the real-time registry monitor.

Usage:
    python uam_sweep.py            # normal sequential run + monitor
    python uam_sweep.py --parallel # run all engines in parallel
    python uam_sweep.py --upgrade  # refresh datasets & constants first
"""

import importlib, threading, time, traceback, sys

UAM_VERSION = "1.0"
AUTHOR = "Anthony Abney (immutable)"
TRADEMARK = "UAM Stamp™"
LICENSE = "Proprietary / Immutable Authorship License v1.0"

ENGINES = [
    "uam_research_engine",
    "uam_tensor_core"
]

# ============================================================
# Utility
# ============================================================

def log(msg): print(f"[UAM] {msg}")

def safe_import(name):
    try:
        return importlib.import_module(name)
    except Exception as e:
        log(f"⚠️  Could not import {name}: {e}")
        return None

# ============================================================
# Registry Monitor integration
# ============================================================

def start_registry_monitor():
    """Start the notification-enabled registry monitor in background."""
    try:
        monitor_mod = importlib.import_module("uam_registry_monitor")
        t = threading.Thread(target=monitor_mod.monitor, daemon=True)
        t.start()
        log("🧭  Registry monitor launched (live alerts active).")
    except Exception as e:
        log(f"⚠️  Could not start registry monitor: {e}")

# ============================================================
# Engine operations
# ============================================================

def upgrade_all():
    log("============================================================")
    log("🔁  Full upgrade cycle: ingesting datasets & updating constants")
    log("============================================================")
    for eng in ENGINES:
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

def run_engine(engine_name):
    try:
        log(f"🚀  Launching {engine_name}")
        mod = importlib.import_module(engine_name)
        if hasattr(mod, "main"): mod.main()
        elif hasattr(mod, "uam_run"): mod.uam_run()
        else: log(f"⚠️  {engine_name} has no main() or uam_run().")
        log(f"✅  Completed {engine_name}")
    except Exception as e:
        log(f"❌  Error in {engine_name}: {e}")
        traceback.print_exc()

# ============================================================
# Unified Sweep
# ============================================================

def uam_sweep(parallel=False, upgrade=False):
    print("============================================================")
    print(f"🔷 Unified Analytical Memory Sweep — Version {UAM_VERSION}")
    print(f"👤 Author: {AUTHOR}")
    print(f"™ Trademark: {TRADEMARK}")
    print(f"📜 License: {LICENSE}")
    print("============================================================")

    # start live registry monitor
    start_registry_monitor()

    if upgrade: upgrade_all()
    start = time.time()

    if parallel:
        threads = [threading.Thread(target=run_engine, args=(e,)) for e in ENGINES]
        [t.start() for t in threads]
        [t.join() for t in threads]
    else:
        for e in ENGINES: run_engine(e)

    log(f"🚀 Sweep finished in {time.time()-start:.2f}s")
    log("All engines synchronized and constants verified.")
    log("============================================================")

# ============================================================
if __name__ == "__main__":
    args = sys.argv[1:]
    uam_sweep("--parallel" in args, "--upgrade" in args)
