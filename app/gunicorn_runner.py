from __future__ import unicode_literals

import multiprocessing
import sys
from os import path

import gunicorn.app.base
from gevent import monkey
from gunicorn.six import iteritems

sys.path.append(path.abspath(path.abspath(path.join(__file__, path.pardir, path.pardir))))
monkey.patch_all()


def number_of_workers():
    return multiprocessing.cpu_count() * 2


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
    from server import create_app
    options = {
        'bind': '%s:%s' % ('0.0.0.0', '8000'),
        'workers': number_of_workers(),
        'worker_class': 'gevent',
        'timeout': 600,
        'accesslog': '-',
        'errorlog': '-'
    }
    StandaloneApplication(create_app(), options).run()


if __name__ == '__main__':
    run_app()
