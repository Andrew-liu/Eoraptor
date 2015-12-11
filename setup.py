#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


setup(
    name='MongoBlog',
    version='0.0.1',
    author='andrewliu',
    author_email='liu.bin.coder@gmail.com',
    description='The simple blog developed by torando and bootstrap',
    license='Apache License',
    packages=find_packages("MongoBlog"),
    package_dir={"": "MongoBlog"},
    install_requires=[
        'nose',
        'pymongo',
        'mysql-python',
        'redis',
        'tornado',
        'requests',
        'mock',
        'Markdown'
    ],
    entry_points={
        'console_scripts': ["MongoBlog=app:main"]
    },
)
