from flask import render_template

from schwifty.core import app


@app.route('/')
def index():
    return "hello, world!"
