# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['welcome_screen.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets/blueprints/easy.png', 'assets/blueprints'),
        ('assets/blueprints/medium.png', 'assets/blueprints'),
        ('assets/blueprints/hard.png', 'assets/blueprints')
        ],
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
    name='SpacecraftSimulator',
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
    icon=['icon.icns'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='SpacecraftSimulator',
)
app = BUNDLE(
    coll,
    name='SpacecraftSimulator.app',
    icon='icon.icns',
    bundle_identifier=None,
)
