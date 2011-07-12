#!/usr/bin/env python
"""
QuickBooks Merchant Services Bindings

@license: LGPLv3
@author: Alex Goodwin <alex@artistechmedia.com>
@copyright: ArtisTech Media, LLC 2009
"""
from setuptools import setup, find_packages

from pyqbms import VERSION

setup(
    name='pyqbms',
    version='.'.join(map(str, VERSION)),
    description='Python Bindings for Quick Books Merchant Services.',
    author='Eric Bartels',
    author_email='ebartels@gmail.com',
    packages=find_packages(),
    url = "https://github.com/bartels/pyqbms",
    license = "LGPLv3",
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Office/Business',
    ],
    include_package_data = True,
)
