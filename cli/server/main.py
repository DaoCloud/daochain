import os

from flask import Flask
from flask import send_file
from flask_restful import abort

from server.api import load_api


def setup_routes(app):
    @app.route('/')
    def index():
        if not os.path.isfile('static/index.html'):
            abort(404)
        return send_file('static/index.html')

        # MEDIA_PATH = app.config.get('MEDIA_PATH')
        # if not os.path.isdir(MEDIA_PATH):
        #     os.mkdir(MEDIA_PATH)
        #
        # @app.route('/uploads/<path:filename>')
        # def base_static(filename):
        #     return send_from_directory(MEDIA_PATH, filename)


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
