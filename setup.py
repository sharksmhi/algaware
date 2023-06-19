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


root_path = pathlib.Path(__file__).parent.resolve()

requirements = []
with open(pathlib.Path(root_path, 'requirements.txt')) as fh:
    for line in fh:
        repo = line.strip()
        if not repo:
            continue
        if repo.startswith('git'):
            repo_name = repo.split('.git')[0].split('/')[-1]
            repo = f"{repo_name} @ {repo}"
        requirements.append(repo)


setuptools.setup(
    name="algaware",
    version="0.3.0",
    author="Johannes Johansson",
    author_email="magnus.wenzer@smhi.se",
    description="No able to specify archive root directory",
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
