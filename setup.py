#!/usr/bin/env python

from setuptools import setup

setup(
    name='ovarian_cancer_pipeline',
    version='0.0.5',
    author='Bernie Pope',
    author_email='bjpope@unimelb.edu.au',
    packages=['src'],
    entry_points={
        'console_scripts': ['ovarian_cancer_pipeline = src.main:main']
    },
    url='https://github.com/bjpop/ovarian_cancer_pipeline',
    license='LICENSE',
    description='ovarian_cancer_pipeline is a demonstration pipeline based on Ruffus', 
    long_description=open('README.md').read(),
    install_requires=[
        "ruffus == 2.6.3",
        "pipeline_base == 1.0.0"
    ],
)
