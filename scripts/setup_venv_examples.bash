#! /bin/bash
#
# setup_venv_examples.bash
# Copyright (C) 2019 m <m@meng.hu>
#
# Distributed under terms of the MIT license.
#

# 创建虚拟环境
python3 -m venv .venv

# 将虚拟环境加到PATH中(建议使用direnv来自动source)
source .envrc

# 安装依赖管理工具
pip install --upgrade pip
pip install pip-tools
