#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 m <m@meng.hu>
#
# Distributed under terms of the MIT license.

"""

"""
from flask import Flask

def create_app(config='development'):
    app = Flask(__name__)
    app.config.from_object(f'services.settings.{config}_config')
    return app
