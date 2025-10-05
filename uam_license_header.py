# ============================================================
#  UAM LICENSE HEADER v1.0
#  © 2025 Anthony Abney.  All Rights Reserved.
#  Trademark: UAM Stamp™
#  Proprietary / Immutable Authorship License v1.0
# ============================================================

UAM_LICENSE = {
    "framework": "Unified Analytical Memory (UAM)",
    "version": "1.0",
    "owner": "Anthony Abney",
    "authors": [
        "Anthony Abney (immutable)",
        "Cody Jackson Abney (immutable)",
        "Ava Serenity Abney (immutable)",
        "Trevor Abney (immutable)"
    ],
    "license": {
        "type": "Proprietary / Immutable Authorship",
        "terms": (
            "Use, reproduction, or distribution of any portion of this code "
            "without explicit written permission of the owner is strictly prohibited. "
            "Derived works must include full attribution and may not remove or modify "
            "the immutable authorship identifiers."
        )
    },
    "trademark": "UAM Stamp™",
    "contact": "contact@uam-labs.org (placeholder — for legal record only)",
    "integrity_hash": "UAM2025-IMMUTABLE-STAMP",
    "notes": [
        "All analytical engines (research, tensor core, sweep) import this header.",
        "Ensures authorship, version control, and reproducibility of constants.",
        "Modifications allowed only under stronger analytical proofs per UAM rules."
    ]
}

def print_license_info():
    """Display UAM license summary."""
    print("============================================================")
    print(" Unified Analytical Memory (UAM) — Immutable License v1.0")
    print(" © 2025 Anthony Abney. All Rights Reserved.")
    print(" Trademark: UAM Stamp™")
    print("============================================================")
    print(f" Framework Version : {UAM_LICENSE['version']}")
    print(f" Owner             : {UAM_LICENSE['owner']}")
    print(f" License Type      : {UAM_LICENSE['license']['type']}")
    print("------------------------------------------------------------")
    print(" Terms:")
    print("  ", UAM_LICENSE['license']['terms'])
    print("============================================================")

if __name__ == "__main__":
    print_license_info()
