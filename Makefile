# ============================================================
#  UAM Framework Build / Run Commands (v1.0)
# ============================================================

.PHONY: install upgrade sweep parallel clean

install:
\tpython3 setup.py install

upgrade:
\tpython3 uam_sweep.py --upgrade

sweep:
\tpython3 uam_sweep.py

parallel:
\tpython3 uam_sweep.py --parallel

clean:
\trm -rf build dist *.egg-info __pycache__
\tfind . -name "__pycache__" -type d -exec rm -rf {} +
