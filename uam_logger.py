#!/usr/bin/env python3
# ============================================================
#  UAM LOGGER v1.0
#  Unified Analytical Memory (UAM) Global Registry Writer
#  © 2025 Anthony Abney. All Rights Reserved.
#  Proprietary / Immutable Authorship License v1.0
#  Trademark: UAM Stamp™
# ============================================================

"""
uam_logger.py — internal utility for recording constants, derivations,
and datasets in the Unified Analytical Memory global registry.

Used automatically by uam_research_engine.py, uam_tensor_core.py, and others.

Functions:
    log_constant(name, value, derivation, scale, source, explanation)
    log_derivation(name, formula, description, scale, reproducible)
    log_dataset(name, description, source, validated)
    log_failure(context, reason)
    load_registry()
    save_registry()
"""

import json, os
from datetime import datetime
from pathlib import Path

REGISTRY_FILE = Path("uam_registry.json")

UAM_VERSION = "1.0"
AUTHOR = "Anthony Abney (immutable)"
TRADEMARK = "UAM Stamp™"
LICENSE = "Proprietary / Immutable Authorship License v1.0"

# ============================================================
# Utility
# ============================================================

def _timestamp():
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

def _load():
    if not REGISTRY_FILE.exists():
        return {
            "version": UAM_VERSION,
            "timestamp": _timestamp(),
            "constants": {},
            "derivations": {},
            "datasets": {},
            "failures": []
        }
    with open(REGISTRY_FILE, "r") as f:
        try:
            return json.load(f)
        except Exception:
            return {
                "version": UAM_VERSION,
                "timestamp": _timestamp(),
                "constants": {},
                "derivations": {},
                "datasets": {},
                "failures": []
            }

def _save(reg):
    reg["timestamp"] = _timestamp()
    with open(REGISTRY_FILE, "w") as f:
        json.dump(reg, f, indent=2)

# ============================================================
# Logging Functions
# ============================================================

def log_constant(name, value, derivation, scale="analytic", source=None, explanation=None):
    """Log a mathematical or physical constant."""
    reg = _load()
    reg["constants"][name] = {
        "value": value,
        "derivation": derivation,
        "scale": scale,
        "source": source or "UAM Engine",
        "explanation": explanation or "No explanation provided",
        "timestamp": _timestamp(),
        "author": AUTHOR,
        "license": LICENSE
    }
    _save(reg)
    print(f"[UAM Logger] ✅ Constant logged: {name} = {value}")

def log_derivation(name, formula, description, scale="analytic", reproducible=True):
    """Log a derived equation or formula."""
    reg = _load()
    reg["derivations"][name] = {
        "formula": formula,
        "description": description,
        "scale": scale,
        "reproducible": reproducible,
        "timestamp": _timestamp(),
        "author": AUTHOR,
        "license": LICENSE
    }
    _save(reg)
    print(f"[UAM Logger] ✅ Derivation logged: {name}")

def log_dataset(name, description, source, validated=False):
    """Log a dataset or experimental reference."""
    reg = _load()
    reg["datasets"][name] = {
        "description": description,
        "source": source,
        "validated": validated,
        "timestamp": _timestamp(),
        "author": AUTHOR,
        "license": LICENSE
    }
    _save(reg)
    print(f"[UAM Logger] ✅ Dataset logged: {name}")

def log_failure(context, reason):
    """Log a failed derivation or experiment with reason."""
    reg = _load()
    reg["failures"].append({
        "context": context,
        "reason": reason,
        "timestamp": _timestamp(),
        "author": AUTHOR
    })
    _save(reg)
    print(f"[UAM Logger] ⚠️  Failure recorded: {context} — {reason}")

# ============================================================
# Manual Access
# ============================================================

def load_registry():
    """Load and return registry as dict."""
    return _load()

def save_registry():
    """Force-save current registry (used by other engines)."""
    reg = _load()
    _save(reg)
    print("[UAM Logger] ✅ Registry saved.")

# ============================================================
# Example Run (standalone)
# ============================================================

if __name__ == "__main__":
    print("============================================================")
    print(f"🔷 UAM Logger — Version {UAM_VERSION}")
    print(f"👤 Author: {AUTHOR}")
    print(f"™ Trademark: {TRADEMARK}")
    print(f"📜 License: {LICENSE}")
    print("============================================================")

    # Example test entries (safe)
    log_constant(
        "C_S",
        0.678,
        "Sharp Sobolev embedding constant for H^{3/2} → L^∞ (Talenti, 1976)",
        scale="analytic",
        source="Talenti (1976)",
        explanation="Best known constant ensuring smooth embedding of critical Sobolev spaces."
    )

    log_derivation(
        "BKM_Criterion",
        "∫₀ᵀ ||ω(t)||_∞ dt < ∞ ⇒ smoothness of u(t)",
        "Beale–Kato–Majda condition ensuring Navier–Stokes regularity.",
        scale="fluid",
        reproducible=True
    )

    log_dataset(
        "JHTDB",
        "Johns Hopkins Turbulence Database isotropic1024 dataset",
        "https://turbulence.pha.jhu.edu",
        validated=True
    )

    log_failure(
        "High-frequency angular operator derivation",
        "Microlocal closure failed due to missing coercivity bound"
    )

    print("✅ Example registry updated at:", REGISTRY_FILE.absolute())
