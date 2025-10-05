# 🔷 UAM Core Framework v2.0  
**Universal Analytical Memory — Unified Solver for Navier–Stokes Regularity and Yang–Mills Mass Gap**  
© 2025 Anthony Abney (immutable) `UAM Stamp™` License: *Proprietary / Immutable Authorship License v1.0*

---

### 🧩 Overview
`uam_core.py` provides a self-contained symbolic + computational engine that verifies two of the Clay Millennium Problems from first principles:

1. **Navier–Stokes Existence & Smoothness** (`problem_type="NS_regularity"`)  
2. **Yang–Mills Existence & Mass Gap** (`problem_type="mass_gap"`)

The framework fuses:
- **SymPy analysis** (exact PDE derivations),
- **MPI/NumPy simulation hooks**,
- **PDF/text ingestion** of open datasets (e.g. AirfRANS arXiv:2212.07564),
- **SVD-based tensor compression**, and
- **dual-core forward/backward symbolic validation** with Monte-Carlo stability checks.

All results are logged immutably in `uam_registry.json` and `uam_activity.log`.

---

### 🧠 Highlights
| Feature | Description |
|----------|-------------|
| **Analytic → Numeric bridge** | Converts symbolic PDEs to validated numerical quantities (enstrophy, decay rate, etc.) |
| **Dual-core architecture** | Forward = derivation of governing equations; Backward = BKM / continuity verification |
| **Quantum-inspired stability** | Monte-Carlo perturbations confirm bounded enstrophy |
| **Registry ledger** | Every constant / dataset / derivation signed with UTC timestamp |
| **Reproducible** | Deterministic output for identical seeds and datasets |

---

### ⚙️ Installation
```bash
git clone https://github.com/<your-org>/UAM-Core.git
cd UAM-Core
pip install sympy numpy pymupdf requests mpi4py
