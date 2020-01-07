# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 08:05:22 2018

@author: a002028
"""

import setuptools
import os


def long_description():
    if os.path.exists('README.md'):
        return open('README.md').read()
    else:
        return 'No readme file'


setuptools.setup(
    name="algaware",
    version="0.0.1",
    author="Johannes Johansson",
    author_email="johannes.johansson@smhi.se",
    description="TEST version 0.0.1 Package to plot algaware figures",
    long_description=long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    package_data={'algaware': [os.path.join('etc', '*.yaml'),
                               os.path.join('etc', 'statistics', '*.txt')]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
