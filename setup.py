# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from setuptools import setup, find_packages

setup(
    name='meteor-ejson',
    version='1.1.0',
    packages=find_packages(exclude=['*tests*']),
    url='https://github.com/lyschoening/meteor-ejson-python',
    license='MIT',
    author='Lars Schöning',
    author_email='lars@lyschoening.de',
    description='Encoder and Decoder for Extended JSON (EJSON) as used in Meteor and DDP.',
    install_requires=[
        'six'
    ],
    test_suite='nose.collector',
    tests_require=[
        'nose>=1.1.2',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
