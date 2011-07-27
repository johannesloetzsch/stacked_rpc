#!/usr/bin/python
# -*- coding: utf-8 -*-
"""To install run this script with root-privileges"""

import sys
from distutils.core import setup
import subprocess
import os

def get_py_modules(path):
    for root, dirs, files in os.walk(path):
        for file_name in files:
            full_name = root + os.sep + file_name
            if os.path.splitext(full_name)[1] == '.py':
                without_ext = os.path.splitext(full_name)[0]
                yield without_ext.replace(os.sep, '.')

"""installation using python-distutils"""
sys.argv.append('install')
setup(name='stacked_rpc',
      version='0.1',
      licence='GPL',
      platforms='should be platform-independent',
      url='https://github.com/johannesloetzsch/stacked_rpc',
      author='Johannes Lötzsch',
      author_email='github_donotspam_at_johannesloetzsch.de',
      description = open('README').readline().strip(),
      long_description = ''.join(open('README').readlines()[1:]).strip(),
      py_modules = list(get_py_modules('stacked_rpc'))
	 )

"""test if everything works"""
print
subprocess.call('./test_stacked_rpc.py')
