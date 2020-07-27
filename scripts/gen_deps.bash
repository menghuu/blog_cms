#! /bin/bash
#
# gen_deps.bash
# Copyright (C) 2019 m <m@meng.hu>
#
# Distributed under terms of the MIT license.
#


set -e -x

source ./.envrc
echo -----

echo generate common requirements
pip-compile ./requirements/requirements.in --output-file requirements.txt
echo -----

echo generate dev requirements
pip-compile ./requirements/dev-requirements.in --output-file dev-requirements.txt
echo -----

pip-sync requirements.txt dev-requirements.txt
echo finish!!
