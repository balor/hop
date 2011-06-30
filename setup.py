# -*- coding: utf-8 -*-
import sys
import os
from distutils.core import setup

if sys.version_info < (2,6):
    raise NotImplementedError(u'You need Python 2.6 or higher to use hop.')

from hop import __version__, __author__, __website__


setup(
    name = 'hop',
    version = str(__version__),
    description = (
        u'HTML Object Printer - simple web helpers without dependencies.'
    ),
    author = __author__,
    author_email = 'michal@balor.pl',
    license = 'MIT',
    packages = ['hop', 'hop.tags'],
    platforms = ['any'],
    url = str(__website__),
)
