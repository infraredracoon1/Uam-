# ============================================================
#  Makefile — Unified Analytical Memory (UAM)
#  Version 1.0 — by Anthony Abney
# ============================================================

PYTHON = python3

.PHONY: install clean sweep upgrade test build publish

install:
	@echo "📦 Installing UAM framework..."
	$(PYTHON) setup.py install

clean:
	@echo "🧹 Cleaning build artifacts..."
	rm -rf build dist *.egg-info __pycache__ */__pycache__ logs

sweep:
	@echo "🚀 Running full UAM sweep..."
	$(PYTHON) -m uam_sweep --parallel --upgrade

upgrade:
	@echo "🔁 Running upgrade of datasets and constants..."
	$(PYTHON) -m uam_sweep --upgrade

test:
	@echo "🧪 Running internal tests..."
	$(PYTHON) -m unittest discover -s tests

build:
	@echo "📦 Building distributable wheel..."
	$(PYTHON) -m build

publish:
	@echo "🚀 Publishing (manual step for Proprietary License)..."
	@echo "✅  Push to private GitHub or internal registry."
