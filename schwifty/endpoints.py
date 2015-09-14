from schwifty import settings
from flask import request
from flask_restful import Resource

class Welcome(Resource):
    def get(self):
        val = {"message": "GET Schwifty!"}
        val["version"] = settings.VERSION
        return val

class Search(Resource):
    def get(self):
        return {}

class Detail(Resource):
    def get(self, datatype, eid):
        return {}
