import os

import requests
from flask import Flask
from flask import send_file, send_from_directory
from gevent import sleep, spawn

from api import load_api
from blockchain import web3_client
from settings import SOURCE_ROOT
from storage import Cache


def setup_routes(app):
    @app.route('/')
    def index():
        return send_file(os.path.join(SOURCE_ROOT, 'static', 'index.html'))

    @app.route('/<path:path>')
    def static_files(path):
        return send_from_directory(os.path.join(SOURCE_ROOT, 'static'), path)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
        return response


def fetch_peers():
    while True:
        try:
            nodes = requests.get('http://blockchain.daocloud.io/nodes.json').json()
            w3 = web3_client()
            for n in nodes:
                w3.admin.addPeer(n)
            sleep(30)
        except Exception:
            sleep(10)


def create_app(name=None):
    app = Flask(name or 'app')
    app.config.root_path = os.path.dirname(os.path.abspath(__file__))
    app.config.from_pyfile('settings.py')
    Cache.init()
    load_api(app)
    setup_routes(app)
    spawn(fetch_peers())
    return app


if __name__ == '__main__':
    app = create_app()
    app.run('0.0.0.0', 8000, True, use_reloader=True)
