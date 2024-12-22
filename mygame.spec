# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=['C:/Users/79520/Desktop/Doodle_Jump_yandexlyceum'],
    binaries=[],
    datas=[('data/button.png', 'data'), ('data/data_us', 'data'), ('data/Doodlemusic.mp3', 'data'), ('data/doodler.png', 'data'), ('data/doodler1.png', 'data'), ('data/F.gif', 'data'), ('data/fon.jpg', 'data'), ('data/fon2.jpg', 'data'), ('data/Fonfutboll.jpg', 'data'), ('data/game over-PhotoRoom.png-PhotoRoom.png', 'data'), ('data/hahahhahahahahhhh.png', 'data'), ('data/lose.mp3', 'data'), ('data/SnowFon.jpg', 'data'), ('data/spring.png', 'data'), ('data/SUBWAY SURFERS.mp3', 'data'), ('data/user.txt', 'data'), ('data/Платформа.jpg', 'data'), ('data/Платформа.png', 'data'), ('data/Платформа1.png', 'data')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='DoodleJump',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
