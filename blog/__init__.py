#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 m <m@meng.hu>
#
# Distributed under terms of the MIT license.

import os
from flask import Flask, redirect, url_for, request
from flask_flatpages import pygments_style_defs


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # register the database commands
    from .models import db
    db.init_app(app)

    # apply the blueprints to the app
    from . import blog
    blog.pages.init_app(app)

    @app.route('/pygments.css')
    def pygments_css():
        return pygments_style_defs('colorful'), 200, {'Content-Type': 'text/css'}

    # app.register_blueprint(auth.bp, url_prefix='/')
    app.register_blueprint(blog.bp, url_prefix='/blog')

    from . import resources
    app.register_blueprint(resources.bp, url_prefix='/resources')

    # make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    # app.add_url_rule("/", endpoint="index")

    @app.route('/', methods=['GET'])
    def index():
        return redirect(url_for('blog.index'), 302)

    @app.route('/update_instance', methods=['GET'])
    def update():
        token = request.args.get('token')
        if token == app.config['UPDATE_INSTANCE_TOKEN']:
            ...

    return app
