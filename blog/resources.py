#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 m <m@meng.hu>
#
# Distributed under terms of the MIT license.

import os
from flask import current_app, send_from_directory, send_file
from flask.blueprints import Blueprint

bp = Blueprint('resources', 'resources')


@bp.route('/<path:path>')
def resources(path):
    return send_from_directory(os.path.join(current_app.instance_path, 'resources'), path)
