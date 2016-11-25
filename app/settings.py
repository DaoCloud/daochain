import os

ERROR_404_HELP = False

SECRET_KEY = os.getenv('SECRET_KEY') or 'monitor'
HUB_ENDPOINT = os.getenv('HUB_ENDPOINT') or 'http://api.daocloud.co'
ETH_RPC_ENDPOINT = os.getenv('ETH_RPC_ENDPOINT') or 'localhost:8545'
DATA_DIR = os.path.expanduser('~/.daocloud')

RECENT_HASH_TIME_BUCKET_SIZE = 50

if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)

SOURCE_ROOT = os.path.abspath(os.path.dirname(__file__))


def in_data_dir(*path):
    return os.path.join(DATA_DIR, *path)
