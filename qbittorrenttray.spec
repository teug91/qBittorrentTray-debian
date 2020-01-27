# -*- mode: python -*-

block_cipher = None

a = Analysis(
    ["qbittorrenttray/qbittorrenttray.py"],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

a.datas += [
    (
        "qbdark_big.png",
        "qbittorrenttray/resources/qbdark_big.png",
        "DATA",
    ),
    (
        "qbdark_dc_big.png",
        "qbittorrenttray/resources/qbdark_dc_big.png",
        "DATA",
    ),
    (
        "qbdark_pause_big.png",
        "qbittorrenttray/resources/qbdark_pause_big.png",
        "DATA",
    ),
]

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name="qbittorrenttray",
    debug=False,
    strip=False,
    upx=True,
    runtime_tmpdir=None,
    console=True,
)
