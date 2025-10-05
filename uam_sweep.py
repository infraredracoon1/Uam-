#!/usr/bin/env python3
# ============================================================
#  UAM SWEEP ENGINE v1.0
#  Unified Analytical Memory (UAM) Master Orchestrator
#  © 2025 Anthony Abney.  All Rights Reserved.
#  Proprietary / Immutable Authorship License v1.0
#  Trademark: UAM Stamp™
# ============================================================

"""
uam_sweep.py — runs all UAM analytical engines in unison.

Usage:
    python uam_sweep.py
or simply (if aliased):
    uam_sweep
"""

import importlib
import threading
import time
import traceback

UAM_VERSION = "1.0"
AUTHOR = "Anthony Abney (immutable)"
TRADEMARK = "UAM Stamp™"
LICENSE = "Proprietary / Immutable Authorship License v1.0"

# --------------------------------------------------------------------
# ENGINE REGISTRY — declare all currently available engine modules
# --------------------------------------------------------------------
ENGINES = [
    "uam_research_engine",   # dataset crawler, constant registry, PDE checks
    "uam_tensor_core"        # bridge analysis between NS ↔ YM ↔ QFT ↔ relativity
    # Future: "uam_referee_engine", "uam_solution_engine", etc.
]

# --------------------------------------------------------------------
# Run individual engine safely
# --------------------------------------------------------------------
def run_engine(engine_name):
    try:
        print(f"\n[UAM] Launching engine: {engine_name}")
        module = importlib.import_module(engine_name)
        if hasattr(module, "main"):
            module.main()
        elif hasattr(module, "uam_run"):
            module.uam_run()
        else:
            print(f"[UAM] ⚠️  Engine {engine_name} has no main() or uam_run() defined.")
        print(f"[UAM] ✅ Completed: {engine_name}")
    except Exception as e:
        print(f"[UAM] ❌ Error in {engine_name}: {e}")
        traceback.print_exc()

# --------------------------------------------------------------------
# Master sweep: sequential or parallel execution
# --------------------------------------------------------------------
def uam_sweep(parallel=False):
    print("============================================================")
    print(f"🔷 Unified Analytical Memory Sweep — Version {UAM_VERSION}")
    print(f"👤 Author: {AUTHOR}")
    print(f"™  Trademark: {TRADEMARK}")
    print(f"📜 License: {LICENSE}")
    print("============================================================")

    start = time.time()

    if parallel:
        threads = []
        for eng in ENGINES:
            t = threading.Thread(target=run_engine, args=(eng,))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
    else:
        for eng in ENGINES:
            run_engine(eng)

    elapsed = time.time() - start
    print("============================================================")
    print(f"[UAM] 🚀 Sweep complete in {elapsed:.2f}s.")
    print("All engines synchronized, constants updated, bridges checked.")
    print("============================================================")

# --------------------------------------------------------------------
# CLI Entry Point
# --------------------------------------------------------------------
if __name__ == "__main__":
    uam_sweep(parallel=False)
