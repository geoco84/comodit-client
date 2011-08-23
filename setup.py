#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

requires = [
    'python >= 2.6',
]

setup(
    name='cortex-client',
    version='0.7.0',
    description='cortex command line client',
    author='Laurent Eschenauer',
    author_email='laurent.eschenauer@gmail.com',
    url='https://github.com/guardis/cortex-client',
    license='',
    packages=['cortex_client', 'cortex_client/control', 'cortex_client/rest', 'cortex_client/util'],
    scripts=[
        'cortex'
    ],
    include_package_data=True,
    data_files=[('/usr/bin/', ['cortex']),],
    # Here's the list of usable classifiers:
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Programming Language :: Python',
        'Operating System :: POSIX',
        'Topic :: Content Management',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
        'Development Status :: 3 - Alpha',
    ],
    install_requires=requires,
)
