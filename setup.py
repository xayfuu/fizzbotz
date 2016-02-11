#!/usr/bin/env python

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

dependency_links = [
    # TODO: figure out a better way to make discord.py async branch work
    'https://codeload.github.com/Rapptz/discord.py/legacy.tar.gz/async#egg=discord.py-0.10.0a0',
]

install_requires = [
    'beautifulsoup4',
    'discord.py==0.10.0a0'
]

setup_requires = [
    'pytest-runner'
]

tests_require = [
    'pytest',
    'pytest-asyncio'
]

setup(
    name='fizzbotz',
    version='0.1.0',
    description='A bot for discord written in Python implementing some basic commands.',
    long_description=readme + '\n\n' + history,
    author='Matthew Martens',
    author_email='matthew.s.martens@gmail.com',
    url='https://github.com/martensm/fizzbotz',
    packages=[
        'fizzbotz',
    ],
    package_dir={'fizzbotz':
                 'fizzbotz'},
    include_package_data=True,
    dependency_links=dependency_links,
    install_requires=install_requires,
    setup_requires=setup_requires,
    license='MIT',
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
