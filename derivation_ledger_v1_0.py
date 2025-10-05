"""
Derivation Ledger v1.0 — records failure reasons and provenance
"""
import json, os

LEDGER_FILE = "data/derivation_ledger.json"

def log_failures(failed, timestamp):
    if not failed: 
        return
    entries = []
    for f in failed:
        entries.append({
            "formula_id": f["formula_id"],
            "expression": f["expression"],
            "reason": f["reason"],
            "source": f.get("source", "UAM_research_engine"),
            "timestamp": timestamp
        })
    os.makedirs("data", exist_ok=True)
    try:
        old = json.load(open(LEDGER_FILE))
    except FileNotFoundError:
        old = []
    old.extend(entries)
    with open(LEDGER_FILE, "w") as f:
        json.dump(old, f, indent=2)
    with open("data/derivation_failures.json", "w") as f:
        json.dump(entries, f, indent=2)
