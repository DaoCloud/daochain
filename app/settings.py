import os

SECRET_KEY = os.environ.get('SECRET_KEY') or 'monitor'
HUB_ENDPOINT = os.getenv('HUB_ENDPOINT', 'http://api.daocloud.co')

DATA_DIR = os.path.expanduser('~/.daocloud')

if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)

SOURCE_ROOT = os.path.abspath(os.path.dirname(__file__))


def in_data_dir(*path):
    return os.path.join(DATA_DIR, *path)
