#!/usr/bin/env python

from setuptools import setup, find_packages
from codecs import open
from os import path

# Get the long description from DESCRIPTION.rst
with open(path.join(path.abspath(path.dirname(__file__)),
          'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

tests_require = ['nose >= 1.3.7']

setup(
    name='tr55',
    version='1.3.0',
    description='A Python implementation of TR-55.',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/azavea/tr-55',
    author='Azavea Inc.',
    license='Apache License 2.0',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
    ],
    keywords='tr-55 watershed hydrology',
    packages=find_packages(exclude=['test']),
    python_requires=">=3.7",
    install_requires=[
        'numpy >= 1.20.3',
    ],
    extras_require={
        'dev': [],
        'test': tests_require,
    },
    test_suite='nose.collector',
    tests_require=tests_require,
)
