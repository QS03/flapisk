"""API route declarations

Imports any Flask resources and registers them as API routes to accept
requests and return responses on the Flask server.
"""
from flask import Blueprint, current_app, jsonify
from flask_restful import Api, Resource


class ApiRouter:
    def __init__(self, url_prefix, app=None):
        self.app = app
        self.url_prefix = url_prefix
        self.api_blueprint = Blueprint(self.__class__.__name__, __name__)
        self.api = Api(self.api_blueprint, catch_all_404s=True)

    def init_app(self, app):
        self.app = app

    def add_resource(self, resource, path, methods=None, strict_slashes=False):
        if methods is None:
            self.api.add_resource(resource, path, strict_slashes=strict_slashes)
        else:
            self.api.add_resource(resource, path, methods=methods, strict_slashes=strict_slashes)

    def register_routes(self):
        self.app.register_blueprint(self.api_blueprint, url_prefix=self.url_prefix)


api_router = ApiRouter(url_prefix="/api")
