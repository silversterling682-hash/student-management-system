# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('app.py', '.'),
        ('start_server.py', '.'),
        ('index.html', '.'),
        ('style.css', '.'),
        ('script.js', '.'),
        ('students_database.json', '.'),
        ('README.md', '.'),
        ('LICENSE', '.'),
        ('logo.svg', '.'),
    ],
    hiddenimports=[
        'flask',
        'flask_cors',
        'json',
        'datetime',
        'uuid',
        'os',
        'sys',
        'threading',
        'time',
        'webbrowser'
        'request'
    ],
    hookspath=[],
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
    [],
    exclude_binaries=True,
    name='Student-Management-System',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # ❌ Hides the black terminal window completely
    icon=None       # We can add a nice icon later if you want!
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Student-Management-System'
)