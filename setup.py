# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='Kpop Stats',
    version='0.1.0',
    description='Data extraction and exploration of Kpop world',
    long_description=readme,
    author='Romain Fonta',
    author_email='romainfonta@hotmail.fr',
    url='https://github.com/kennethreitz/samplemod',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)