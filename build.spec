# -*- mode: python ; coding: utf-8 -*-
import os
import sys

block_cipher = None


def get_modules(module_dir):
    import os
    import pkgutil
    return [f"{module_dir.replace('/', '.')}.{name}"
            for path_finder, name, __ in pkgutil.iter_modules([os.path.relpath(module_dir, os.getcwd())])]


hiddenimports = get_modules("sunrise/engines")
hiddenimports += get_modules("sunrise/basic_plugins")
hiddenimports += get_modules("sunrise/filter")

current_dir = os.path.abspath('')

a = Analysis(['run.py'],
             pathex=[r'D:\Nattsu_python\gongkaisai_client'],
             binaries=[],
             datas=[('./file', 'file'), ('./plugins', 'plugins'), ('./dll', 'dll'), (".env", ".")],
             hiddenimports=hiddenimports,
             hookspath=[],
             runtime_hooks=[],
             excludes=['tkinter'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data,
          cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='sunrise',
          icon=os.path.join(os.getcwd(), "logo.ico"),
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          uac_admin=False)
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='sunrise')
