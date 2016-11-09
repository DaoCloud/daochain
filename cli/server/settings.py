import os

SECRET_KEY = os.environ.get('SECRET_KEY') or 'monitor'

ROOT_PATH = os.path.dirname(__file__)
MEDIA_PATH = os.environ.get('MEDIA_PATH') or os.path.join(ROOT_PATH, 'static', 'uploads')