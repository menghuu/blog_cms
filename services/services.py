#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 m <m@meng.hu>
#
# Distributed under terms of the MIT license.

"""
example service here
"""

from flask import Flask
from flask_restful import Api, Resource, reqparse

parser = reqparse.RequestParser()
parser.add_argument('rate', type=int, help='Rate to charge for this resource')
args = parser.parse_args()


class SimpleApi(Resource):
    def __init__(self):
        pass

    def post(self):
        args = parser.parse_args()
        return args


if __name__ == '__main__':
    # just for testing this restful api
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(SimpleApi, '/simple')
    app.run(debug=True, host='0.0.0.0', port=8080)

