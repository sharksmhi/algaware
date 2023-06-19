# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 08:05:22 2018

@author: a002028
"""

import setuptools
import os
import pathlib


def long_description():
    if os.path.exists('README.md'):
        return open('README.md').read()
    else:
        return 'No readme file'


root = pathlib.Path(__file__).parent.resolve()

requirements = []
with open(pathlib.Path(root, 'requirements.txt')) as fh:
    for line in fh:
        requirements.append(line.strip())


setuptools.setup(
    name="algaware",
    version="0.3.1",
    author="Johannes Johansson",
    author_email="magnus.wenzer@smhi.se",
    description="",
    long_description=long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/sharksmhi/algaware",
    # url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    package_data={'algaware': [os.path.join('etc', '*.yaml'),
                               os.path.join('etc', '*.txt'),
                               os.path.join('etc', 'statistics', '*.txt')]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=requirements,
)
