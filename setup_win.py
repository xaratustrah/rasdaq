# !/usr/bin/env python
"""
A client/server code for Raspberry Pi ADC input

Xaratustrah
2016

"""

from distutils.core import setup
import py2exe
import matplotlib
from version import __version__

name = 'rdgui'

pkgs = []

includes = ['sip',
            'PyQt5',
            'PyQt5.QtWidgets',
            'PyQt5.QtCore',
            'PyQt5.QtGui',
            'zmq',
            ]

excludes = ['pkg_resources',
            'doctest',
            'pdb',
            'optparse',
            'jsonschema',
            'tornado',
            'setuptools',
            'urllib2',
            'tkinter']

options = {'bundle_files': 3,
           # 'optimize': 2,
           'compressed': True,
           'includes': includes,
           'excludes': excludes,
           'packages': pkgs
           }

datafiles = matplotlib.get_py2exe_datafiles() + \
            [("platforms", ["C:\\Python34\\Lib\\site-packages\\PyQt5\\plugins\\platforms\\qwindows.dll"]),
             ("", [r"c:\windows\syswow64\MSVCP100.dll", r"C:\Windows\System32\MSVCR100.dll"]),
             ("", [r"C:\Python34\Lib\site-packages\numpy\core\libifcoremd.dll"]),
             ("", [r"C:\Python34\Lib\site-packages\numpy\core\libifportmd.dll"]),
             ("", [r"C:\Python34\Lib\site-packages\numpy\core\libiomp5md.dll"]),
             ("", [r"C:\Python34\Lib\site-packages\numpy\core\svml_dispmd.dll"]),
             ("", [r"C:\Python34\Lib\site-packages\numpy\core\libiompstubs5md.dll"]),
             ("", [r"C:\Python34\Lib\site-packages\numpy\core\libmmd.dll"]),
             ("", [r"C:\Python34\Lib\site-packages\spectrum\mydpss.pyd"])
             ]

setup(
    name=name,
    version=__version__,
    url='https://github.com/xaratustrah/iq_suite',
    license='GPL V 3.0',
    zipfile=None,
    data_files=datafiles,
    windows=[{
        'script': 'rdgui.py',
        # 'icon_resources': [(1, 'rsrc/icon.ico')],
        'dest_base': 'rdgui'
    }],
    options={'py2exe': options}
)
