import re
import sys
from os import path

sys.path.append(path.abspath(path.abspath(path.join(__file__, path.pardir, path.pardir))))
from gunicorn.app.wsgiapp import run


def run_app():
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.argv += ["-k", "gevent", "-w", "2",
                 "--max-requests", "5000", "--max-requests-jitter", "5000",
                 "--access-logfile", "-", "--error-logfile", "-",
                 '-b', '0.0.0.0:8000', 'server.app:app']

    sys.exit(run())


if __name__ == "__main__":
    run_app()
