#!/usr/bin/env python3
"""
UAM Query Interface v1.0
Command: uam query [options]

Examples:
  uam query --failed
  uam query --constant C_S
  uam query --bridge YangMills
  uam query --history formula-107
  uam query --recent 5
"""

import json, argparse, os, datetime
DATA_DIR = "data"

def load_json(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def query_failed():
    data = load_json(os.path.join(DATA_DIR, "derivation_ledger.json"))
    if not data:
        print("✅ No recorded derivation failures.")
        return
    print(f"📘 {len(data)} failed derivations logged:")
    for entry in data[-10:]:  # last 10
        print(f"\n• ID: {entry['formula_id']}")
        print(f"  Expression: {entry['expression']}")
        print(f"  Reason: {entry['reason']}")
        print(f"  Timestamp: {entry['timestamp']}")
        print(f"  Source: {entry.get('source','unknown')}")

def query_constant(name):
    data = load_json(os.path.join(DATA_DIR, "constants_db.json"))
    found = [c for c in data if c.get("name") == name]
    if not found:
        print(f"⚠️ Constant {name} not found in database.")
        return
    for c in found:
        print(f"🔢 Constant: {c['name']}")
        print(f"  Value: {c['value']}")
        print(f"  Derived from: {c['derivation']}")
        print(f"  Scale: {c.get('scale', 'unspecified')}")
        print(f"  Source: {c.get('source', 'UAM')}")
        print(f"  Verified: {c.get('verified', False)}")

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
        print(f"  Constants: {b.get('constants', 'N/A')}")

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

def main():
    parser = argparse.ArgumentParser(description="Unified Analytical Memory (UAM) Query Interface v1.0")
    parser.add_argument("--failed", action="store_true", help="Show latest derivation failures")
    parser.add_argument("--constant", type=str, help="Query a constant by name")
    parser.add_argument("--bridge", type=str, help="Search for a tensor bridge by keyword")
    parser.add_argument("--history", type=str, help="Show derivation history for a formula ID")
    parser.add_argument("--recent", type=int, help="Show recent UAM upgrades (default=5)")
    args = parser.parse_args()

    if args.failed:
        query_failed()
    elif args.constant:
        query_constant(args.constant)
    elif args.bridge:
        query_bridge(args.bridge)
    elif args.history:
        query_history(args.history)
    elif args.recent:
        query_recent(args.recent)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
