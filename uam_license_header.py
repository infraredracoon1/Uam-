#!/usr/bin/env python3
# ============================================================
#  UAM LICENSE HEADER v1.0
#  Unified Analytical Memory (UAM) — Authorship & Licensing
#  © 2025 Anthony Abney.  All Rights Reserved.
#  Proprietary / Immutable Authorship License v1.0
#  Trademark: UAM Stamp™
# ============================================================

"""
uam_license_header.py
---------------------
Shared immutable license header for all UAM modules.

Usage:
    from uam_license_header import UAM_INFO, print_header, stamp_metadata
"""

import datetime, platform, getpass

# ------------------------------------------------------------
UAM_INFO = {
    "framework": "Unified Analytical Memory (UAM)",
    "version": "1.0",
    "author": "Anthony Abney (immutable)",
    "contributors": [
        "Cody Jackson Abney (immutable)",
        "Ava Serenity Abney (immutable)",
        "Trevor Abney (immutable)"
    ],
    "trademark": "UAM Stamp™",
    "license": "Proprietary / Immutable Authorship License v1.0",
    "year": 2025,
    "rights": "All rights reserved.",
    "purpose": (
        "Provides immutable authorship and provenance stamping "
        "for every UAM analytical or computational module."
    ),
    "legal": (
        "Unauthorized use, modification, or redistribution is prohibited "
        "without written permission from the author. All UAM modules "
        "must retain this header verbatim."
    ),
}

# ------------------------------------------------------------
def print_header(module_name: str = None):
    """Display the standard header for any UAM module."""
    print("============================================================")
    print(f"🔷 {UAM_INFO['framework']} — Version {UAM_INFO['version']}")
    if module_name:
        print(f"📘 Module: {module_name}")
    print(f"👤 Author: {UAM_INFO['author']}")
    print(f"™ Trademark: {UAM_INFO['trademark']}")
    print(f"📜 License: {UAM_INFO['license']}")
    print(f"📅 Date: {datetime.datetime.utcnow().isoformat()} UTC")
    print(f"💻 Host: {platform.node()}  |  User: {getpass.getuser()}")
    print("============================================================")

# ------------------------------------------------------------
def stamp_metadata(module_dict: dict):
    """
    Add license and authorship metadata into a module’s global dictionary.
    Example:
        import sys
        stamp_metadata(sys.modules[__name__].__dict__)
    """
    module_dict.update({
        "__uam_framework__": UAM_INFO["framework"],
        "__uam_version__": UAM_INFO["version"],
        "__uam_author__": UAM_INFO["author"],
        "__uam_trademark__": UAM_INFO["trademark"],
        "__uam_license__": UAM_INFO["license"],
        "__uam_timestamp__": datetime.datetime.utcnow().isoformat(),
    })

# ------------------------------------------------------------
if __name__ == "__main__":
    print_header("uam_license_header")
