#!/usr/bin/env python
# -*- coding: utf-8 -*-

import fizzbotz

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

dependency_links = [
    # TODO: figure out a better way to make discord.py async branch work
    'https://codeload.github.com/Rapptz/discord.py/legacy.tar.gz/async#egg=discord.py-0.10.0a0',
]

install_requires = [
    'discord.py==0.10.0a0',
    'beautifulsoup4'
]

setup_requires = [
    'pytest-runner'
]

tests_require = [
    'pytest'
]

setup(
    name=fizzbotz.__name__,
    version=fizzbotz.__version__,
    description=fizzbotz.__description__,
    long_description=readme + '\n\n' + history,
    author=fizzbotz.__author__,
    author_email=fizzbotz.__email__,
    url=fizzbotz.__url__,
    packages=[
        'fizzbotz',
    ],
    package_dir={'fizzbotz':
                 'fizzbotz'},
    include_package_data=True,
    dependency_links=dependency_links,
    install_requires=install_requires,
    setup_requires=setup_requires,
    license=fizzbotz.__license__,
    zip_safe=False,
    keywords='fizzbotz',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=tests_require
)
