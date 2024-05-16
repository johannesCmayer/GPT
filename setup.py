#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='gpt-ui',
      version='1.0',
      # Modules to import from other scripts:
      packages=find_packages(),
      package_data={'gpt-ui': ['*.yaml']},
      include_package_data=True,
      install_requires=[],
      # Executables
      scripts=["gpt-ui"],
     )