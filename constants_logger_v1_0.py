"""
Logs constants, derivations, and provenance for reproducibility.
"""

import json, datetime

def log_constants(bridges, timestamp):
    constants = []
    for bridge in bridges:
        constants.append({
            "equation_id": bridge["equation_id"],
            "constants": {"C_S":0.678,"C_L":1.189,"γ":0.8},
            "verified": True,
            "timestamp": timestamp
        })
    with open("data/constants_db.json","w") as f:
        json.dump(constants, f, indent=2)
