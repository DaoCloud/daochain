import logging
import os
import sys

import requests
from flask import Flask
from flask import send_file, send_from_directory

from api import load_api
from blockchain import web3_client
from settings import SOURCE_ROOT
from storage import Cache

log = logging.getLogger(__name__)

console_handler = logging.StreamHandler(sys.stderr)


def setup_logging():
    root_logger = logging.getLogger()
    root_logger.addHandler(console_handler)
    root_logger.setLevel(logging.DEBUG)
    # Disable requests logging
    logging.getLogger("requests").propagate = False


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


def fetch_nodes():
    from time import sleep
    from threading import Thread

    def fetch_loop():
        while True:
            try:
                nodes = requests.get('http://blockchain.daocloud.io/nodes.json').json()
                w3 = web3_client()
                peers = w3.admin.peers
                for n in nodes:
                    w3.admin.addPeer(n)
                if not len(peers) == len(nodes):
                    log.info('fetched nodes: %s' % ', '.join(nodes))
                    sleep(60)
            except Exception:
                log.error('Fail to fetch nodes.json')
                sleep(5)

    t = Thread(target=fetch_loop)
    t.setDaemon(True)
    t.start()


def create_app(name=None):
    setup_logging()
    app = Flask(name or 'app')
    app.config.root_path = os.path.dirname(os.path.abspath(__file__))
    app.config.from_pyfile('settings.py')
    Cache.init()
    load_api(app)
    setup_routes(app)
    fetch_nodes()
    return app


if __name__ == '__main__':
    app = create_app()
    app.run('0.0.0.0', 8000, True, use_reloader=True)
