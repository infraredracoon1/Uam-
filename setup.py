#!/usr/bin/env python3
# ============================================================
#  setup.py — UAM Framework Installation Script
#  Unified Analytical Memory (UAM)
#  © 2025 Anthony Abney. All Rights Reserved.
#  Proprietary / Immutable Authorship License v1.0
#  Trademark: UAM Stamp™
# ============================================================

from setuptools import setup, find_packages

setup(
    name="uam",
    version="1.0.0",
    author="Anthony Abney",
    author_email="anthony.abney@protonmail.com",  # optional placeholder
    description="Unified Analytical Memory (UAM): analytical PDE/QFT research engine suite.",
    long_description=open("README.md").read() if __file__ else "",
    long_description_content_type="text/markdown",
    license="Proprietary / Immutable Authorship License v1.0",
    packages=find_packages(exclude=("tests", "docs")),
    python_requires=">=3.9",
    install_requires=[
        "numpy>=1.21.0",
        "scipy>=1.8.0",
        "sympy>=1.10",
        "requests",
        "pandas",
        "matplotlib",
        "tqdm",
        "beautifulsoup4",   # for dataset crawling
        "lxml",
    ],
    entry_points={
        "console_scripts": [
            "uam_sweep=uam_sweep:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Proprietary",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
    include_package_data=True,
)
