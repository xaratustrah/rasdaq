# !/usr/bin/env python
"""
A client/server code for Raspberry Pi ADC input

Xaratustrah
2016

"""

from version import __version__
from setuptools import setup
from subprocess import call
import shutil, os

NAME = 'rdgui'

app = ['rdgui.py']

packages = []

includes = ['sip',
            'PyQt5',
            'PyQt5.QtWidgets',
            'PyQt5.QtCore',
            'PyQt5.QtGui',
            'atexit']

excludes = ['PyQt5.QtDesigner', 'PyQt5.QtNetwork', 'PyQt5.QtOpenGL', 'PyQt5.QtScript', 'PyQt5.QtTest', 'PyQt5.QtSql',
            'PyQt5.QtWebKit', 'PyQt5.QtXml', 'PyQt5.phonon', 'PyQt5.uic.port_v2', 'numpy', 'scipy', 'matplotlib']

resources = ['rsrc', ]

plist = dict(CFBundleName=NAME,
             CFBundleShortVersionString=__version__,
             CFBundleGetInfoString='%s %s' % (NAME, __version__),
             CFBundleExecutable=NAME,
             CFBundleIdentifier='org.%s.%s' % (NAME, NAME),
             )

QTDIR = '/opt/local/libexec/qt5'

options = {'argv_emulation': True,
           'includes': includes,
           'excludes': excludes,
           'packages': packages,
           'resources': resources,
           'plist': plist,
           'frameworks': ['%s/plugins/platforms/libqcocoa.dylib' % QTDIR],
           # 'iconfile': 'rsrc/icon.icns'
           }

data_files = ['rsrc/qt.conf']

setup(
    app=app,
    name=NAME,
    version=__version__,
    url='https://github.com/xaratustrah/rasdaq',
    license='GPLv.3',
    data_files=data_files,
    setup_requires=['py2app'],
    options={'py2app': options},
)

os.makedirs('dist/' + NAME + '.app/Contents/PlugIns/platforms', exist_ok=True)
shutil.copyfile('dist/' + NAME + '.app/Contents/Frameworks/libqcocoa.dylib',
                'dist/' + NAME + '.app/Contents/PlugIns/platforms/libqcocoa.dylib')

print('Now creating the disk image...')
command = 'hdiutil create {}_{}.dmg -volname {} -fs HFS+ -srcfolder dist/{}.app'.format(NAME, __version__, NAME, NAME)
command = command.split()
call(command)
