# -*- mode: python -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['Z:\\Desktop\\lvq-network'],
             binaries=[],
             datas=[('config.txt', '.'), ('data_train.txt', '.'), ('data_vc.txt', '.'), ('data_test.txt', '.')],
             hiddenimports=['cmean', 'system', 'branch', 'calculator','network', 'logger', 'representative', 'utility'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
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
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='main')
