from flask import Flask
from flask_restful import Api

from schwifty import settings

app = Flask("Schwifty")
api = Api(app)
app.config.from_object(settings)
