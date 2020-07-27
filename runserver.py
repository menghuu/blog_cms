#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 m <m@meng.hu>
#
# Distributed under terms of the MIT license.

from setuptools import setup

setup(
    name='blog',
    packages=['blog'],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask-sqlalchemy'
    ],
)