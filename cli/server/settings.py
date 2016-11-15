import os

SECRET_KEY = os.environ.get('SECRET_KEY') or 'monitor'

SERVER_ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
