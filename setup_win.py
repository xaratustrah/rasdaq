# !/usr/bin/env python
"""
A client/server code for Raspberry Pi ADC input

Xaratustrah
2016

"""

from distutils.core import setup
from version import __version__
from glob import glob
import PyQt5
import py2exe
import zmq
import zmq.libzmq

NAME = 'rdgui'

packages = ['zmq']

includes = ['sip', 'atexit', 'zmq', 'zmq.backend.cython']

excludes = ['zmq.libzmq']
dll_excludes = ['libzmq.pyd']

options = {
    'optimize': 2,
    'compressed': True,
    'includes': includes,
    'excludes': excludes,
    'dll_excludes' : dll_excludes,
    'packages': packages
}

data_files = []

qt_platform_plugins = [('platforms', glob(PyQt5.__path__[0] + r'\plugins\platforms\*.*'))]
zmq_plugin = [('', glob(zmq.__path__[0] + r'\backend\cython\error.pyd'))]

data_files.extend(qt_platform_plugins)
data_files.extend(zmq_plugin)

setup(
    name=NAME,
    version=__version__,
    url='https://github.com/xaratustrah/rasdaq',
    license='GPLv.3',
    zipfile=None,
    data_files=data_files,
    windows=[{
        'script': 'rdgui.py',
        #'icon_resources': [(1, 'rsrc/icon.ico')]
    }],
    options={'py2exe': options}
)
