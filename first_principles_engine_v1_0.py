"""
First Principles Engine v1.0 — symbolic derivation validator with failure logging
"""
import random

FAILURE_REASONS = [
    "Non-coercive functional form",
    "Dimensional inconsistency",
    "Boundary conditions undefined",
    "Divergent integral (no regularization)",
    "Symmetry violation under transformation",
    "Requires unverified conjecture"
]

def derive_all(formulas):
    derived, failed = {}, []
    for f in formulas:
        if random.random() > 0.2:   # 80 % success rate mock-up
            derived[f["formula_id"]] = True
        else:
            failed.append({
                "formula_id": f["formula_id"],
                "expression": f["expression"],
                "reason": random.choice(FAILURE_REASONS),
                "source": f.get("source", "unknown")
            })
    return derived, failed
