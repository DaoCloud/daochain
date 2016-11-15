import os

from flask import Flask
from flask import redirect, send_from_directory

from server.api import load_api
from server.settings import SERVER_ROOT_PATH


def setup_routes(app):
    @app.route('/')
    def index():
        return redirect('/index.html')

    @app.route('/<path:path>')
    def send_file(path):
        return send_from_directory(os.path.join(SERVER_ROOT_PATH, 'static'), path)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
        return response


def create_app(name=None):
    app = Flask(name or 'app')
    app.config.root_path = os.path.dirname(os.path.abspath(__file__))
    app.config.from_pyfile('settings.py')
    load_api(app)
    setup_routes(app)
    return app


app = create_app()
if __name__ == '__main__':
    app.run('0.0.0.0', 8000, True, use_reloader=True)
