#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 m <m@meng.hu>
#
# Distributed under terms of the MIT license.

"""

"""
import logging
import logging.config
import os
import json

def setup_logging(default_path='config/logging.json', default_level=logging.INFO):
    """Setup logging configuration

    """
    if os.path.exists(default_path):
        with open(default_path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)
