# -*- mode: python ; coding: utf-8 -*-

import os
from pathlib import Path

import customtkinter

# Determine the current directory dynamically based on the location of this .spec file
CURRENT_DIR = Path(os.path.abspath(os.path.dirname(__name__))) / "src"

# Add data files using the relative file path to the spec file
data_files = [
    # (source, destination in the bundle)
    ("logging_config.py"), "."),
    ("mongo.py"), "."),
    ("security.py"), "."),
    (str(Path(customtkinter.__file__).parent), "customtkinter/"),
]

a = Analysis(
    ['app.py'],
    pathex=[str(CURRENT_DIR)],
    binaries=[],
    datas=data_files,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='collections_app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='collections_app',
)
