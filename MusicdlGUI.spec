# -*- mode: python ; coding: utf-8 -*-
block_cipher = None

# Add the current directory to the path
import sys
import os
sys.setrecursionlimit(5000)  # Increase recursion limit

a = Analysis(
    ['MusicdlGUI.py'],
    pathex=[os.getcwd()],  # Add current working directory to path
    binaries=[],
    datas=[
        ('toilet_window_icon_pink.ico', '.'),
        ('ffmpeg.exe', '.'),
        ('Toilet_App_Icon_pink.ico', '.')
    ],
    hiddenimports=[
        'yt_dlp',
        'certifi',
        'urllib3',
        'requests'
    ],
    hookspath=[],
    hooksconfig={},
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Collect all yt-dlp data
for d in a.datas:
    if 'yt_dlp' in d[0]:
        a.datas.remove(d)

import yt_dlp
a.datas += Tree(yt_dlp.__path__[0], prefix='yt_dlp')

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='MusicdlGUI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to False for windowed application
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='Toilet_App_Icon_pink.ico',
)