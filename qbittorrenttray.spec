# -*- mode: python -*-

block_cipher = None


a = Analysis(['Code/qbittorrenttray.py'],
             pathex=['/home/terje/Documents/personal/qBittorrentTray-debian/'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
a.datas += [('qbdark_big.png','/home/terje/Documents/personal/qBittorrentTray-debian/Resources/qbdark_big.png', "DATA"),
            ('qbdark_dc_big.png','/home/terje/Documents/personal/qBittorrentTray-debian/Resources/qbdark_dc_big.png', "DATA"),
            ('qbdark_pause_big.png','/home/terje/Documents/personal/qBittorrentTray-debian/Resources/qbdark_pause_big.png', "DATA"),
            ('qbdark.ico','/home/terje/Documents/personal/qBittorrentTray-debian/Resources/qbdark.ico', "DATA")]
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='qbittorrenttray',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
