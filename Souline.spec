# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

# Uygulama simgesi: pencere ve tepsi icin exe'nin icine gomulur
datas = [('assets/souline.ico', 'assets'), ('assets/souline.png', 'assets')]
binaries = []
hiddenimports = ['pystray._win32']
tmp_ret = collect_all('pyatv')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('soundcard')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('zeroconf')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
# Windows 11 temasi (Sun Valley) tcl dosyalariyla gelir
tmp_ret = collect_all('sv_ttk')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['souline_app.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    # Gelistirme araclari uygulamaya girmesin (pydantic'in istege bagli mypy eklentisi bunlari cekiyordu)
    excludes=['mypy', 'mypyc', 'pydantic.mypy'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

# Klasor modu (onedir): tek islem, her acilista gecici klasore acilma yok.
# Tek dosya modunda kapanirken baslatici exe'yi bir sure kilitli tutuyor ve
# kaldirma "bazi bilesenler kaldirilamadi" diyordu.
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Souline',
    version='assets/version_info.txt',
    icon='assets/souline.ico',
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
    name='Souline',
)
