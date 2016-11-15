import os

SECRET_KEY = os.environ.get('SECRET_KEY') or 'monitor'
HUB_ENDPOINT = os.getenv('HUB_ENDPOINT', 'http://api.daocloud.co')

SERVER_ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
