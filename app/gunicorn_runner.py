from __future__ import unicode_literals

import multiprocessing
import sys
from os import path

import gunicorn.app.base
from gunicorn.six import iteritems

sys.path.append(path.abspath(path.abspath(path.join(__file__, path.pardir, path.pardir))))
from server import create_app


def number_of_workers():
    return multiprocessing.cpu_count()


class StandaloneApplication(gunicorn.app.base.BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super(StandaloneApplication, self).__init__()

    def load_config(self):
        config = dict([(key, value) for key, value in iteritems(self.options)
                       if key in self.cfg.settings and value is not None])
        for key, value in iteritems(config):
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


def run_app():
    options = {
        'bind': '%s:%s' % ('0.0.0.0', '8000'),
        'workers': number_of_workers(),
        'worker_class': 'gevent',
        'accesslog': '-',
        'errorlog': '-'
    }
    StandaloneApplication(create_app(), options).run()


if __name__ == '__main__':
    run_app()
