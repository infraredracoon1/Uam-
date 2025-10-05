from setuptools import setup, find_packages

setup(
    name="UAM_Framework",
    version="1.0",
    author="Anthony Abney",
    author_email="contact@uam.local",
    description="Unified Analytical Memory (UAM) analytical framework v1.0",
    packages=find_packages(),
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "uam_sweep=uam_sweep:uam_sweep",
        ],
    },
    license="Proprietary / Immutable Authorship License v1.0",
)
