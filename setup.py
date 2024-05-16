#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='gsay',
      version='1.0',
      # Modules to import from other scripts:
      packages=find_packages(),
      package_data={'': ['license.txt']},
      include_package_data=True,
      # Executables
      scripts=["gpt-ui"],
     )