#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""
平时都是使用此文件导入配置，但是有些特殊的需要和开发者机器相关的，需要在local_configs中书写
"""

from .local_configs import *
from shisuo_event_extractor.utils import setup_logging

setup_logging()
