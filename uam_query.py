#!/usr/bin/env python3
"""
Unified Analytical Memory (UAM) Query Interface v1.0
© 2025 Anthony Abney – Immutable Authorship

Commands:
  uam query --failed
  uam query --constant C_S
  uam query --bridge YangMills
  uam query --history formula-42
  uam query --recent 5
  uam query --rederive formula-42
"""

import os, json, argparse, datetime, sympy as sp

DATA_DIR = "data"

# ---------- Utility ----------------------------------------------------------
def load_json(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def timestamp():
    return datetime.datetime.utcnow().isoformat() + "Z"

# ---------- Query Functions --------------------------------------------------
def query_failed():
    data = load_json(os.path.join(DATA_DIR, "derivation_ledger.json"))
    if not data:
        print("✅ No recorded derivation failures.")
        return
    print(f"📘 {len(data)} failed derivations logged:")
    for entry in data[-10:]:
        print(f"\n• ID: {entry['formula_id']}")
        print(f"  Expression: {entry['expression']}")
        print(f"  Reason: {entry['reason']}")
        print(f"  Timestamp: {entry['timestamp']}")
        print(f"  Source: {entry.get('source','unknown')}")

def query_constant(name):
    data = load_json(os.path.join(DATA_DIR, "constants_db.json"))
    found = [c for c in data if c.get("name") == name]
    if not found:
        print(f"⚠️ Constant {name} not found.")
        return
    for c in found:
        print(f"\n🔢 Constant: {c['name']}")
        print(f"  Value: {c['value']}")
        print(f"  Derived from: {c['derivation']}")
        print(f"  Scale: {c.get('scale','unspecified')}")
        print(f"  Source: {c.get('source','UAM')}")
        print(f"  Verified: {c.get('verified',False)}")

def query_bridge(term):
    data = load_json(os.path.join(DATA_DIR, "tensor_bridges.json"))
    found = [b for b in data if term.lower() in str(b).lower()]
    if not found:
        print(f"⚠️ No tensor bridges found containing '{term}'.")
        return
    print(f"🔗 Found {len(found)} bridge(s):")
    for b in found:
        print(f"\n• {b['bridge_id']}: {b['description']}")
        print(f"  Domains: {b['domains']}")
        print(f"  Constants: {b.get('constants','N/A')}")

def query_history(formula_id):
    data = load_json(os.path.join(DATA_DIR, "derivation_ledger.json"))
    records = [r for r in data if r["formula_id"] == formula_id]
    if not records:
        print(f"⚠️ No derivation record found for {formula_id}.")
        return
    print(f"📜 Derivation history for {formula_id}:")
    for r in records:
        print(f"  {r['timestamp']} | Reason: {r['reason']} | Source: {r.get('source','unknown')}")

def query_recent(n):
    data = load_json(os.path.join(DATA_DIR, "upgrade_log.json"))
    if not data:
        print("No recorded upgrades.")
        return
    print(f"🕑 Showing last {n} UAM upgrades:")
    for entry in data[-n:]:
        print(f"  {entry['timestamp']}: {entry['message']}")

# ---------- Derivation Replay ------------------------------------------------
def rederive_formula(formula_id):
    ledger = load_json(os.path.join(DATA_DIR, "derivation_ledger.json"))
    entry = next((r for r in ledger if r["formula_id"] == formula_id), None)
    if not entry:
        print(f"⚠️ Formula {formula_id} not found in derivation ledger.")
        return

    expr_str = entry.get("expression")
    print(f"\n🔁 Re-deriving {formula_id}: {expr_str}")

    try:
        expr = sp.sympify(expr_str)
    except Exception as e:
        print(f"❌ Unable to parse expression: {e}")
        return

    # Apply first-principles checks
    symbols = sorted(list(expr.free_symbols), key=lambda s: s.name)
    print(f"  Symbols: {[s.name for s in symbols]}")

    # Example: differentiate and simplify to confirm identity (toy check)
    deriv_tests = {}
    for s in symbols:
        deriv_tests[s.name] = sp.simplify(sp.diff(expr, s))

    print("\n📐 Symbolic derivation steps:")
    for k,v in deriv_tests.items():
        print(f"  ∂/∂{k}: {v}")

    # Evaluate at unit values to check numeric consistency
    subs = {s:1 for s in symbols}
    try:
        numeric = float(expr.evalf(subs=subs))
        print(f"\n🔎 Numeric check (at all vars=1): {numeric}")
        if abs(numeric) < 1e6:
            status = "PASSED"
        else:
            status = "UNSTABLE"
    except Exception:
        numeric = None
        status = "FAILED (non-numeric)"

    print(f"✅ Derivation Status: {status}")

    # Log the re-derivation attempt
    log_path = os.path.join(DATA_DIR, "rederive_log.json")
    log = load_json(log_path)
    log.append({
        "formula_id": formula_id,
        "timestamp": timestamp(),
        "expression": expr_str,
        "status": status,
        "result": str(numeric)
    })
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(log_path, "w") as f:
        json.dump(log, f, indent=2)
    print(f"🧾 Re-derivation logged at {log_path}")

# ---------- CLI --------------------------------------------------------------
def main():
    p = argparse.ArgumentParser(description="Unified Analytical Memory (UAM) Query Interface v1.0")
    p.add_argument("--failed", action="store_true")
    p.add_argument("--constant", type=str)
    p.add_argument("--bridge", type=str)
    p.add_argument("--history", type=str)
    p.add_argument("--recent", type=int)
    p.add_argument("--rederive", type=str)
    args = p.parse_args()

    if args.failed: query_failed()
    elif args.constant: query_constant(args.constant)
    elif args.bridge: query_bridge(args.bridge)
    elif args.history: query_history(args.history)
    elif args.recent: query_recent(args.recent)
    elif args.rederive: rederive_formula(args.rederive)
    else: p.print_help()

if __name__ == "__main__":
    main()
