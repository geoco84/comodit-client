#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from platform import python_version
from setuptools import setup, find_packages

major, minor, micro = python_version().split('.')

if major != '2' or minor not in ['6', '7']:
    raise Exception('unsupported version of python')

requires = [
    'python >= 2.6',
]

# Utility function to read the README file.
# http://packages.python.org/an_example_pypi_project/setuptools.html
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def get_template_files():
    files = []
    for name in os.listdir('templates'):
        files.append('templates/' + name)
    return files

VERSION = '0.0'
RELEASE = '0'
try:
    from cortex_client import version
    VERSION = version.VERSION
    RELEASE = version.RELEASE
except ImportError:
    pass

setup(
    name = 'cortex-client',
    description = 'ComodIT command line client and python library.',
    long_description = read('README'),
    version = VERSION + "-" + RELEASE,
    author = 'see AUTHOR file',
    author_email = 'team@comodit.com',
    url = 'https://github.com/guardis/cortex-client',
    license = 'MIT',
    packages = find_packages(),
    scripts = [
        'cortex'
    ],
    include_package_data = True,
    # Here's the list of usable classifiers:
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers = [
        'Programming Language :: Python',
        'Operating System :: POSIX',
        'Topic :: Content Management',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
        'Development Status :: 4 - Beta'
    ],
    install_requires = requires,
    data_files = [
        ('/etc/bash_completion.d', ['auto_completion/cortex']),
        ('/etc/cortex/client/templates', get_template_files()),
        ('/etc/cortex/', ['conf/cortex-client.conf'])
    ],
)
