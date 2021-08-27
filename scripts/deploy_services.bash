#! /bin/bash
#
# deploy_services.bash
# Copyright (C) 2019 m <m@meng.hu>
#
# Distributed under terms of the MIT license.
#

# simple server run
FLASK_APP=blog flask run

# gunicorn server run
#gunicorn -w 4 "blog:create_app()" -b 0.0.0.0:5000

# using supervisord to watch the gunicorn
#supervisord -c instance/supervisord.conf

# restart blog
supervisorctl -c instance/supervisord.conf restart blog
