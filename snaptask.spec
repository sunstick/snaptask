# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec file for SnapTask
# This bundles all Python dependencies and PyObjC frameworks into a single binary

block_cipher = None

a = Analysis(
    ['snaptask_cli.py', 'snaptask.py', 'snaptask_vision.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        # PyObjC frameworks (required for macOS Vision and screen capture)
        'Vision',
        'Quartz',
        'objc',
        'Foundation',
        'CoreGraphics',
        'AppKit',
        # OpenAI API
        'openai',
        'openai.types',
        'openai.types.chat',
        # Standard library modules that might not be auto-detected
        'json',
        'base64',
        'subprocess',
        'os',
        'datetime',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='snaptask',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # Compress the binary (optional, can be disabled for faster builds)
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # CLI tool, needs console output
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
