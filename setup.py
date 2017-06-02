#!/usr/bin/env python3
# -*- coding: utf8 -*-

from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='PersonalPass',
    version='1.0',
    url='https://github.com/DerNitro/PersonalPass',
    license='GPLv3',
    author='Sergey <DerNitro> Utkin',
    author_email='utkins01@gmail.com',
    description='Small gen password',
    long_description=long_description,

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3 :: Only',
        'Natural Language :: Russian',
        'Operating System :: POSIX :: Linux',
        'Topic :: Security'
    ],

    scripts=['bin/PersonalPass.py']
)
