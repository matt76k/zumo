#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
from setuptools import setup

setup(
    name = "Zumo",
    version = "0.0.1",
    description = ("Mahjong library, tools"),
    author = "matt",
    author_email = "matt76k@gmail.com",
    license = "MIT License",
    url = "https://github.com/matt76k/zumo",
    packages = ['zumo'],
    classifiers = [
        "Topic :: Games/Entertainment :: Board Games",
        "Programming Language :: Python :: 3.4",
        "License :: OSI Approved :: MIT License"
    ],
    install_requires = open('requirements.txt').read().splitlines(),
)
