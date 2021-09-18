# -*- mode: python ; coding: utf-8 -*-
# type: ignore

from packaging.version import parse as version_parse
from PyInstaller.utils.hooks import collect_all
from PyInstaller.utils.win32.versioninfo import (
    FixedFileInfo,
    StringFileInfo,
    StringStruct,
    StringTable,
    VarFileInfo,
    VarStruct,
    VSVersionInfo,
)

from msfs_screenshot_geotag import __app_name__, __author__, __version__

PACKAGE_NAME = "msfs_screenshot_geotag"


# ---- Windows version info ----

version = version_parse(__version__)
version_tuple = (version.major, version.minor, version.micro, 0)

windows_version_info = VSVersionInfo(
    ffi=FixedFileInfo(
        # filevers and prodvers should be always a tuple with four items: (1, 2, 3, 4)
        # Set not needed items to zero 0.
        filevers=version_tuple,
        prodvers=version_tuple,
        # Contains a bitmask that specifies the valid bits 'flags'r
        mask=0x3F,
        # Contains a bitmask that specifies the Boolean attributes of the file.
        flags=0x0,
        # The operating system for which this file was designed.
        # 0x4 - NT and there is no need to change it.
        OS=0x4,
        # The general type of file.
        # 0x1 - the file is an application.
        fileType=0x1,
        # The function of the file.
        # 0x0 - the function is not defined for this fileType
        subtype=0x0,
        # Creation date and time stamp.
        date=(0, 0),
    ),
    kids=[
        StringFileInfo(
            [
                StringTable(
                    "040904B0",
                    [
                        StringStruct("CompanyName", f"{__author__}"),
                        StringStruct("FileDescription", f"{__app_name__}"),
                        StringStruct("FileVersion", f"{__version__}"),
                        StringStruct("InternalName", f"{__app_name__}"),
                        StringStruct("LegalCopyright", f"Copyright (c) {__author__}"),
                        StringStruct("OriginalFilename", f"{__app_name__}.exe"),
                        StringStruct("ProductName", f"{__app_name__}"),
                        StringStruct("ProductVersion", f"{__version__}"),
                    ],
                )
            ]
        ),
        VarFileInfo([VarStruct("Translation", [1033, 1200])]),
    ],
)


# ---- Bundled binaries, datas, and forced packages ----

binaries = [
    (f"{PACKAGE_NAME}\\_bin", "_bin"),
]
datas = [
    (f"{PACKAGE_NAME}\\_resources", "_resources"),
]
hiddenimports = []
tmp_ret = collect_all("tzdata")
datas += tmp_ret[0]
binaries += tmp_ret[1]
hiddenimports += tmp_ret[2]
tmp_ret = collect_all("pyqtkeybind")
datas += tmp_ret[0]
binaries += tmp_ret[1]
hiddenimports += tmp_ret[2]
tmp_ret = collect_all("SimConnect")
datas += tmp_ret[0]
binaries += tmp_ret[1]
hiddenimports += tmp_ret[2]


block_cipher = None

# ---- Main spec definitions ----

a = Analysis(
    [f"{PACKAGE_NAME}\\__main__.py"],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name=__app_name__,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version=windows_version_info,
    icon=f"{PACKAGE_NAME}\\_resources\\main.ico",
)
