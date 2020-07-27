#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 m <m@meng.hu>
#
# Distributed under terms of the MIT license.

"""
这里应该存放着和api服务配置相关的配置, 可能包括的内容有:
- redis url
- es url

和模型有关的配置, 应该和你训练以及cli所使用的配置存放位置一致, 而不是放在这里

总之,这里应该存放着和服务有关的配置
"""
import os

class _BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY', os.urandom(16))
    ...

class _DevelopmentConfig(_BaseConfig):
    ENV = 'development'
    ...

class _ProductionConfig(_BaseConfig):
    ENV = 'production'
    ...


development_config = _DevelopmentConfig()
production_config = _ProductionConfig()
