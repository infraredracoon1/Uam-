#!/usr/bin/env python3
"""
UAM Core v3.0 — Abney Self-Contained Installer/Launcher
Anthony Abney © 2025 — All Rights Reserved
"""

import os, sys, subprocess, pathlib, zipapp, shutil

root = pathlib.Path("UAM_Core_v3_0_Abney_Full")
lib  = root / "uam_lib"
dirs = [
    "uam_modules", "uam_data", "uam_db", "uam_docs",
    "uam_proofs", "uam_config", "uam_launcher", "logs"
]

# ────────────────────────────────────────────────────────────────
# 1. Create structure without touching existing data
# ────────────────────────────────────────────────────────────────
def mkdirs():
    print("📁  Preparing directories…")
    root.mkdir(exist_ok=True)
    for d in dirs:
        p = root / d
        if not p.exists():
            p.mkdir(parents=True)
        elif d in ("uam_data", "uam_db"):
            ans = input(f"⚠️  Existing {d} detected. Keep it? [Y/n] ").strip().lower()
            if ans in ("n","no"):
                shutil.rmtree(p)
                p.mkdir()
                print(f"🗑️  Reinitialized {d}")
            else:
                print(f"✅  Keeping existing {d}")

# ────────────────────────────────────────────────────────────────
# 2. Download dependencies once for offline reuse
# ────────────────────────────────────────────────────────────────
def download_wheels():
    print("📦  Collecting dependencies (offline-ready)…")
    lib.mkdir(exist_ok=True)
    pkgs = [
        "numpy", "sympy", "sqlalchemy", "pyqt5",
        "h5py", "scikit-learn", "requests", "better-profanity"
    ]
    subprocess.run([sys.executable, "-m", "pip", "download",
                    "--only-binary=:all:", "-d", str(lib)] + pkgs, check=True)

# ────────────────────────────────────────────────────────────────
# 3. Create the internal launcher scripts
# ────────────────────────────────────────────────────────────────
def write_launcher_files():
    print("🧩  Writing launcher scripts…")

    (root/"uam_launcher/install_env.py").write_text(
        "import subprocess,sys,pathlib\n"
        "LIB=pathlib.Path(__file__).parent.parent/'uam_lib'\n"
        "print('[UAM] Installing dependencies...')\n"
        "for whl in LIB.glob('*.whl'):\n"
        " subprocess.run([sys.executable,'-m','pip','install','--no-index',"
        "'--find-links',str(LIB),str(whl)],stdout=subprocess.DEVNULL)\n"
        "print('[UAM] Dependencies installed.')\n"
    )

    (root/"uam_launcher/sync_db.py").write_text(
        "import sqlite3,datetime,pathlib\n"
        "DB=pathlib.Path(__file__).parent.parent/'uam_db'/'uam_knowledge.db'\n"
        "print('[UAM] Checking databases...')\n"
        "conn=sqlite3.connect(DB)\n"
        "c=conn.cursor()\n"
        "c.execute('CREATE TABLE IF NOT EXISTS meta(key TEXT,value TEXT)')\n"
        "c.execute('INSERT OR REPLACE INTO meta VALUES(?,?)',"
        "('last_sync',datetime.datetime.now().isoformat()))\n"
        "conn.commit();conn.close()\n"
        "print('[UAM] Database ready.')\n"
    )

    (root/"uam_launcher/launch_gui.py").write_text(
        "from PyQt5 import QtWidgets,QtGui\n"
        "import sys\n"
        "app=QtWidgets.QApplication(sys.argv)\n"
        "app.setStyle('Fusion')\n"
        "pal=app.palette();pal.setColor(QtGui.QPalette.Window,QtGui.QColor(30,30,30));"
        "pal.setColor(QtGui.QPalette.WindowText,QtGui.QColor(240,240,240));"
        "app.setPalette(pal)\n"
        "w=QtWidgets.QWidget();w.setWindowTitle('UAM Core v3.0 — Dark Edition')\n"
        "layout=QtWidgets.QVBoxLayout(w)\n"
        "msg=QtWidgets.QLabel('🌑 UAM Core v3.0 Abney Edition is running.');"
        "msg.setStyleSheet('font-size:18px;color:white;')\n"
        "layout.addWidget(msg)\n"
        "btn=QtWidgets.QPushButton('Close');btn.clicked.connect(app.quit);layout.addWidget(btn)\n"
        "w.resize(420,160);w.show();sys.exit(app.exec_())\n"
    )

    (root/"__main__.py").write_text(
        "import subprocess,sys,pathlib\n"
        "root=pathlib.Path(__file__).parent\n"
        "print('🔧 Booting UAM Core v3.0 (Abney Edition)')\n"
        "subprocess.run([sys.executable,str(root/'uam_launcher/install_env.py')])\n"
        "subprocess.run([sys.executable,str(root/'uam_launcher/sync_db.py')])\n"
        "subprocess.run([sys.executable,str(root/'uam_launcher/launch_gui.py')])\n"
    )

# ────────────────────────────────────────────────────────────────
# 4. Package everything into uam_core_v3_0.pyz
# ────────────────────────────────────────────────────────────────
def build_zipapp():
    print("🧱 Packaging to uam_core_v3_0.pyz…")
    out = pathlib.Path("uam_core_v3_0.pyz")
    if out.exists():
        out.unlink()
    zipapp.create_archive(root, target=out, interpreter="/usr/bin/env python3")
    print(f"✅ Created {out.resolve()}")

# ────────────────────────────────────────────────────────────────
def main():
    mkdirs()
    download_wheels()
    write_launcher_files()
    build_zipapp()
    print("\n🎉 Build complete!")
    print("To run: python uam_core_v3_0.pyz\n")

if __name__ == "__main__":
    main()
