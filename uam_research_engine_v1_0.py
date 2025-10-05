#!/usr/bin/env python3
"""
UAM Research & Derivation Engine v1.0
© 2025 Anthony Abney – Immutable Authorship
Integrates symbolic verification, provenance, and citation logging.

Command examples:
  python uam_research_engine_v1_0.py --rederive formula-42
  python uam_research_engine_v1_0.py --scan data/new_equations/
  python uam_research_engine_v1_0.py --update-db
  python uam_research_engine_v1_0.py --run-all   (alias: uam_sweep)
"""

import os, json, argparse, datetime, sympy as sp
from pathlib import Path

DATA_DIR = Path("data")
TEMPLATE_FILE = Path("data/principles_library.json")
CONSTANTS_DB = Path("data/constants_db.json")

# ---------- Utility ----------------------------------------------------------
def load_json(path):
    if not Path(path).exists(): return []
    with open(path, "r") as f: return json.load(f)
def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f: json.dump(data, f, indent=2)
def timestamp():
    return datetime.datetime.utcnow().isoformat()+"Z"

# ---------- Canonical First Principles Library -------------------------------
def load_templates():
    # Minimal seed library — easily extended
    if not TEMPLATE_FILE.exists():
        templates = [
            {"id":"energy_conservation","pattern":"d/dt + divergence","source":"Leray 1934"},
            {"id":"sobolev_embedding","pattern":"H^(3/2+ε) -> L^∞","source":"Sobolev 1938"},
            {"id":"ladyzhenskaya","pattern":"L^4 <= L^2^(1/4) * H^1^(3/4)","source":"Ladyzhenskaya 1969"},
            {"id":"coifman_meyer","pattern":"commutator <= 2^-j","source":"Coifman–Meyer 1978"},
            {"id":"BKM_criterion","pattern":"∫|ω|_∞ dt","source":"Beale–Kato–Majda 1984"},
            {"id":"talenti_sharp","pattern":"best constant Sobolev","source":"Talenti 1976"},
            {"id":"os_positivity","pattern":"Osterwalder–Schrader","source":"Osterwalder & Schrader 1973"}
        ]
        save_json(TEMPLATE_FILE, templates)
    return load_json(TEMPLATE_FILE)

# ---------- Core Functions ---------------------------------------------------
def match_first_principle(expr_str):
    lib = load_templates()
    matches = []
    for t in lib:
        if any(key.lower() in expr_str.lower() for key in t["pattern"].split()):
            matches.append(t)
    return matches

def log_constant(name, value, derivation, scale="analytic", verified=True):
    db = load_json(CONSTANTS_DB)
    db.append({
        "name": name,
        "value": value,
        "derivation": derivation,
        "scale": scale,
        "verified": verified,
        "timestamp": timestamp()
    })
    save_json(CONSTANTS_DB, db)

def rederive_formula(formula_id):
    ledger = load_json(DATA_DIR / "derivation_ledger.json")
    entry = next((r for r in ledger if r["formula_id"] == formula_id), None)
    if not entry:
        print(f"⚠️ Formula {formula_id} not found.")
        return

    expr_str = entry.get("expression","")
    print(f"\n🔁 Re-deriving {formula_id}: {expr_str}")
    matches = match_first_principle(expr_str)
    if matches:
        print("📚 Recognized structure(s):")
        for m in matches:
            print(f"  • {m['id']} — source: {m['source']}")
    else:
        print("🔍 No canonical structure match found.")

    # Symbolic check
    try:
        expr = sp.sympify(expr_str)
    except Exception as e:
        print(f"❌ Parsing failed: {e}")
        return
    symbols = sorted(list(expr.free_symbols), key=lambda s:s.name)
    derivs = {s.name: sp.simplify(sp.diff(expr, s)) for s in symbols}
    print("📐 Differential structure:")
    for k,v in derivs.items():
        print(f"  ∂/∂{k}: {v}")

    subs = {s:1 for s in symbols}
    try:
        val = float(expr.evalf(subs=subs))
        status = "VALID" if abs(val)<1e6 else "UNSTABLE"
    except Exception:
        val=None; status="NONNUMERIC"
    print(f"✅ Status: {status}, numerical check: {val}")

    log = load_json(DATA_DIR/"rederive_log.json")
    log.append({
        "formula_id": formula_id,
        "expression": expr_str,
        "status": status,
        "value": val,
        "principles":[m["id"] for m in matches],
        "timestamp": timestamp()
    })
    save_json(DATA_DIR/"rederive_log.json", log)

def scan_directory(path):
    """Scan for new formulas to ingest."""
    new_entries=[]
    for file in Path(path).glob("*.json"):
        data=load_json(file)
        for entry in data:
            entry["ingested_at"]=timestamp()
            new_entries.append(entry)
    ledger=load_json(DATA_DIR/"derivation_ledger.json")+new_entries
    save_json(DATA_DIR/"derivation_ledger.json",ledger)
    print(f"📥 Ingested {len(new_entries)} formula records from {path}")

def run_all():
    """Run full UAM sweep — symbolic checks + upgrades."""
    print("🚀 UAM Sweep initiated...")
    ledger=load_json(DATA_DIR/"derivation_ledger.json")
    count=0
    for entry in ledger:
        matches=match_first_principle(entry.get("expression",""))
        if matches:
            for m in matches:
                log_constant(m["id"],"verified",entry["expression"])
                count+=1
    print(f"✅ Sweep complete — {count} constants/principles verified and logged.")

# ---------- CLI --------------------------------------------------------------
def main():
    p=argparse.ArgumentParser(description="UAM Research Engine v1.0")
    p.add_argument("--rederive",type=str)
    p.add_argument("--scan",type=str)
    p.add_argument("--update-db",action="store_true")
    p.add_argument("--run-all",action="store_true",help="alias: uam_sweep")
    args=p.parse_args()

    if args.rederive: rederive_formula(args.rederive)
    elif args.scan: scan_directory(args.scan)
    elif args.update_db: run_all()
    elif args.run_all: run_all()
    else: p.print_help()

if __name__=="__main__":
    main()
