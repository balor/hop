# -*- coding: utf-8 -*-
import sys
import os
from distutils.core import setup

if sys.version_info < (2,6):
    raise NotImplementedError(u'You need Python 2.6 or higher to use HOP.')

import hop


setup(
    name = 'HOP',
    version = hop.__version__,
    description = (
        u'HTML Object Printer - simple web helpers without dependencies.'
    ),
    author = u'Michał Thoma',
    author_email = 'michal@balor.pl',
    licence = 'MIT',
    packages = ['hop', 'hop.tags'],
    platforms = ['any'],
    url = 'https://github.com/balor/hop',
)
