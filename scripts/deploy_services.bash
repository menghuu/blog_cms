#! /bin/bash
#
# deploy_services.bash
# Copyright (C) 2019 m <m@meng.hu>
#
# Distributed under terms of the MIT license.
#

FLASK_ENV=${FLASK_ENV:-development}
gunicorn -w 4 "services:wsgi:create_app(config='${FLASK_ENV}')"
