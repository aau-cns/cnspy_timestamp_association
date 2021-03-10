#!/usr/bin/env python

from distutils.core import setup

setup(name='trajectory',
      version='1.0',
      description='Python Distribution Utilities',
      author='Roland Jung',
      author_email='roland.jung@aau.at',
      url='https://gitlab.aau.at/aau-cns/py3_pkgs/trajectory/',
      packages=['distutils', 'distutils.command', 'numpy', 'matplotlib', ' scipy', 'tqdm', 'pandas', 'argparse', 'PyYAML', 'spatialmath-python', 'numpy_utils', 'trajectory', 'csv2dataframe', 'ros_csv_formats'],
     )
